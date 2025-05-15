# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlSerealEncoder(PerlPackage):
    """Fast, compact, powerful binary serialization"""

    homepage = "https://metacpan.org/pod/Sereal::Encoder"
    url = "https://cpan.metacpan.org/authors/id/Y/YV/YVES/Sereal-Encoder-5.004.tar.gz"

    maintainers("greenc-FNAL", "EbiArnie", "gartung", "marcmengel")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("5.004", sha256="5e5a86ccd32dae34ed80932ecbe5c68e29752b5de0e9b0a793ab7eb2ca55cb1b")
    version("5.001", sha256="2367f2f5f1486f32f65c3905048918de55639c79d1835ab56789f70cedfbbac3")
    version("4.025", sha256="0fd51ba6083026650d08526758261173c18ab8234c5526fac7edb91ad9c6026e")

    provides("perl-sereal-encoder-constants")

    depends_on("c", type="build")  # generated

    depends_on("perl@5.8.0:", type=("build", "link", "run", "test"))

    depends_on("perl-devel-checklib@1.16:", when="@5.004:", type=("build"))
    depends_on("perl-extutils-parsexs@2.21:", when="@:5.001", type=("build"))
    depends_on("perl-extutils-makemaker@7.0:", when="@:5.001", type=("build"))

    depends_on("perl-sereal-decoder@5.0:", type=("build", "test"), when="@5.0:")
    depends_on("perl-sereal-decoder@:4.999999", type=("build", "test"), when="@:4.999999")
    depends_on("perl-test-longstring", type=("build", "test"))
    depends_on("perl-test-deep", type=("build", "test"))
    depends_on("perl-test-differences", type=("build", "test"))
    depends_on("perl-test-warn", type=("build", "test"))
    depends_on("perl-scalar-util", type=("build", "test"))
    depends_on("perl-data-dumper", type=("build", "test"))

    def setup_build_environment(self, env: EnvironmentModifications) -> None:
        # These are not currently available in Spack
        env.set("SEREAL_USE_BUNDLED_CSNAPPY", "1")
        env.set("SEREAL_USE_BUNDLED_MINIZ", "1")
        env.set("USE_UNALIGNED", "1")
        env.set("NO_ASM", "0")
        env.set("ZSTD_DISABLE_ASM", "0")
