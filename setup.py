# -*- coding: utf-8 -*-
"""setup -- setuptools setup file for Thomas-aquinas.

$Author: shackra $
$Rev: 1 $
$Date: 2012-05-12 02:55:00 -0600 (Sun, 12 March 2013) $
"""

__author__ = "Invensible Studios"
__author_email__ = "jorgean@lavabit.com"
__version__ = "0.0.1"
__date__ = "2013 05 12"

try:
    import setuptools
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()

from setuptools import setup, find_packages

with open("README", 'rU') as f:
    long_description = f.read()

setup(
    name = "thomas-aquinas",
    version = __version__,
    author = "Invensible Studios",
    license="GPL3+",
    description = "a 2D framework for games and multimedia. Based on Cocos2D",
    long_description=long_description,
    url = "http://www.ohloh.net/p/thomas-aquinas",
    download_url = "https://bitbucket.org/shackra/thomas-aquinas/downloads"
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Environment :: MacOS X",
        "Environment :: Win32 (MS Windows)",
        "Environment :: X11 Applications",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Natural Language :: Spanish"
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        ("Topic :: Software Development :: Libraries :: Python Modules"),
        ("Topic :: Games/Entertainment"),
    ],

    packages = find_packages(),
    package_data={'summa': ['resources/*']},

    install_requires=['pyglet>=1.1.4',],
    dependency_links=['http://code.google.com/p/pyglet/downloads/list',],

    include_package_data = True,
    zip_safe = False,
)
