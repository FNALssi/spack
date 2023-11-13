# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""This module implements the classes necessary to generate UpsVersion
non-hierarchical modules.
"""
import os.path
from typing import Dict, Optional, Tuple

import spack.config
import spack.spec
import spack.tengine as tengine

from .common import BaseConfiguration, BaseContext, BaseFileLayout, BaseModuleFileWriter


#: UpsVersion specific part of the configuration
def configuration(module_set_name: str) -> dict:
    return spack.config.get(f"modules:{module_set_name}:ups_version", {})


# Caches the configuration {spec_hash: configuration}
configuration_registry: Dict[Tuple[str, str, bool], BaseConfiguration] = {}


def make_configuration(
    spec: spack.spec.Spec, module_set_name: str, explicit: Optional[bool] = None
) -> BaseConfiguration:
    """Returns the ups_version configuration for spec"""
    explicit = bool(spec._installed_explicitly()) if explicit is None else explicit
    key = (spec.dag_hash(), module_set_name, explicit)
    try:
        return configuration_registry[key]
    except KeyError:
        return configuration_registry.setdefault(
            key, UpsVersionConfiguration(spec, module_set_name, explicit)
        )


def make_layout(
    spec: spack.spec.Spec, module_set_name: str, explicit: Optional[bool] = None
) -> BaseFileLayout:
    """Returns the layout information for spec"""
    return UpsVersionFileLayout(make_configuration(spec, module_set_name, explicit))


def make_context(
    spec: spack.spec.Spec, module_set_name: str, explicit: Optional[bool] = None
) -> BaseContext:
    """Returns the context information for spec"""
    return UpsVersionContext(make_configuration(spec, module_set_name, explicit))


class UpsVersionConfiguration(BaseConfiguration):
    """Configuration class for ups_version module files."""


class UpsVersionFileLayout(BaseFileLayout):
    """File layout for ups_version module files."""

    @property
    def modulerc(self):
        """Returns the modulerc file associated with current module file"""
        return os.path.join(os.path.dirname(self.filename), ".modulerc")

    @property
    def filename(self):
        """Name of the module file for the current spec."""
        # Just the name of the file
        filename = os.path.basename(self.use_name)
        subdirname = self.spec.format("{name}/{version}.version").replace("-", "_")
        if not os.access(os.path.join(self.dirname(), subdirname), os.F_OK):
            os.makedirs(os.path.join(self.dirname(), subdirname))
        return os.path.join(self.dirname(), subdirname, filename)


class UpsVersionContext(BaseContext):
    """Context class for ups_version module files."""

    @tengine.context_property
    def prerequisites(self):
        """List of modules that needs to be loaded automatically."""
        return self._create_module_list_of("specs_to_prereq")


class UpsVersionModulefileWriter(BaseModuleFileWriter):
    """Writer class for ups_version module files."""

    default_template = "modules/modulefile.ups_version"

    modulerc_header = ["#%Module4.7"]

    hide_cmd_format = "module-hide --soft --hidden-loaded %s"
