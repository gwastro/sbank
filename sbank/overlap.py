# There is an overlap_cuda.py module, but that's never been hooked up
# So we just hook up the CPU module in all cases. We could add switches here
# to use the GPU if needed (although it will likely be more complicated than
# that if the waveforms were not generated on the GPU)

from .overlap_cpu import _SBankComputeMatch, _SBankComputeRealMatch
from .overlap_cpu import _SBankComputeMatchMaxSkyLoc
from .overlap_cpu import _SBankComputeMatchMaxSkyLocNoPhase
from .overlap_cpu import SbankWorkspaceCache as CPUWorkspaceCache

# If considering enabling the GPU code, need to switch this as well.
# Currently the GPU WorkspaceCache will not work and would need some fixing.
SbankWorkspaceCache = CPUWorkspaceCache

def SBankComputeMatch(inj, tmplt, workspace_cache, phase_maximized=True):
    """
    ADD ME
    """
    min_len = tmplt.data.length
    if inj.data.length <= tmplt.data.length:
        min_len = inj.data.length
    else:
        min_len = tmplt.data.length
    assert(inj.delta_f == tmplt.delta_f)
    delta_f = inj.delta_f
    if phase_maximized:
        return _SBankComputeMatch(inj.data.data, tmplt.data.data, min_len,
                                  delta_f, workspace_cache.get_workspace())
    else:
        return _SBankComputeRealMatch(inj.data.data, tmplt.data.data, min_len,
                                      delta_f, workspace_cache.get_workspace())

def SbankComputeMatchSkyLoc(hp, hc, hphccorr, proposal, workspace_cache1,
                            workspace_cache2, phase_maximized=False):
    """
    ADD ME
    """
    assert(hp.delta_f == proposal.delta_f)
    assert(hc.delta_f == proposal.delta_f)
    assert(hp.data.length == hc.data.length)
    if proposal.data.length <= hp.data.length:
        min_len = proposal.data.length
    else:
        min_len = hp.data.length
    if phase_maximized:
        return _SBankComputeMatchMaxSkyLoc(hp.data.data, hc.data.data,
                                           hphccorr, proposal.data.data,
                                           min_len, hp.delta_f,
                                           workspace_cache1.get_workspace(),
                                           workspace_cache2.get_workspace())
    else:
        ws1 = workspace_cache1.get_workspace()
        ws2 = workspace_cache2.get_workspace()
        return _SBankComputeMatchMaxSkyLocNoPhase(hp.data.data, hc.data.data, 
                                                  hphccorr, proposal.data.data,
                                                  min_len, hp.delta_f,
                                                  ws1, ws2)

