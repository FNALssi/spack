# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTestDeep(PerlPackage):
    """Extremely flexible deep comparison"""

    homepage = "https://metacpan.org/pod/Test::Deep"
    url = "https://cpan.metacpan.org/authors/id/R/RJ/RJBS/Test-Deep-1.127.tar.gz"

    version("1.204", sha256="b6591f6ccdd853c7efc9ff3c5756370403211cffe46047f082b1cd1611a84e5f")
    version("1.130", sha256="4064f494f5f62587d0ae501ca439105821ee5846c687dc6503233f55300a7c56")
    version("1.128", sha256="852d7e836fba8269b0b755082051a24a1a309d015a8b76838790af9e3760092f")
    version("1.127", sha256="b78cfc59c41ba91f47281e2c1d2bfc4b3b1b42bfb76b4378bc88cc37b7af7268")

    provides("perl-test-deep-all")
    provides("perl-test-deep-any")
    provides("perl-test-deep-array")
    provides("perl-test-deep-arrayeach")
    provides("perl-test-deep-arrayelementsonly")
    provides("perl-test-deep-arraylength")
    provides("perl-test-deep-arraylengthonly")
    provides("perl-test-deep-blessed")
    provides("perl-test-deep-boolean")
    provides("perl-test-deep-cache")
    provides("perl-test-deep-cache-simple")
    provides("perl-test-deep-class")
    provides("perl-test-deep-cmp")
    provides("perl-test-deep-code")
    provides("perl-test-deep-hash")
    provides("perl-test-deep-hasheach")
    provides("perl-test-deep-hashelements")
    provides("perl-test-deep-hashkeys")
    provides("perl-test-deep-hashkeysonly")
    provides("perl-test-deep-ignore")
    provides("perl-test-deep-isa")
    provides("perl-test-deep-listmethods")
    provides("perl-test-deep-mm")
    provides("perl-test-deep-methods")
    provides("perl-test-deep-notest")
    provides("perl-test-deep-none")
    provides("perl-test-deep-number")
    provides("perl-test-deep-obj")
    provides("perl-test-deep-ref")
    provides("perl-test-deep-reftype")
    provides("perl-test-deep-regexp")
    provides("perl-test-deep-regexpmatches")
    provides("perl-test-deep-regexponly")
    provides("perl-test-deep-regexpref")
    provides("perl-test-deep-regexprefonly")
    provides("perl-test-deep-regexpversion")
    provides("perl-test-deep-scalarref")
    provides("perl-test-deep-scalarrefonly")
    provides("perl-test-deep-set")
    provides("perl-test-deep-shallow")
    provides("perl-test-deep-stack")
    provides("perl-test-deep-string")
    provides("perl-test-deep-subhash")
    provides("perl-test-deep-subhashelements")
    provides("perl-test-deep-subhashkeys")
    provides("perl-test-deep-subhashkeysonly")
    provides("perl-test-deep-superhash")
    provides("perl-test-deep-superhashelements")
    provides("perl-test-deep-superhashkeys")
    provides("perl-test-deep-superhashkeysonly")
    depends_on("perl-extutils-makemaker", type="build")
    depends_on("perl-scalar-util@1.9:", type="run")
    depends_on("perl-list-util@1.9:", type="run")
