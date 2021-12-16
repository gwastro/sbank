[![PyPI version](https://badge.fury.io/py/sbank.svg)](http://badge.fury.io/py/sbank)
[![Conda version](https://img.shields.io/conda/vn/conda-forge/sbank.svg)](https://anaconda.org/conda-forge/sbank/)
[![License](https://img.shields.io/pypi/l/sbank.svg)](https://choosealicense.com/licenses/gpl-2.0/)
![Supported Python versions](https://img.shields.io/pypi/pyversions/sbank.svg)

[![Build status](https://github.com/gwastro/sbank/actions/workflows/build.yml/badge.svg?branch=master)](https://github.com/gwastro/sbank/actions/workflows/build.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/1488c7bc13b82b49661d/maintainability)](https://codeclimate.com/github/gwastro/sbank/maintainability)
[![Coverage status](https://codecov.io/gh/gwastro/sbank/branch/master/graph/badge.svg)](https://codecov.io/gh/gwastro/sbank)

Sbank is a library for generating a template bank for compact binary searches
covering a given region of mass and spin parameter space.
The program can support all waveform approximants available in the
lalsimulation suite. Currently implemented waveforms can be found with
`sbank --help` and others added with only minor additions.

Sbank has been developed collaboratively by a diverse group of LIGO scientists
starting in 2012, and has been split off from the larger `lalsuite` package as
a standalone module in 2021.
Sbank has been used to generate template banks for the separate GstLAL, MBTA,
PyCBC and SPIIR analysis codes.
Sbank also offers support for generating precessing and/or higher-order mode
template banks.

The source code is open-source on GitHub and we welcome contributions from
anyone.

If you use sbank in scientific publication, please see our citation guidelines
(which Ian will have to write, for now the PyCBC help page
<https://pycbc.org/pycbc/latest/html/tmpltbank.html#tmpltbank-alignedstochbank>
contains the important details).

![Structure of sbank](./tools/sbank_structure_ini.svg?raw=true "Structure of sbank")

"Structure of sbank" image courtesy of Han Wang, Sun Yat-sen University.

