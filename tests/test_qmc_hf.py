# -*- coding: utf-8 -*-
"""
Created on Tue Nov 25 12:44:23 2014

@author: oscar
"""

from __future__ import division, absolute_import, print_function
import numpy as np
import dmft.hirschfye as hf
import pytest
import hffast


@pytest.mark.parametrize("chempot, u_int", [(0, 2), (0.5, 2.3)])
def test_hf_fast_updatecond(chempot, u_int, beta=16.,
                            n_tau=2**11, n_matsubara=64):
    parms = {'BETA': beta, 'N_TAU': n_tau, 'N_MATSUBARA': n_matsubara,
             'MU': chempot, 'U': u_int, 'dtau_mc': 0.5, 'n_tau_mc':    32, }
    tau, w_n, g0t, __, v = hf.setup_PM_sim(parms)

    g0ttp = hf.ret_weiss(g0t)
    kroneker = np.eye(v.size)

    groot = hf.gnewclean(g0ttp, v, 1, kroneker)
    flip = 5
    v[flip] *= -1

    g_flip = hf.gnewclean(g0ttp, v, 1, kroneker)
    g_fast_flip = hf.gnew(np.copy(groot), v[flip], flip, 1)

    assert np.allclose(g_flip, g_fast_flip)

    g_ffast_flip = hffast.gnew(np.copy(groot), v[flip], flip, 1)
    assert np.allclose(g_flip, g_ffast_flip)
