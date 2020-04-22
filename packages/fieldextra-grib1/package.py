# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install fieldextra-grib1
#
# You can edit this file again by typing:
#
#     spack edit fieldextra-grib1
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class FieldextraGrib1(MakefilePackage):

    homepage = "http://www.cosmo-model.org/content/support/software/default.html"
    url      = "https://github.com/COSMO-ORG/fieldextra/archive/v13.2.0.tar.gz"
    git      = 'git@github.com:COSMO-ORG/fieldextra.git'
    maintainers = ['elsagermann']

    version('12.5', commit='fe0a8b14314d7527168fd5684d89828bbd83ebf2')

    variant('build_type', default='optimized', description='Build type', values=('debug', 'optimized'))
    variant('openmp', default=True)

    build_directory = 'grib1/src'

    def edit(self, spec, prefix):
        if self.compiler.name == 'gcc':
            mode = 'gnu'
        else:
            mode = self.compiler.name
        if spec.variants['build_type'].value == 'debug':
            mode += ',dbg'
        elif spec.variants['build_type'].value == 'optimized':
            mode += ',opt'
        if self.spec.variants['openmp'].value:
            mode += ',omp'
        env['mode'] = mode

        with working_dir(self.build_directory):
            optionsfilter = FileFilter('Makefile')
            optionsfilter.filter('INCDIR *=.*', 'INCDIR = ../include')
            optionsfilter.filter('LIBDIR *=.*', 'LIBDIR = ' + self.prefix + '/lib')
            optionsfilter.filter('INCLUDEDIR *=.*', 'INCLUDEDIR = ' + self.prefix + '/include')