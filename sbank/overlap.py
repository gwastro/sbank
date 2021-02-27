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
                                  delta_f, workspace_cache)
    else:
        return _SBankComputeRealMatch(inj.data.data, tmplt.data.data, min_len,
                                      delta_f, workspace_cache)

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
                                           workspace_cache1, workspace_cache2)
    else:
        return _SBankComputeMatchMaxSkyLocNoPhase(hp.data.data, hc.data.data, 
                                                  hphccorr, proposal.data.data,
                                                  min_len, hp.delta_f,
                                                  workspace_cache1,
                                                  workspace_cache2)


    




