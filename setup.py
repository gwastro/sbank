# -*- coding: utf-8 -#-
# Copyright (2021) Cardiff University (macleoddm@cardiff.ac.uk)

"""Build configuration for sbank
"""

import os
import re
from pathlib import Path

from setuptools import setup, Extension

import numpy

from Cython.Build import cythonize

__author__ = "Duncan Macleod <duncan.macleod@ligo.org>"


def find_version(path, varname="__version__"):
    """Parse the version metadata in the given file.
    """
    with Path(path).open("r") as fobj:
        version_file = fobj.read()
    version_match = re.search(
        r"^{0} = ['\"]([^'\"]*)['\"]".format(varname),
        version_file,
        re.M,
    )
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


# define cython options
cython_compile_args = [
    "-O3",
    "-w",
    "-ffast-math",
    "-ffinite-math-only",
]
cython_directives = {
    "embedsignature": True,
    "language_level": 3,
}

# enable coverage for cython
if int(os.getenv("CYTHON_LINETRACE", "0")):
    cython_directives["linetrace"] = True
    cython_compile_args.append("-DCYTHON_TRACE")

# define compiled extensions
exts = [
    Extension(
        "sbank.overlap_cpu",
        ["sbank/overlap_cpu.pyx"],
        include_dirs=[numpy.get_include()],
        language="c",
        libraries=["lal"],
        extra_compile_args=cython_compile_args,
        extra_link_args=[],
    ),
]

# -- build the thing
# this function only manually specifies things that aren't
# supported by setup.cfg (as of setuptools-30.3.0)
setup(
    version=find_version(Path("sbank") / "__init__.py"),
    ext_modules=cythonize(exts, compiler_directives=cython_directives),
)
