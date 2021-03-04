# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""This package contains code for creating environment modules, which can
include TCL non-hierarchical modules, LUA hierarchical modules, and others.
"""

from __future__ import absolute_import

from .tcl import TclModulefileWriter
from .lmod import LmodModulefileWriter
from .ups_table import UpsTableModulefileWriter
from .ups_version import UpsVersionModulefileWriter

__all__ = [
    'TclModulefileWriter',
    'LmodModulefileWriter'
    'UpsTableModulefileWriter',
    'UpsVersionModulefileWriter',
]

module_types = {
    'tcl': TclModulefileWriter,
    'lmod': LmodModulefileWriter,
    'ups_table': UpsTableModulefileWriter,
    'ups_version': UpsVersionModulefileWriter,
}
