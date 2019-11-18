from __future__ import print_function
from setuptools import setup
from distutils.extension import Extension
import warnings
import os
import sys


use_cython = True

try:
    from Cython.Build import cythonize
except ImportError:
    use_cython = False
    warnings.warn('No cython found -- install will use pre-generated C files')




def create_ext_modules():
    """
    Build commands require preinstalled numpy to compile the c extensions. A global "import numpy"
    here would break tox and also if installed as a dependency from another python package.
    So we only require numpy for the cases where its header files are actually needed.
    """

    build_commands = ('build', 'build_ext', 'build_py',
                    'build_clib', 'build_scripts', 'bdist_wheel', 'bdist_rpm',
                    'bdist_wininst', 'bdist_msi', 'bdist_mpkg', 'build_sphinx')

    ext_modules = []
    for command in build_commands:
        if command in sys.argv[1:]:
            try:
                import numpy
            except ImportError:
                raise Exception(
                    "please install numpy, need numpy header files to compile c extensions")
            ext_modules = [Extension("imnet.process_strings_cy",
                                    sources=["imnet/process_strings_cy.pyx"],
                                    include_dirs=[numpy.get_include()])]
            if use_cython:
                print('Using cython')
                ext_modules = cythonize(ext_modules)

            break
    return ext_modules

currdir = os.getcwd()

import numpy
process_strings_cy = Extension(
    'imnet.process_strings_cy',
    sources=["imnet/process_strings_cy.pyx"],
    include_dirs=[numpy.get_include()]
)

setup(name="imnet",
      author="Rok Roskar",
      version='0.1.post2',
      author_email="roskar@ethz.ch",
      url="http://github.com/rokroskar/imnet",
      package_dir={'imnet/': ''},
      packages=['imnet'],
      #ext_modules=create_ext_modules(),
      ext_modules = [process_strings_cy],
      scripts=['scripts/imnet-analyze'],
      install_requires=['click', 'findspark',
                        'python-Levenshtein', 'scipy', 'networkx', 'pandas'],
      keywords=['pyspark', 'genomics', 'hpc', 'bioinformatics']
      )
