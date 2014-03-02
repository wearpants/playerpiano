#!/usr/bin/env python

from setuptools import setup, find_packages

with open('VERSION') as version_stream:
    version = version_stream.read().strip()

with open('README.rst') as readme_stream:
    readme = readme_stream.read()

setup(
    name='PlayerPiano',
    version=version,
    description='Amaze your friends by running Python doctests in a fake interactive shell',
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
    long_description=readme,
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Operating System :: POSIX",
        "Topic :: Education :: Computer Aided Instruction (CAI)",
        "Topic :: System :: Shells",
    ],
)
