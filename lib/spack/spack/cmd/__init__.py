# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from __future__ import print_function

import os
import re
import sys
import argparse

import llnl.util.tty as tty
from llnl.util.lang import index_by
from llnl.util.tty.colify import colify
from llnl.util.tty.color import colorize
from llnl.util.filesystem import working_dir

import spack.config
import spack.paths
import spack.spec
import spack.store
import spack.util.spack_json as sjson
from spack.error import SpackError


# cmd has a submodule called "list" so preserve the python list module
python_list = list

# Patterns to ignore in the commands directory when looking for commands.
ignore_files = r'^\.|^__init__.py$|^#'


def python_name(cmd_name):
    """Convert ``-`` to ``_`` in command name, to make a valid identifier."""
    return cmd_name.replace("-", "_")


def require_python_name(pname):
    """Require that the provided name is a valid python name (per
    python_name())."""
    if python_name(pname) != pname:
        raise PythonNameError(pname)


def cmd_name(python_name):
    """Convert module name (with ``_``) to command name (with ``-``)."""
    return python_name.replace('_', '-')


def require_cmd_name(cname):
    """Require that the provided name is a valid command name (per
    cmd_name())."""
    if cmd_name(cname) != cname:
        raise CommandNameError(cname)


def find_commands(*command_paths):
    """Get a sorted list of all spack commands at the specified path.

    This will list the command_path directory and find the commands
    there to construct the list.  It does not actually import the python
    files - just gets the names.
    """
    command_list = []
    if command_paths is not None:
        for path in command_paths:
            for file in os.listdir(path):
                if file.endswith(".py") and not re.search(ignore_files, file):
                    cmd = re.sub(r'.py$', '', file)
                    command_list.append(cmd_name(cmd))
        command_list.sort()
    return command_list


def remove_options(parser, *options):
    """Remove some options from a parser."""
    for option in options:
        for action in parser._actions:
            if vars(action)['option_strings'][0] == option:
                parser._handle_conflict_resolve(None, [(option, action)])
                break


def parse_specs(args, **kwargs):
    """Convenience function for parsing arguments from specs.  Handles common
       exceptions and dies if there are errors.
    """
    concretize = kwargs.get('concretize', False)
    normalize = kwargs.get('normalize', False)
    tests = kwargs.get('tests', False)

    try:
        specs = spack.spec.parse(args)
        for spec in specs:
            if concretize:
                spec.concretize(tests=tests)  # implies normalize
            elif normalize:
                spec.normalize(tests=tests)

        return specs

    except spack.spec.SpecParseError as e:
        msg = e.message + "\n" + str(e.string) + "\n"
        msg += (e.pos + 2) * " " + "^"
        raise SpackError(msg)

    except spack.spec.SpecError as e:

        msg = e.message
        if e.long_message:
            msg += e.long_message

        raise SpackError(msg)


def elide_list(line_list, max_num=10):
    """Takes a long list and limits it to a smaller number of elements,
       replacing intervening elements with '...'.  For example::

           elide_list([1,2,3,4,5,6], 4)

       gives::

           [1, 2, 3, '...', 6]
    """
    if len(line_list) > max_num:
        return line_list[:max_num - 1] + ['...'] + line_list[-1:]
    else:
        return line_list


def disambiguate_spec(spec, env):
    """Given a spec, figure out which installed package it refers to.

    Arguments:
        spec (spack.spec.Spec): a spec to disambiguate
        env (spack.environment.Environment): a spack environment,
            if one is active, or None if no environment is active
    """
    hashes = env.all_hashes() if env else None
    matching_specs = spack.store.db.query(spec, hashes=hashes)
    if not matching_specs:
        tty.die("Spec '%s' matches no installed packages." % spec)

    elif len(matching_specs) > 1:
        format_string = '{name}{@version}{%compiler}{arch=architecture}'
        args = ["%s matches multiple packages." % spec,
                "Matching packages:"]
        args += [colorize("  @K{%s} " % s.dag_hash(7)) +
                 s.cformat(format_string) for s in matching_specs]
        args += ["Use a more specific spec."]
        tty.die(*args)

    return matching_specs[0]


def gray_hash(spec, length):
    h = spec.dag_hash(length) if spec.concrete else '-' * length
    return colorize('@K{%s}' % h)


def display_specs_as_json(specs, deps=False):
    """Convert specs to a list of json records."""
    seen = set()
    records = []
    for spec in specs:
        if spec.dag_hash() in seen:
            continue
        seen.add(spec.dag_hash())
        records.append(spec.to_record_dict())

        if deps:
            for dep in spec.traverse():
                if dep.dag_hash() in seen:
                    continue
                seen.add(dep.dag_hash())
                records.append(dep.to_record_dict())

    sjson.dump(records, sys.stdout)


def iter_groups(specs, indent, all_headers):
    """Break a list of specs into groups indexed by arch/compiler."""
    # Make a dict with specs keyed by architecture and compiler.
    index = index_by(specs, ('architecture', 'compiler'))
    ispace = indent * ' '

    # Traverse the index and print out each package
    for i, (architecture, compiler) in enumerate(sorted(index)):
        if i > 0:
            print()

        header = "%s{%s} / %s{%s}" % (
            spack.spec.architecture_color,
            architecture if architecture else 'no arch',
            spack.spec.compiler_color,
            compiler if compiler else 'no compiler')

        # Sometimes we want to display specs that are not yet concretized.
        # If they don't have a compiler / architecture attached to them,
        # then skip the header
        if all_headers or (architecture is not None or compiler is not None):
            sys.stdout.write(ispace)
            tty.hline(colorize(header), char='-')

        specs = index[(architecture, compiler)]
        specs.sort()
        yield specs


