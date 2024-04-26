# -*- coding: utf-8 -#-
# Copyright (2021) Cardiff University (macleoddm@cardiff.ac.uk)

"""Build configuration for sbank
"""

import os
import subprocess

from setuptools import setup, Extension

import numpy

from Cython.Build import cythonize

__author__ = "Duncan Macleod <duncan.macleod@ligo.org>"

# Ensure we can find lal libraries
def pkgconfig(package, kw):
    flag_map = {'-I': 'include_dirs', '-L': 'library_dirs', '-l': 'libraries'}
    output = subprocess.getoutput(
        'pkg-config --cflags --libs {}'.format(package))
    for token in output.strip().split():
        kw.setdefault(flag_map.get(token[:2]), []).append(token[2:])
    return kw


# define cython options
cython_compile_args = [
    "-O3",
    "-w",
    "-ffast-math",
    "-ffinite-math-only",
    "-std=c99",
]
cython_directives = {
    "embedsignature": True,
    "language_level": 3,
}

# enable coverage for cython
if int(os.getenv("CYTHON_LINETRACE", "0")):
    cython_directives["linetrace"] = True
    cython_compile_args.append("-DCYTHON_TRACE")

# Set extension arguments
extension_kwargs = {
    'include_dirs': [numpy.get_include()],
    'language': "c",
    'libraries': ["lal"],
    'extra_compile_args': cython_compile_args,
    'extra_link_args': [],
}

# lal arguments
extension_kwargs = pkgconfig('lal', extension_kwargs)

# define compiled extensions
exts = [
    Extension(
        "sbank.overlap_cpu",
        ["sbank/overlap_cpu.pyx"],
        **extension_kwargs
    ),
]

# -- build the thing
# this function only manually specifies things that aren't
# supported by setup.cfg (as of setuptools-30.3.0)
setup(
    ext_modules=cythonize(exts, compiler_directives=cython_directives),
)
