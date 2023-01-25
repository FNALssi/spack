# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTextCsv(PerlPackage):
    """Comma-separated values manipulator (using XS or PurePerl)"""

    homepage = "https://metacpan.org/pod/Text::CSV"
    url = "https://cpan.metacpan.org/authors/id/I/IS/ISHIGAKI/Text-CSV-1.95.tar.gz"

    version("1.95", sha256="7e0a11d9c1129a55b68a26aa4b37c894279df255aa63ec8341d514ab848dbf61")
