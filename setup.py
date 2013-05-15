from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

import os


ext_modules = []
for item in ['src/calculations.pyx']:
    ext_modules.append(Extension(os.path.basename(item)[:-4], [item]))

setup(
  name = 'zwilletree',
  cmdclass = {'build_ext': build_ext},
  ext_modules = ext_modules
)
