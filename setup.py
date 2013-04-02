#!/usr/bin/env python

from setuptools import setup, find_packages

# this horrible mess brought to you by the crap that is Python distutils. Just use CPAN.
import os.path
version_file = os.path.join(os.path.dirname(__file__), 'VERSION')
VERSION = open(version_file).read().strip().split('.')
release = '.'.join(VERSION)

setup(name='PlayerPiano',
      version=release,
      description='Amazes your friends by running Python doctests in a fake interactive shell.',
      author='Peter Fein',
      author_email='pete@wearpants.org',
      url='https://github.com/wearpants/playerpiano',
      entry_points = {
          'console_scripts': [
              'playerpiano=playerpiano.piano:main',
              'recorderpiano=playerpiano.recorder:main',
          ]},
      packages=find_packages(),
      include_package_data = True,
      install_requires=['pygments'],
      license="BSD",
      long_description=open("README.rst").read(),
      classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Operating System :: POSIX",
        "Topic :: Education :: Computer Aided Instruction (CAI)",
        "Topic :: System :: Shells",
        ],
)