def display_specs(specs, args=None, **kwargs):
    """Display human readable specs with customizable formatting.

    Prints the supplied specs to the screen, formatted according to the
    arguments provided.

    Specs are grouped by architecture and compiler, and columnized if
    possible.

    Options can add more information to the default display. Options can
    be provided either as keyword arguments or as an argparse namespace.
    Keyword arguments take precedence over settings in the argparse
    namespace.

    Args:
        specs (list of spack.spec.Spec): the specs to display
        args (optional argparse.Namespace): namespace containing
            formatting arguments

    Keyword Args:
        paths (bool): Show paths with each displayed spec
        deps (bool): Display dependencies with specs
        long (bool): Display short hashes with specs
        very_long (bool): Display full hashes with specs (supersedes ``long``)
        namespace (bool): Print namespaces along with names
        show_flags (bool): Show compiler flags with specs
        variants (bool): Show variants with specs
        indent (int): indent each line this much
        groups (bool): display specs grouped by arch/compiler (default True)
        decorators (dict): dictionary mappng specs to decorators
        header_callback (function): called at start of arch/compiler groups
        all_headers (bool): show headers even when arch/compiler aren't defined

    """
    def get_arg(name, default=None):
        """Prefer kwargs, then args, then default."""
        if name in kwargs:
            return kwargs.get(name)
        elif args is not None:
            return getattr(args, name, default)
        else:
            return default

    paths         = get_arg('paths', False)
    deps          = get_arg('deps', False)
    hashes        = get_arg('long', False)
    namespace     = get_arg('namespace', False)
    flags         = get_arg('show_flags', False)
    full_compiler = get_arg('show_full_compiler', False)
    variants      = get_arg('variants', False)
    groups        = get_arg('groups', True)
    all_headers   = get_arg('all_headers', False)

    decorator     = get_arg('decorator', None)
    if decorator is None:
        decorator = lambda s, f: f

    indent = get_arg('indent', 0)

    hlen = 7
    if get_arg('very_long', False):
        hashes = True
        hlen = None

    format_string = get_arg('format', None)
    if format_string is None:
        nfmt = '{namespace}.{name}' if namespace else '{name}'
        ffmt = ''
        if full_compiler or flags:
            ffmt += '{%compiler.name}'
            if full_compiler:
                ffmt += '{@compiler.version}'
            ffmt += ' {compiler_flags}'
        vfmt = '{variants}' if variants else ''
        format_string = nfmt + '{@version}' + ffmt + vfmt

    transform = {'package': decorator, 'fullpackage': decorator}

    def fmt(s, depth=0):
        """Formatter function for all output specs"""
        string = ""
        if hashes:
            string += gray_hash(s, hlen) + ' '
        string += depth * "    "
        string += s.cformat(format_string, transform=transform)
        return string

    def format_list(specs):
        """Display a single list of specs, with no groups"""
        # create the final, formatted versions of all specs
        formatted = []
        for spec in specs:
            formatted.append((fmt(spec), spec))
            if deps:
                for depth, dep in spec.traverse(root=False, depth=True):
                    formatted.append((fmt(dep, depth), dep))
                formatted.append(('', None))  # mark newlines

        # unless any of these are set, we can just colify and be done.
        if not any((deps, paths)):
            colify((f[0] for f in formatted), indent=indent)
            return

        # otherwise, we'll print specs one by one
        max_width = max(len(f[0]) for f in formatted)
        path_fmt = "%%-%ds%%s" % (max_width + 2)

        # getting lots of prefixes requires DB lookups. Ensure
        # all spec.prefix calls are in one transaction.
        with spack.store.db.read_transaction():
            for string, spec in formatted:
                if not string:
                    print()  # print newline from above
                    continue

                if paths:
                    print(path_fmt % (string, spec.prefix))
                else:
                    print(string)

    if groups:
        for specs in iter_groups(specs, indent, all_headers):
            format_list(specs)
    else:
        format_list(sorted(specs))


def spack_is_git_repo():
    """Ensure that this instance of Spack is a git clone."""
    with working_dir(spack.paths.prefix):
        return os.path.isdir('.git')


########################################
# argparse types for argument validation
########################################
def extant_file(f):
    """
    Argparse type for files that exist.
    """
    if not os.path.isfile(f):
        raise argparse.ArgumentTypeError('%s does not exist' % f)
    return f


########################################
# Exceptions
########################################
class PythonNameError(SpackError):
    """Exception class thrown for impermissible python names"""
    def __init__(self, name):
        self.name = name
        super(PythonNameError, self).__init__(
            '{0} is not a permissible Python name.'.format(name))


class CommandNameError(SpackError):
    """Exception class thrown for impermissible command names"""
    def __init__(self, name):
        self.name = name
        super(CommandNameError, self).__init__(
            '{0} is not a permissible Spack command name.'.format(name))
