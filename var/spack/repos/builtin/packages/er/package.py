# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Er(CMakePackage):
    """Encoding and redundancy on a file set"""

    homepage = "https://github.com/ecp-veloc/er"
    url = "https://github.com/ecp-veloc/er/archive/v0.0.3.tar.gz"
    git = "https://github.com/ecp-veloc/er.git"
    tags = ["ecp"]

    maintainers = ["CamStan", "gonsie"]

    version("main", branch="main")
    version("0.3.0", sha256="01bc71bfb2ebb015ccb948f2bb9138b70972a3e8be0e53f9a4844e46b106a36c")
    version("0.2.0", sha256="9ddfe2b63682ed0e89685f9b7d5259ef82b802aba55c8ee78cc15a7adbad6bc0")
    version("0.1.0", sha256="543afc1c48bb2c67f48c32f6c9efcbf7bb27f2e622ff76f2c2ce5618c77aacfc")
    version("0.0.4", sha256="c456d34719bb57774adf6d7bc2fa9917ecb4a9de442091023c931a2cb83dfd37")
    version("0.0.3", sha256="243b2b46ea274e17417ef5873c3ed7ba16dacdfdaf7053d1de5434e300de796b")

    depends_on("mpi")
    depends_on("kvtree+mpi")
    depends_on("rankstr", when="@0.0.4:")
    depends_on("redset")
    depends_on("shuffile")
    depends_on("zlib", type="link")

    depends_on("kvtree@1.3", when="@0.2.0")

    deps = ["kvtree", "rankstr", "redset", "shuffile"]
    for dep in deps:
        depends_on(dep + "@main", when="@main")

    variant("shared", default=True, description="Build with shared libraries")
    for dep in deps:
        depends_on(dep + "+shared", when="@0.1: +shared")
        depends_on(dep + "~shared", when="@0.1: ~shared")

    def cmake_args(self):
        spec = self.spec
        args = []
        args.append(self.define("MPI_C_COMPILER", spec["mpi"].mpicc))
        args.append(self.define("WITH_KVTREE_PREFIX", spec["kvtree"].prefix))
        args.append(self.define("WITH_REDSET_PREFIX", spec["redset"].prefix))
        args.append(self.define("WITH_SHUFFILE_PREFIX", spec["shuffile"].prefix))

        if spec.satisfies("@0.0.4:"):
            args.append(self.define("WITH_RANKSTR_PREFIX", spec["rankstr"].prefix))

        if spec.satisfies("@0.1.0:"):
            args.append(self.define_from_variant("BUILD_SHARED_LIBS", "shared"))
        else:
            if spec.satisfies("platform=cray"):
                args.append(self.define("ER_LINK_STATIC", True))

        return args
