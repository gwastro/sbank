# Copyright (C) 2021 Ian Harry

import cython

cdef extern from "overlap_lib.c":
    ctypedef struct WS
    WS *SBankCreateWorkspaceCache()
    void SBankDestroyWorkspaceCache(WS *workspace_cache)
    double _SBankComputeMatch(double complex *inj, double complex *tmplt, size_t min_len, double delta_f, WS *workspace_cache)
    double _SBankComputeRealMatch(double complex *inj, double complex *tmplt, size_t min_len, double delta_f, WS *workspace_cache)
    double _SBankComputeMatchMaxSkyLoc(double complex *hp, double complex *hc, const double hphccorr, double complex *proposal, size_t min_len, double delta_f, WS *workspace_cache1, WS *workspace_cache2)
    double _SBankComputeMatchMaxSkyLocNoPhase(double complex *hp, double complex *hc, const double hphccorr, double complex *proposal, size_t min_len, double delta_f, WS *workspace_cache1, WS *workspace_cache2)


# https://www.mail-archive.com/cython-dev@codespeak.net/msg06363.html
cdef class SbankWorkspaceCache:
    cdef WS *workspace

    def __cinit__(self):
        self.workspace = self.__create()
        
    def __dealloc__(self):
        if self.workspace != NULL:
            SBankDestroyWorkspaceCache(self.workspace)

    cdef WS* __create(self):
        cdef WS *temp
        temp = SBankCreateWorkspaceCache()
        return temp

    cdef WS* get_workspace(self):
        return self.workspace

