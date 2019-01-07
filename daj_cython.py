from distutils.core import setup
from Cython.Build import cythonize
import os

os.environ['CFLAGS'] = '-O3'
setup(
    ext_modules=cythonize(['engine.pyx'], language_level=3,
                          annotate=True),        # enables generation of the html annotation file
)
