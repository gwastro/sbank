# Copyright (C) 2021 Ian Harry

import cython
cimport numpy

cdef extern from "overlap_cpu_lib.c":
    ctypedef struct WS
    WS *SBankCreateWorkspaceCache()
    void SBankDestroyWorkspaceCache(WS *workspace_cache)
    double _SBankComputeMatch(float complex *inj, float complex *tmplt, size_t min_len, double delta_f, WS *workspace_cache)
    double _SBankComputeRealMatch(float complex *inj, float complex *tmplt, size_t min_len, double delta_f, WS *workspace_cache)
    double _SBankComputeMatchMaxSkyLoc(float complex *hp, float complex *hc, const double hphccorr, float complex *proposal, size_t min_len, double delta_f, WS *workspace_cache1, WS *workspace_cache2)
    double _SBankComputeMatchMaxSkyLocNoPhase(float complex *hp, float complex *hc, const double hphccorr, float complex *proposal, size_t min_len, double delta_f, WS *workspace_cache1, WS *workspace_cache2)


# WARNING: Handling C pointers in python gets nasty. The workspace item is
#          important for sbank's memory management and optimality. It makes
#          sense that we store this *in* python, but it needs to contain
#          actual C memory pointers. I'm not 100% sure I've understood how I've
#          solved this, but I think the main point is to have the structure
#          imported here, and then any function that needs it must use cdef.
#          It's okay to *get* the thing using the cdeffed functions below, but
#          when interacting with the C functions it must be clear what we have
#          and then the cdef interface functions are needed as well.
# https://www.mail-archive.com/cython-dev@codespeak.net/msg06363.html
cdef class SBankWorkspaceCache:
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

# As a reference for sending numpy arrays onto C++
# https://github.com/cython/cython/wiki/tutorials-NumpyPointerToC
# http://docs.cython.org/en/latest/src/userguide/wrapping_CPlusPlus.html
# https://cython.readthedocs.io/en/latest/src/tutorial/numpy.html
# https://stackoverflow.com/questions/21242160/how-to-build-a-cython-wrapper-for-c-function-with-stl-list-parameter

def SBankCythonComputeMatch(
    numpy.ndarray[numpy.complex64_t, ndim=1, mode="c"] inj,
    numpy.ndarray[numpy.complex64_t, ndim=1, mode="c"] tmplt,
    int min_len,
    double delta_f,
    workspace_cache
):
    cdef WS* _workspace
    # So even though workspace_cache is an instance of SBankWorkspaceCache, it
    # seems we still need to call like this. workspace_cache.get_workspace()
    # does not compile as cython is not clear it *is* a SBankWorkspaceCache
    # object.
    _workspace = SBankWorkspaceCache.get_workspace(workspace_cache)
    return _SBankComputeMatch(&inj[0], &tmplt[0], min_len, delta_f,
                              _workspace)

def SBankCythonComputeRealMatch(
    numpy.ndarray[numpy.complex64_t, ndim=1, mode="c"] inj,
    numpy.ndarray[numpy.complex64_t, ndim=1, mode="c"] tmplt,
    int min_len,
    double delta_f,
    workspace_cache
):
    cdef WS* _workspace
    _workspace = SBankWorkspaceCache.get_workspace(workspace_cache)
    return _SBankComputeRealMatch(&inj[0], &tmplt[0], min_len, delta_f,
                                  _workspace)

def SBankCythonComputeMatchMaxSkyLoc(
    numpy.ndarray[numpy.complex64_t, ndim=1, mode="c"] hp,
    numpy.ndarray[numpy.complex64_t, ndim=1, mode="c"] hc,
    double hphccorr,
    numpy.ndarray[numpy.complex64_t, ndim=1, mode="c"] proposal,
    int min_len,
    double delta_f,
    workspace_cache1,
    workspace_cache2
):
    cdef WS* _workspace1
    cdef WS* _workspace2
    _workspace1 = SBankWorkspaceCache.get_workspace(workspace_cache1)
    _workspace2 = SBankWorkspaceCache.get_workspace(workspace_cache2)
    return _SBankComputeMatchMaxSkyLoc(&hp[0], &hc[0], hphccorr, &proposal[0],
                                       min_len, delta_f, _workspace1,
                                       _workspace2)

def SBankCythonComputeMatchMaxSkyLocNoPhase(
    numpy.ndarray[numpy.complex64_t, ndim=1, mode="c"] hp,
    numpy.ndarray[numpy.complex64_t, ndim=1, mode="c"] hc,
    double hphccorr,
    numpy.ndarray[numpy.complex64_t, ndim=1, mode="c"] proposal,
    int min_len,
    double delta_f,
    workspace_cache1,
    workspace_cache2
):
    cdef WS* _workspace1
    cdef WS* _workspace2
    _workspace1 = SBankWorkspaceCache.get_workspace(workspace_cache1)
    _workspace2 = SBankWorkspaceCache.get_workspace(workspace_cache2)
    return _SBankComputeMatchMaxSkyLocNoPhase(&hp[0], &hc[0], hphccorr,
                                              &proposal[0], min_len, delta_f,
                                              _workspace1, _workspace2)
