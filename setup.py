#!/usr/bin/env python

from setuptools import setup

setup(name='PlayerPiano',
      version='0.01',
      description='PlayerPiano amazes your friends by running Python doctests in a fake interactive shell.',
      author='Peter Fein',
      author_email='pfein@pobox.com',
      url='http://playerpiano.googlecode.com',
      scripts=['playerpiano.py'],
      install_requires=['orbited', 'stompservice', 'twisted'],
     )
