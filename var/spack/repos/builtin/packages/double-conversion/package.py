# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class DoubleConversion(CMakePackage):
    """This project (double-conversion) provides binary-decimal and decimal-binary
    routines for IEEE doubles.

    The library consists of efficient conversion routines that have been
    extracted from the V8 JavaScript engine. The code has been refactored
    and improved so that it can be used more easily in other projects.

    There is extensive documentation in src/double-conversion.h. Other examples
    can be found in test/cctest/test-conversions.cc.
    """

    homepage = "https://github.com/google/double-conversion"
    url      = "https://github.com/google/double-conversion/archive/v2.0.1.zip"

    version('2.0.1', sha256='476aefbdc2051bbcca0d5919ebc293c90a7ad2c0cb6c4ad877d6e665f469146b')
    version('2.0.0', sha256='437df89059bfa6c1c0f8703693c2584a57f75289ed7020d801c9befb23f46a26')
    version('1.1.5', sha256='496fd3354fa0ff17562907632f5560c1d444ea98b6069f1436fa573949b94fb0')
    version('1.1.4', sha256='24b5edce8c88f0f632c83e60e0bde11252656dc3b714ba195619c1798ff28834')
    version('1.1.3', sha256='f0d1b8621592a3cf010c04c3e1c0f08455fc0fc7ee22e1583e2a63dc6d3e3871')

    def cmake_args(self):
        return ['-DCMAKE_POSITION_INDEPENDENT_CODE:BOOL=true']
