# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""This package contains code for creating environment modules, which can
include TCL non-hierarchical modules, LUA hierarchical modules, and others.
"""

from __future__ import absolute_import

from .common import disable_modules
from .lmod import LmodModulefileWriter
from .tcl import TclModulefileWriter
from .ups_table import UpsTableModulefileWriter
from .ups_version import UpsVersionModulefileWriter

__all__ = [
    'TclModulefileWriter',
    'LmodModulefileWriter',
    'UpsTableModulefileWriter',
    'UpsVersionModulefileWriter',
    'disable_modules'
]

module_types = {
    'tcl': TclModulefileWriter,
    'lmod': LmodModulefileWriter,
    'ups_table': UpsTableModulefileWriter,
    'ups_version': UpsVersionModulefileWriter,
}

