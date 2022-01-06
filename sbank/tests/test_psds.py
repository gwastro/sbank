# -*- coding: utf-8 -*-
# Copyright: 2021 Cardiff University

"""Test suite for `sbank.psds`
"""

import pytest

from .. import psds as sbank_psds

LIGO_LW_ARRAY = """<?xml version='1.0' encoding='utf-8'?>
<!DOCTYPE LIGO_LW SYSTEM "http://ldas-sw.ligo.caltech.edu/doc/ligolwAPI/html/ligolw_dtd.txt">
<LIGO_LW Name="psd">
  <LIGO_LW Name="REAL8FrequencySeries">
    <Time Type="GPS" Name="epoch">0</Time>
    <Param Name="f0:param" Type="real_8" Unit="s^-1">0</Param>
    <Array Type="real_8" Name="aLIGOZeroDetHighPower:array" Unit="s">
      <Dim Name="Frequency" Unit="s^-1" Start="0" Scale="1">11</Dim>
      <Dim Name="Frequency,Real">2</Dim>
      <Stream Type="Local" Delimiter=" ">
        0 0
        1 5.870471766089542e-40
        2 1.962088320602432e-41
        3 2.751143271999274e-42
        4 6.92354999020744e-43
        5 2.39732692753636e-43
        6 1.014780466036667e-43
        7 4.931072304135098e-44
        8 2.649571891648038e-44
        9 1.536838230224327e-44
        10 9.466734353467912e-45
      </Stream>
    </Array>
    <Param Name="instrument:param" Type="lstring">H1</Param>
  </LIGO_LW>
  <LIGO_LW Name="REAL8FrequencySeries">
    <Time Type="GPS" Name="epoch">0</Time>
    <Param Name="f0:param" Type="real_8" Unit="s^-1">0</Param>
    <Array Type="real_8" Name="aLIGOZeroDetHighPower:array" Unit="s">
      <Dim Name="Frequency" Unit="s^-1" Start="0" Scale="1">11</Dim>
      <Dim Name="Frequency,Real">2</Dim>
      <Stream Type="Local" Delimiter=" ">
        0 0
        1 5.870471766089542e-40
        2 1.962088320602432e-41
        3 2.751143271999274e-42
        4 6.92354999020744e-43
        5 2.39732692753636e-43
        6 1.014780466036667e-43
        7 4.931072304135098e-44
        8 2.649571891648038e-44
        9 1.536838230224327e-44
        10 9.466734353467912e-45
      </Stream>
    </Array>
    <Param Name="instrument:param" Type="lstring">L1</Param>
  </LIGO_LW>
</LIGO_LW>
"""  # noqa: E501


@pytest.mark.parametrize("arg, result", (
    (1, 1),
    (3, 4),
    (4, 4),
    (100, 128),
))
def test_next(arg, result):
    assert sbank_psds.next_pow2(arg) == result


def test_read_psds(tmp_path):
    llwf = tmp_path / "test.xml"
    llwf.write_text(LIGO_LW_ARRAY)
    psd = sbank_psds.read_psd(llwf)
    for ifo in ("H1", "L1"):
        assert psd[ifo].data.data.size == 11
