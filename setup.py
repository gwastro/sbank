# -*- coding: utf-8 -#-
# Copyright (2021) Cardiff University (macleoddm@cardiff.ac.uk)

"""Build configuration for sbank
"""

import re
import numpy
from pathlib import Path

from setuptools import setup, Extension

__author__ = "Duncan Macleod <duncan.macleod@ligo.org>"


def find_version(path, varname="__version__"):
    """Parse the version metadata in the given file.
    """
    with Path(path).open('r') as fobj:
        version_file = fobj.read()
    version_match = re.search(
        r"^{0} = ['\"]([^'\"]*)['\"]".format(varname),
        version_file,
        re.M,
    )
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


exts = []
cython_compile_args = ['-O3', '-w', '-ffast-math',
                       '-ffinite-math-only']

ext = Extension("sbank.overlap_cpu",
                ["sbank/overlap_cpu.pyx"],
                include_dirs=[numpy.get_include(), "sbank"],
                language='c',
                libraries=['lal'],
                extra_compile_args=cython_compile_args,
                extra_link_args=[],
                compiler_directives={'embedsignature': True})
exts.append(ext)

# this function only manually specifies things that aren't
# supported by setup.cfg (as of setuptools-30.3.0)
setup(
    version=find_version(Path('sbank') / "__init__.py"),
    ext_modules=exts,
)
