"""
This file was automatically generated by polynomial_fit_v4.py on 2022-09-01 18:37:25.690079
running at revision 159a400f4d78ddb6f88aa7bd43c2d31289a3a4ae.
The posterior data used was spinning_pst_handcut.h5 with md5sum: 3cc8d7aab62dbfbb451f57548b6d1522

The RMSE was [37.02442072  2.49453561]

The TPL residuals were [-16.73657386 -12.40339386   1.35879203  -3.05734409]

The settings used:

input_physical_parameters = [ "q", "chi1", "chi2",]
reduction = "median"
input_transformations = "ETA_CHIEFF_CHIA"
calibration_parameters = [ "dSO", "NR_deltaT",]
calibration_labels = [ "$\\Delta t_{22}$", "$d_\\mathrm{SO}$",]
force_independent = false
TPL_rescaling = true
k = 0
fitk = false
hierarchical = true
hierarchical_function = "dt22_non_spinning_fit"
weight_function = "seobnrv4"
regularize = false
alpha = 0.8
lambda = 0.3
solver = "SLSQP"
n_restarts = 512

[feature_map]
x0 = "nu"
x1 = "ap"
x2 = "am"

[feature_array]
dSO = [ "1", "x0", "x0*x0", "x0*x0*x0", "x0*x0*x1", "x0*x0*x2", "x0*x1", "x0*x1*x1", "x0*x1*x2", "x0*x2", "x0*x2*x2", "x1", "x1*x1", "x1*x1*x1", "x1*x1*x2", "x1*x2", "x1*x2*x2", "x2", "x2*x2", "x2*x2*x2",]
NR_deltaT = [ "x0*x0*x1", "x0*x0*x2", "x0*x1", "x0*x1*x1", "x0*x1*x2", "x0*x2", "x0*x2*x2", "x1", "x1*x1", "x1*x1*x1", "x1*x1*x2", "x1*x2", "x1*x2*x2", "x2", "x2*x2", "x1*x1*x1*x1",]

[extra_physical_info]
TPL = false
additional_terms = "spinning_TPL_info"
additional_terms_weight = 25.0

"""

import numpy as np
from numba import jit


@jit(nopython=True)
def dSO(nu, ap, am):
    return (
        -7.71251231383957 * am ** 3
        - 17.2294679794015 * am ** 2 * ap
        - 238.430383378296 * am ** 2 * nu
        + 69.5461667822545 * am ** 2
        - 10.5225438990315 * am * ap ** 2
        + 362.767393298729 * am * ap * nu
        - 85.8036338010274 * am * ap
        - 1254.66845939312 * am * nu ** 2
        + 472.431937787377 * am * nu
        - 39.742317057316 * am
        - 7.58458103577458 * ap ** 3
        - 42.7601129678844 * ap ** 2 * nu
        + 18.1783435552183 * ap ** 2
        - 201.905934468847 * ap * nu ** 2
        - 90.5790079104259 * ap * nu
        + 49.6299175121658 * ap
        + 478.546231305475 * nu ** 3
        + 679.521769948995 * nu ** 2
        - 177.334831768076 * nu
        - 37.6897780220529
    )


@jit(nopython=True)
def NR_deltaT(nu, ap, am):
    return nu ** (-1.0 / 5 + 0 * nu) * (
        8.39238879807543 * am ** 2 * ap
        - 16.9056858928167 * am ** 2 * nu
        + 7.23410583477034 * am ** 2
        + 6.38975598319936 * am * ap ** 2
        + 179.569824846781 * am * ap * nu
        - 40.6063653476775 * am * ap
        + 144.253395844761 * am * nu ** 2
        - 90.1929138487509 * am * nu
        + 14.2203101910927 * am
        - 6.78913884987037 * ap ** 4
        + 5.39962303470497 * ap ** 3
        - 132.224950777226 * ap ** 2 * nu
        + 49.8016443361381 * ap ** 2
        + 384.201018794943 * ap * nu ** 2
        - 141.253181790353 * ap * nu
        + 17.5710132409988 * ap
    )


"""
Non-spinning functions obtained by a least-square fit of the maxL of the calibraton posteriors

The NR_deltaT is done hierarchically, and one needs to add the non-spinning and spinning contributions
NR_deltaT = NR_deltaT_NS(nu) +  NR_deltaT(nu, ap, am)
"""


@jit(nopython=True)
def a6_NS(nu):
    par = np.array(
        [4.17877875e01, -3.02193382e03, 3.34144394e04, -1.69019140e05, 3.29523262e05]
    )
    return par[0] + par[1] * nu + par[2] * nu ** 2 + par[3] * nu ** 3 + par[4] * nu ** 4


@jit(nopython=True)
def NR_deltaT_NS(nu):
    par = np.array(
        [1.00513217e01, -5.96231800e01, -1.05687385e03, -9.79317619e03, 5.55652392e04]
    )
    return nu ** (-1.0 / 5 + par[0] * nu) * (
        par[1] + par[2] * nu + par[3] * nu ** 2 + par[4] * nu ** 3
    )
