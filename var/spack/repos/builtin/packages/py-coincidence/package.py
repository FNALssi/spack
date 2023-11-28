# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCoincidence(PythonPackage):
    """Helper functions for pytest."""

    homepage = "https://github.com/python-coincidence/coincidence"
    pypi = "coincidence/coincidence-0.6.5.tar.gz"

    maintainers("greenc-FNAL", "gartung", "marcmengel", "vitodb")

    license("MIT")

    version("0.6.5", sha256="0d6511665d23d237838adec59d51423712cd563fb1be32c1058a6de10c06fe44")

    depends_on("py-whey", type="build")

    depends_on("py-domdf-python-tools@2.8.0:", type=("build", "run"))
    depends_on("py-pytest@6.2.0:", type=("build", "run"))
    depends_on("py-pytest-regressions@2.0.2:", type=("build", "run"))
    depends_on("py-typing-extensions@3.7.4.3:", type=("build", "run"))
