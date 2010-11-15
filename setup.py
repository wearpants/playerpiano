#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='PlayerPiano',
      version='0.1',
      description='PlayerPiano amazes your friends by running Python doctests in a fake interactive shell.',
      author='Peter Fein',
      author_email='pfein@pobox.com',
      url='http://playerpiano.googlecode.com',
      entry_points = {
          'console_scripts': [
              'playerpiano=playerpiano.piano:main',
              'recorderpiano=playerpiano.recorder:main',
          ]},
      packages=find_packages(),
      include_package_data = True,
      install_requires=['pygments'],
     )
