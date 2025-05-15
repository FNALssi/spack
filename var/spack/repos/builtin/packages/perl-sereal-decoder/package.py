# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlSerealDecoder(PerlPackage):
    """Fast, compact, powerful binary deserialization"""

    homepage = "https://metacpan.org/pod/Sereal::Decoder"
    url = "https://cpan.metacpan.org/authors/id/Y/YV/YVES/Sereal-Decoder-5.004.tar.gz"

    maintainers("greenc-FNAL", "EbiArnie", "gartung", "marcmengel")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("5.004", sha256="68ef0314d87d1a6e60bb0f66fcf43eb2cacdeb1754432f5e25e784e39d3e6784")
    version("5.001", sha256="b27c33ec910de57d72817cc2baa0bf039d5e647a7359edfcf1cf7d5efeeed9b2")
    version("5.000_002", sha256="abe866ec8480a364745d00b8980d8f866dd0edd1420102e9e5ed82e932269507")
    version("4.025", sha256="8e0e3b9a9af1a778b7de21506fa30797fb1b520dcd002f3f29e6dcb52446dea5")

    provides("perl-sereal-decoder-constants")
    provides("perl-sereal-performance")

    depends_on("c", type="build")  # generated

    depends_on("perl@5.8.0:", type=("build", "link", "run", "test"))

    depends_on("perl-devel-checklib@1.16:", type=("build"))

    depends_on("perl-data-dumper", type=("build", "test"))
    depends_on("perl-scalar-util", type=("build", "test"))
    depends_on("perl-test-deep", type=("build", "link", "test"))
    depends_on("perl-test-differences", type=("build", "link", "test"))
    depends_on("perl-test-longstring", type=("build", "link", "test"))
    depends_on("perl-test-warn", type=("build", "link", "test"))
    depends_on("zstd", type=("build", "link", "run", "test"))

    def setup_build_environment(self, env: EnvironmentModifications) -> None:
        # These are not currently available in Spack
        env.set("SEREAL_USE_BUNDLED_CSNAPPY", "1")
        env.set("SEREAL_USE_BUNDLED_MINIZ", "1")
        env.set("USE_UNALIGNED", "1")
        env.set("NO_ASM", "0")
        env.set("ZSTD_DISABLE_ASM", "0")
