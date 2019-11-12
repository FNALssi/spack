# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RModelmetrics(RPackage):
    """Collection of metrics for evaluating models written in C++ using
    'Rcpp'."""

    homepage = "https://cloud.r-project.org/package=ModelMetrics"
    url      = "https://cloud.r-project.org/src/contrib/ModelMetrics_1.1.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/ModelMetrics"

    version('1.2.2', sha256='66d6fc75658287fdbae4d437b51d26781e138b8baa558345fb9e5a2df86a0d95')
    version('1.2.0', sha256='3021ae88733695a35d66e279e8e61861431f14c9916a341f0a562f675cf6ede9')
    version('1.1.0', 'd43175001f0531b8810d2802d76b7b44')

    depends_on('r@3.2.2:', type=('build', 'run'))
    depends_on('r-rcpp', type=('build', 'run'))
    depends_on('r-data-table', when='@1.2.0:', type=('build', 'run'))
