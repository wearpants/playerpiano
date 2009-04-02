#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='PlayerPiano',
      version='0.02',
      description='PlayerPiano amazes your friends by running Python doctests in a fake interactive shell.',
      author='Peter Fein',
      author_email='pfein@pobox.com',
      url='http://playerpiano.googlecode.com',
      scripts=['bin/playerpiano.py', 'bin/player_rst.py', 'bin/recorderpiano.py'],
      packages=find_packages(),
      install_requires=['pygments'],
       
     )
