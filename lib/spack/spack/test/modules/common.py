# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import stat
import sys

import pytest

import spack.error
import spack.modules.tcl
import spack.spec
from spack.modules.common import UpstreamModuleIndex
from spack.spec import Spec

pytestmark = pytest.mark.skipif(sys.platform == "win32",
                                reason="does not run on windows")


def test_update_dictionary_extending_list():
    target = {
        'foo': {
            'a': 1,
            'b': 2,
            'd': 4
        },
        'bar': [1, 2, 4],
        'baz': 'foobar'
    }
    update = {
        'foo': {
            'c': 3,
        },
        'bar': [3],
        'baz': 'foobaz',
        'newkey': {
            'd': 4
        }
    }
    spack.modules.common.update_dictionary_extending_lists(target, update)
    assert len(target) == 4
    assert len(target['foo']) == 4
    assert len(target['bar']) == 4
    assert target['baz'] == 'foobaz'


@pytest.fixture()
def mock_module_defaults(monkeypatch):
    def impl(*args):
        # No need to patch both types because neither override base
        monkeypatch.setattr(spack.modules.common.BaseConfiguration,
                            'defaults',
                            [arg for arg in args])

    return impl


@pytest.fixture()
def mock_package_perms(monkeypatch):
    perms = stat.S_IRGRP | stat.S_IWGRP
    monkeypatch.setattr(spack.package_prefs,
                        'get_package_permissions',
                        lambda spec: perms)

    yield perms


def test_modules_written_with_proper_permissions(mock_module_filename,
                                                 mock_package_perms,
                                                 mock_packages, config):
    spec = spack.spec.Spec('mpileaks').concretized()

    # The code tested is common to all module types, but has to be tested from
    # one. TCL picked at random
    generator = spack.modules.tcl.TclModulefileWriter(spec, 'default')
    generator.write()

    assert mock_package_perms & os.stat(
        mock_module_filename).st_mode == mock_package_perms


@pytest.mark.parametrize('module_type', ['tcl', 'lmod', 'ups_table', 'ups_version'])
def test_modules_default_symlink(
        module_type, mock_packages, mock_module_filename, mock_module_defaults, config
):
    spec = spack.spec.Spec('mpileaks@2.3').concretized()
    mock_module_defaults(spec.format('{name}{@version}'))

    generator_cls = spack.modules.module_types[module_type]
    generator = generator_cls(spec, 'default')
    generator.write()

    link_path = os.path.join(os.path.dirname(mock_module_filename), 'default')
    assert os.path.islink(link_path)
    assert os.readlink(link_path) == mock_module_filename


class MockDb(object):
    def __init__(self, db_ids, spec_hash_to_db):
        self.upstream_dbs = db_ids
        self.spec_hash_to_db = spec_hash_to_db

    def db_for_spec_hash(self, spec_hash):
        return self.spec_hash_to_db.get(spec_hash)


class MockSpec(object):
    def __init__(self, unique_id):
        self.unique_id = unique_id

    def dag_hash(self):
        return self.unique_id


def test_upstream_module_index():
    s1 = MockSpec('spec-1')
    s2 = MockSpec('spec-2')
    s3 = MockSpec('spec-3')
    s4 = MockSpec('spec-4')

    tcl_module_index = """\
module_index:
  {0}:
    path: /path/to/a
    use_name: a
""".format(s1.dag_hash())

    module_indices = [
        {
            'tcl': spack.modules.common._read_module_index(tcl_module_index)
        },
        {}
    ]

    dbs = [
        'd0',
        'd1'
    ]

    mock_db = MockDb(
        dbs,
        {
            s1.dag_hash(): 'd0',
            s2.dag_hash(): 'd1',
            s3.dag_hash(): 'd0'
        }
    )
    upstream_index = UpstreamModuleIndex(mock_db, module_indices)

    m1 = upstream_index.upstream_module(s1, 'tcl')
    assert m1.path == '/path/to/a'

    # No modules are defined for the DB associated with s2
    assert not upstream_index.upstream_module(s2, 'tcl')

    # Modules are defined for the index associated with s1, but none are
    # defined for the requested type
    assert not upstream_index.upstream_module(s1, 'lmod')

    # A module is registered with a DB and the associated module index has
    # modules of the specified type defined, but not for the requested spec
    assert not upstream_index.upstream_module(s3, 'tcl')

    # The spec isn't recorded as installed in any of the DBs
    with pytest.raises(spack.error.SpackError):
        upstream_index.upstream_module(s4, 'tcl')


def test_get_module_upstream():
    s1 = MockSpec('spec-1')

    tcl_module_index = """\
module_index:
  {0}:
    path: /path/to/a
    use_name: a
""".format(s1.dag_hash())

    module_indices = [
        {},
        {
            'tcl': spack.modules.common._read_module_index(tcl_module_index)
        }
    ]

    dbs = ['d0', 'd1']

    mock_db = MockDb(
        dbs,
        {s1.dag_hash(): 'd1'}
    )
    upstream_index = UpstreamModuleIndex(mock_db, module_indices)

    setattr(s1, "installed_upstream", True)
    try:
        old_index = spack.modules.common.upstream_module_index
        spack.modules.common.upstream_module_index = upstream_index

        m1_path = spack.modules.common.get_module('tcl', s1, True)
        assert m1_path == '/path/to/a'
    finally:
        spack.modules.common.upstream_module_index = old_index


def test_load_installed_package_not_in_repo(install_mockery, mock_fetch,
                                            monkeypatch):
    # Get a basic concrete spec for the trivial install package.
    spec = Spec('trivial-install-test-package')
    spec.concretize()
    assert spec.concrete

    # Get the package
    pkg = spec.package

    def find_nothing(*args):
        raise spack.repo.UnknownPackageError(
            'Repo package access is disabled for test')

    try:
        pkg.do_install()

        spec._package = None
        monkeypatch.setattr(spack.repo, 'get', find_nothing)
        with pytest.raises(spack.repo.UnknownPackageError):
            spec.package

        module_path = spack.modules.common.get_module('tcl', spec, True)
        assert module_path
        pkg.do_uninstall()
    except Exception:
        pkg.remove_prefix()
        raise
