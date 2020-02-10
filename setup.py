import os

from subprocess import Popen, PIPE
from setuptools import setup, find_packages, Extension


extension_mod = Extension(
    'lhc.misc.bitap',
    ['lib/bitap/bitapmodule.cpp', 'lib/bitap/bitap.cpp'],
    include_dirs=['lib/bitap'])

with open('README.rst', encoding='utf-8') if os.path.exists('README.rst') else \
        open('README.md', encoding='utf-8') as fileobj:
    long_description = fileobj.read()

prc = Popen(['git', 'describe', '--tags'],
            stdout=PIPE,
            cwd=os.path.dirname(os.path.realpath(__file__)))
version, _ = prc.communicate()

setup(
    name='lhc-python',
    version=version.decode(encoding='utf-8').strip(),
    author='Liam H. Childs',
    author_email='liam.h.childs@gmail.com',
    packages=find_packages(exclude=['docs', 'test*']),
    scripts=[],
    url='https://github.com/childsish/lhc-python',
    license='LICENSE.txt',
    description='My python library of classes and functions that help me work',
    long_description=long_description,
    install_requires=['sortedcontainers == 2.1.0', 'numpy == 1.17', 'pysam == 0.15.4'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics'],
    ext_modules=[extension_mod]
)
