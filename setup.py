import os

from setuptools import setup, find_namespace_packages, Extension


bitap_extension = Extension(
    'lhc.misc.bitap',
    ['lib/bitap/bitapmodule.cpp', 'lib/bitap/bitap.cpp'],
    include_dirs=['./lib/bitap'])

digen_extension = Extension(
    'lhc.misc.digen',
    ['lib/digen/digenmodule.cpp', 'lib/digen/digen.cpp'],
    include_dirs=['./lib/digen'])

setup(
    ext_modules=[digen_extension, bitap_extension],
)
