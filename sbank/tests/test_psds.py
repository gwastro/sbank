# -*- coding: utf-8 -*-
# Copyright: 2021 Cardiff University

"""Test suite for `sbank.psds`
"""

import pytest

from .. import psds as sbank_psds


@pytest.mark.parametrize("arg, result", (
    (1, 1),
    (3, 4),
    (4, 4),
    (100, 128),
))
def test_next(arg, result):
    assert sbank_psds.next_pow2(arg) == result
