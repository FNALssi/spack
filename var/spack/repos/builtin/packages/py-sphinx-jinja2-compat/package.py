# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySphinxJinja2Compat(PythonPackage):
    """Patches Jinja2 v3 to restore compatibility with earlier Sphinx versions."""

    homepage = "https://github.com/sphinx-toolbox/sphinx-jinja2-compat"
    pypi = "sphinx_jinja2_compat/sphinx_jinja2_compat-0.2.0.post1.tar.gz"

    maintainers("greenc-FNAL", "gartung", "marcmengel", "vitodb")

    license("MIT")

    version(
        "0.2.0.post1", sha256="974289a12a9f402108dead621e9c15f7004e945d5cfcaea8d6419e94d3fa95a3"
    )

    depends_on("py-whey", type="build")
    depends_on("py-whey-pth", type="build")

    depends_on("py-jinja2@2.10:", type=("build", "run"))
    depends_on("py-markupsafe@1:", type=("build", "run"))
