# Copyright (C) 2021 Ian Harry

# There is an overlap_cuda.py module, but that's never been hooked up
# So we just hook up the CPU module in all cases. We could add switches here
# to use the GPU if needed (although it will likely be more complicated than
# that if the waveforms were not generated on the GPU)

from .overlap_cpu import SBankCythonComputeMatch
from .overlap_cpu import SBankCythonComputeRealMatch
from .overlap_cpu import SBankCythonComputeMatchMaxSkyLoc
from .overlap_cpu import SBankCythonComputeMatchMaxSkyLocNoPhase
from .overlap_cpu import SBankWorkspaceCache as CPUWorkspaceCache

# If considering enabling the GPU code, need to switch this as well.
# Currently the GPU WorkspaceCache will not work and would need some fixing.
SBankWorkspaceCache = CPUWorkspaceCache


def SBankComputeMatch(inj, tmplt, workspace_cache, phase_maximized=True):
    """
    ADD ME
    """
    min_len = tmplt.data.length
    if inj.data.length <= tmplt.data.length:
        min_len = inj.data.length
    else:
        min_len = tmplt.data.length
    assert(inj.deltaF == tmplt.deltaF)
    delta_f = inj.deltaF
    if phase_maximized:
        return SBankCythonComputeMatch(inj.data.data, tmplt.data.data, min_len,
                                       delta_f, workspace_cache)
    else:
        return SBankCythonComputeRealMatch(inj.data.data, tmplt.data.data,
                                           min_len, delta_f, workspace_cache)


def SBankComputeMatchSkyLoc(hp, hc, hphccorr, proposal, workspace_cache1,
                            workspace_cache2, phase_maximized=False):
    """
    ADD ME
    """
    assert(hp.deltaF == proposal.deltaF)
    assert(hc.deltaF == proposal.deltaF)
    assert(hp.data.length == hc.data.length)
    if proposal.data.length <= hp.data.length:
        min_len = proposal.data.length
    else:
        min_len = hp.data.length
    if phase_maximized:
        return SBankCythonComputeMatchMaxSkyLoc(hp.data.data, hc.data.data,
                                                hphccorr, proposal.data.data,
                                                min_len, hp.deltaF,
                                                workspace_cache1,
                                                workspace_cache2)
    else:
        return SBankCythonComputeMatchMaxSkyLocNoPhase(
            hp.data.data,
            hc.data.data,
            hphccorr,
            proposal.data.data,
            min_len,
            hp.deltaF,
            workspace_cache1,
            workspace_cache2
        )
