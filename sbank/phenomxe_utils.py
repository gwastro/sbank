# Copyright (C) 2012  Alex Nitz
#
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.


#
# =============================================================================
#
#                                   Preamble
#
# =============================================================================
#
import numpy as np

import lal, lalsimulation
from scipy.interpolate import Rbf, InterpolatedUnivariateSpline

# import time
# from pycbc.psd.analytical import aLIGOZeroDetHighPower, aLIGOZeroDetHighPowerGWINC
from scipy.interpolate import Rbf, InterpolatedUnivariateSpline

from scipy.signal import argrelextrema

from pycbc.types import TimeSeries,FrequencySeries

LALMTSUNSI= 4.925491025543575903411922162094833998e-6
#(* Subscript[M, \[CircleDot]][s] = G/c^3Subscript[M, \[CircleDot]][kg] ~ 4.93 10^-6s is the geometrized solar mass in seconds. [LAL_MTSUN_SI] defined in  lal/src/std/LALConstants.h *)
LALCSI=299792458.0 # (* LAL_C_SI 299792458e0 /**< Speed of light in vacuo, m s^-1 *)
LALPCSI = 3.085677581491367e16 # (*  LAL_PC_SI 3.085677581491367278913937957796471611e16 /**< Parsec, m * *)

def AmpPhysicaltoNR(ampphysical, M, dMpc):
    return ampphysical*dMpc*1000000*LALPCSI/(LALCSI*( M*LALMTSUNSI)**2)

def AmpPhysicaltoNR(ampphysical, M, dMpc):
    return ampphysical*dMpc*1000000*LALPCSI/(LALCSI*( M*LALMTSUNSI)**2)

def AmpNRtoPhysical(ampNR, M, dMpc):
    return ampNR*(LALCSI*(M*LALMTSUNSI)**2)/(1000000*LALPCSI*dMpc)

def AmpPhysicaltoNRTD(ampphysical, M, dMpc):
    return ampphysical*dMpc*1000000*LALPCSI/(LALCSI*(M*LALMTSUNSI))


def SectotimeM(seconds, M):
    return seconds/(M*lal.MTSUN_SI)

def timeMtoSec(timeM, M):
    return timeM*M*lal.MTSUN_SI

def compute_freqInterp(time, hlm):

    philm=np.unwrap(np.angle(hlm))

    intrp = InterpolatedUnivariateSpline(time,philm)
    omegalm = intrp.derivative()(time)
    return omegalm

def MftoHz(Mf,M):
    return Mf/(M*lal.MTSUN_SI)

def HztoMf(Hz,M):
    return Hz*(M*lal.MTSUN_SI)

def SectotimeM(seconds, M):
    return seconds/(M*LALMTSUNSI)

def compute_chiEff(q,Mtot, chi1,chi2):

    m1 = q/(1.+q)*Mtot
    m2 = 1./(1.+q)*Mtot

    return (m1*chi1+m2*chi2)/(m1+m2)

def eNewtEstimate(f,fRef,eRef):
    return eRef*(f/fRef)**(-19.0/18.0)


def get_h22_jn2nm2(m1, m2, chi1,chi2,dMpc, f_min, f_max, deltaF, phiRef, f_ref, e0,l0, approximant):

    distance = dMpc*1.0e6*lal.PC_SI
    mtotal = m1+m2
    m1SI = m1*lal.MSUN_SI
    m2SI = m2*lal.MSUN_SI

    Nharmonic = 1
    kAdvance = 1
    LAL_params_template = lal.CreateDict()
    lalsimulation.SimInspiralWaveformParamsInsertPhenomXENHarmonics(LAL_params_template, Nharmonic)
    lalsimulation.SimInspiralWaveformParamsInsertPhenomXEPeriastronAdvance(LAL_params_template, kAdvance)

    if approximant == "IMRPhenomXAS":
        h22 = lalsimulation.SimIMRPhenomXASGenerateFD(m1SI, m2SI, chi1,chi2,distance, f_min, f_max, deltaF,
                                                phiRef, f_ref, LAL_params_template)
    else:
        h22 = lalsimulation.SimIMRPhenomXEv1_opt_GenerateFD(m1SI, m2SI, chi1,chi2,distance, f_min, f_max, deltaF,
                                                    phiRef, f_ref, e0,l0, LAL_params_template)

    h22_0 = AmpPhysicaltoNR(h22.data.data, mtotal, dMpc)
    h22_fd = FrequencySeries(h22_0, delta_f = deltaF)

    freq = HztoMf(h22_fd.get_sample_frequencies().data,mtotal)
    amp22 = np.abs(h22_fd.data)
    phase22 = np.unwrap(np.angle(h22_fd.data))
    iphase22 = InterpolatedUnivariateSpline(freq,phase22)
    dph22df = iphase22.derivative()(freq)

    return freq, h22_fd.data, amp22,phase22, dph22df

def AmpPhysicaltoNR(ampphysical, M, dMpc):
    return ampphysical*dMpc*1000000*LALPCSI/(LALCSI*( M*LALMTSUNSI)**2)

