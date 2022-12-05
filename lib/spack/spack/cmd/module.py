# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from typing import Callable, Dict

import spack.cmd.modules.lmod
import spack.cmd.modules.tcl
import spack.cmd.modules.ups_table
import spack.cmd.modules.ups_version

description = "generate/manage module files"
section = "user environment"
level = "short"


_subcommands: Dict[str, Callable] = {}


def setup_parser(subparser):
    sp = subparser.add_subparsers(metavar="SUBCOMMAND", dest="module_command")
    spack.cmd.modules.lmod.add_command(sp, _subcommands)
    spack.cmd.modules.tcl.add_command(sp, _subcommands)
    spack.cmd.modules.ups_table.add_command(sp, _subcommands)
    spack.cmd.modules.ups_version.add_command(sp, _subcommands)


def module(parser, args):
    _subcommands[args.module_command](parser, args)
