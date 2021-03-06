# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RCheckmate(RPackage):
    """Tests and assertions to perform frequent argument checks.
    A substantial part of the package was written in C to
    minimize any worries about execution time overhead."""

    homepage = "https://cloud.r-project.org/package=checkmate"
    url      = "https://cloud.r-project.org/src/contrib/checkmate_1.8.4.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/checkmate"

    version('1.9.4', sha256='faa25754b757fe483b876f5d07b73f76f69a1baa971420892fadec4af4bbad21')
    version('1.8.4', '00bd2c464386614da208f82c4b21910b')

    depends_on('r@3.0.0:', type=('build', 'run'))
    depends_on('r-backports@1.1.0:', type=('build', 'run'))