# def get_XE_chirptime_all(m1, m2, chi1,chi2,dMpc, f_min, f_max, deltaF, phiRef, f_ref, e0,l0,approximant):
#
#     distance = dMpc*1.0e6*lal.PC_SI
#     mtotal = m1+m2
#     m1SI = m1*lal.MSUN_SI
#     m2SI = m2*lal.MSUN_SI
#     Mtot_sec = mtotal*lal.MTSUN_SI
#     # Convert starting frequency to Mf
#     Mfmin = f_min*Mtot_sec
#
#     f_minwf = 0.98*f_min #Offset in fmin, to not have problems later with the derivative at fmin
#
#     # Peak frequency based on PhenomD estimate
#     Mfpeak = lalsimulation.IMRPhenomDGetPeakFreq(m1,m2,chi1,chi2)*Mtot_sec
#
#     LAL_params_template = lal.CreateDict()
#     Nharmonic=1
#     kAdvance=1
#     lalsimulation.SimInspiralWaveformParamsInsertPhenomXENHarmonics(LAL_params_template, Nharmonic)
#     lalsimulation.SimInspiralWaveformParamsInsertPhenomXEPeriastronAdvance(LAL_params_template, kAdvance)
#
#     if approximant == "IMRPhenomXAS":
#         h22 = lalsimulation.SimIMRPhenomXASGenerateFD(m1SI, m2SI, chi1,chi2,distance, f_minwf, f_max, deltaF,
#                                                 phiRef, f_ref, LAL_params_template)
#     else:
#         h22 = lalsimulation.SimIMRPhenomXEv1_opt_GenerateFD(m1SI, m2SI, chi1,chi2,distance, f_minwf, f_max, deltaF,
#                                                     phiRef, f_ref, e0,l0, LAL_params_template)
#
#
#     h22_py = FrequencySeries(h22.data.data, delta_f = deltaF)
#
#     h22_NR = AmpPhysicaltoNR(h22.data.data, mtotal, dMpc)
#
#     Mfreq = h22_py.get_sample_frequencies()*Mtot_sec
#
#     #Mfreq = freq*(mtotal*lal.MTSUN_SI)
#     #print(Mfreq)
#     #amp22 = np.abs(h22_NR)
#     phase22 = np.unwrap(np.angle(h22_NR))
#     iphase22 = InterpolatedUnivariateSpline(Mfreq,phase22)
#
#
#     idph22df_Mfmin = iphase22.derivative()(Mfmin)
#     idph22df_Mfpeak = iphase22.derivative()(Mfpeak)
#
# #     print(f"Mfmin = {Mfmin}, idph22df_Mfmin = {idph22df_Mfmin}")
# #     print(f"Mfpeak = {Mfpeak}, idph22df_Mfpeak = {idph22df_Mfpeak}")
#     t_corr = np.abs(idph22df_Mfpeak/(2.*np.pi)-idph22df_Mfmin/(2*np.pi)) #positive time spent from f_min to f_peak
#
#     t_corr_s = t_corr*Mtot_sec
#
#     print("Estimated time = {} M ".format(t_corr))
#     print("Estimated time = {} s ".format(t_corr_s))
#
#     t_corr_D_s = lalsimulation.SimIMRPhenomDChirpTime(m1SI,m2SI,chi1,chi2,f_min)
#     t_corr_D = t_corr_D_s/Mtot_sec
#
#     print("Estimated time phenomD = {} M ".format(t_corr_D))
#     print("Estimated time phenomD = {} s ".format(t_corr_D_s))
#
#     return t_corr,t_corr_s,Mfreq, phase22




def get_XE_chirptime(m1, m2, chi1, chi2, e0, l0, f_ref, f_min, f_max=1024., deltaF=1./128., phiRef=0, approximant='IMRPhenomXEv1'):

    distance = 1.0e9*lal.PC_SI
    mtotal = m1+m2
    m1SI = m1*lal.MSUN_SI
    m2SI = m2*lal.MSUN_SI
    Mtot_sec = mtotal*lal.MTSUN_SI
    # Convert starting frequency to Mf
    Mfmin = f_min*Mtot_sec

    f_minwf = 0.98*f_min #Offset in fmin, to not have problems later with the derivative at fmin

    # Peak frequency based on PhenomD estimate
    Mfpeak = lalsimulation.IMRPhenomDGetPeakFreq(m1,m2,chi1,chi2)*Mtot_sec

    LAL_params_template = lal.CreateDict()
    Nharmonic=1
    kAdvance=1
    lalsimulation.SimInspiralWaveformParamsInsertPhenomXENHarmonics(LAL_params_template, Nharmonic)
    lalsimulation.SimInspiralWaveformParamsInsertPhenomXEPeriastronAdvance(LAL_params_template, kAdvance)

    if approximant == "IMRPhenomXAS":
        h22 = lalsimulation.SimIMRPhenomXASGenerateFD(m1SI, m2SI, chi1,chi2,distance, f_minwf, f_max, deltaF,
                                                phiRef, f_ref, LAL_params_template)
    else:
        h22 = lalsimulation.SimIMRPhenomXEv1_opt_GenerateFD(m1SI, m2SI, chi1,chi2,distance, f_minwf, f_max, deltaF,
                                                    phiRef, f_ref, e0,l0, LAL_params_template)


    h22_py = FrequencySeries(h22.data.data, delta_f = deltaF)
    Mfreq = h22_py.get_sample_frequencies()*Mtot_sec

    h22_NR = AmpPhysicaltoNR(h22.data.data, mtotal, dMpc)
    phase22 = np.unwrap(np.angle(h22_NR))
    iphase22 = InterpolatedUnivariateSpline(Mfreq,phase22)


    idph22df_Mfmin = iphase22.derivative()(Mfmin)
    idph22df_Mfpeak = iphase22.derivative()(Mfpeak)

    t_corr = np.abs(idph22df_Mfpeak/(2.*np.pi)-idph22df_Mfmin/(2*np.pi)) #positive time spent from f_min to f_peak

    t_corr_s = t_corr*Mtot_sec

    return t_corr_s
