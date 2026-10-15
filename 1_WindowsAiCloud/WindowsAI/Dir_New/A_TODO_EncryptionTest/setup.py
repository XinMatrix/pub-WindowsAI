from distutils.core import setup
from Cython.Build import cythonize

setup(
    name='WindowsAi',
    ext_modules=cythonize("config.py")
)
