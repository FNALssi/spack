# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Davix(CMakePackage):
    """High-performance file management over WebDAV/HTTP."""

    homepage = "https://dmc.web.cern.ch/projects/davix"
    url      = "https://github.com/cern-fts/davix/releases/download/R_0_7_5/davix-0.7.5.tar.gz" 

    def url_for_version(self,version):
        return "https://github.com/cern-fts/davix/releases/download/R_%s/davix-%s.tar.gz" % ( version.underscored, version.dotted)

    version('0.7.6', sha256='a2e7fdff29f7ba247a3bcdb08ab1db6d6ed745de2d3971b46526986caf360673')
    version('0.7.5', sha256='d920ca976846875d83af4dc50c99280bb3741fcf8351d5733453e70fa5fe6fc8')
    version('0.7.4', sha256='302a61ec90d597ab034da7eb1757b64c6b108f41e2d23145103c70bd273b80cc')
    version('0.7.3', sha256='cd46276e72c6a0da1e2ad30eb66ec509a4c023687767c62a66713fa8c23d328a')
    version('0.6.9', sha256='fbd97eb5fdf82ca48770d06bf8e2805b35f23255478aa381a9d25a49eb98e348')
    version('0.6.8', sha256='e1820f4cc3fc44858ae97197a3922cce2a1130ff553b080ba19e06eb8383ddf7')

    variant('cxxstd',
            default='11',
            values=('11', '14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')

    variant('thirdparty',default=True)

    depends_on('pkgconfig', type='build')
    depends_on('libxml2')
    depends_on('uuid')
    depends_on('openssl')
    depends_on('gsoap', when='+thirdparty')

    def cmake_args(self):
        cmake_args = ['-DCMAKE_CXX_STANDARD={0}'.format(
                      self.spec.variants['cxxstd'].value)]

        if self.spec.variants['thirdparty']:
            cmake_args.append('-DENABLE_THIRD_PARTY_COPY=ON')

        if 'darwin' in self.spec.architecture:
            cmake_args.append('-DCMAKE_MACOSX_RPATH=ON')
        return cmake_args
