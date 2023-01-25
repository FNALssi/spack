# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlMathCephes(PerlPackage):
    """This module provides an interface to over 150 functions of the
    cephes math library of Stephen Moshier."""

    homepage = "https://metacpan.org/pod/Math::Cephes"
    url = "http://search.cpan.org/CPAN/authors/id/S/SH/SHLOMIF/Math-Cephes-0.5305.tar.gz"

    version(
        "0.53.05",
        sha256="561a800a4822e748d2befc366baa4b21e879a40cc00c22293c7b8736caeb83a1",
        url="https://cpan.metacpan.org/authors/id/S/SH/SHLOMIF/Math-Cephes-0.5305.tar.gz",
    )
    version(
        "0.53.04",
        sha256="5d2cc55965505eee4fc8da870cb4754c0eeff144afb6254848d8c3b24b30a981",
        url="https://cpan.metacpan.org/authors/id/S/SH/SHLOMIF/Math-Cephes-0.5304.tar.gz",
    )
