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

with open('README.rst', encoding='utf-8') if os.path.exists('README.rst') else \
        open('README.md', encoding='utf-8') as fileobj:
    long_description = fileobj.read()

setup(
    long_description=long_description,
    long_description_content_type='text/markdown',
    ext_modules=[digen_extension, bitap_extension],
)
