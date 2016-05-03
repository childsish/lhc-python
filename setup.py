import os

from setuptools import setup

long_description = open('README.rst').read() if os.path.exists('README.rst') else\
    open('README.md').read()

setup(
    name='lhc-python',
    version='1.1.2',
    author='Liam H. Childs',
    author_email='liam.h.childs@gmail.com',
    packages=['lhc'],
    scripts=[],
    url='https://github.com/childsish/lhc-python',
    license='LICENSE.txt',
    description='My python library of classes and functions that help me work',
    long_description=long_description
)
