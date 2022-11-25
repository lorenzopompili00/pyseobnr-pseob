import numpy as np
from ..fits.EOB_fits import *


def compute_MR_mode_free(
    t, m1, m2, chi1, chi2, attach_params, ell, m, fits_dict,t_match=0, phi_match=0, debug=True
):
    # Step 1 - use the NR fits for amplitude and frequency at attachment time
    chiA = (chi1 - chi2) / 2
    chiS = (chi1 + chi2) / 2
    eta = m1 * m2 / (m1 + m2) ** 2
    chi = 0.5 * (chi1 + chi2) + 0.5 * (chi1 - chi2) * (m1 - m2) / (m1 + m2) / (
        1.0 - 2.0 * eta
    )
    nra = attach_params["amp"]
    nraDot = attach_params["damp"]
    nromega = attach_params["omega"]

    # Step 2 - compute the  QNMs
    final_mass = attach_params["final_mass"]
    final_spin = attach_params["final_spin"]
    omega_complex = compute_QNM(ell, m, 0, final_spin, final_mass).conjugate()
    sigmaR = -np.imag(omega_complex)
    sigmaI = -np.real(omega_complex)
    # Step 3 - use the fits for the free coefficients in the RD anzatse
    c1f = fits_dict['c1f'][(ell,m)]
    c2f = fits_dict['c2f'][(ell,m)]
    # Ensure that the ampitude of the (2,2) mode has a maximum at t_match
    if ell == 2 and m == 2:
        if sigmaR > 2.0 * c1f * np.tanh(c2f):
            c1f = sigmaR / (2.0 * np.tanh(c2f))

    d1f = fits_dict['d1f'][(ell,m)]
    d2f = fits_dict['d2f'][(ell,m)]
    # Step 4 - compute the constrainted coefficients
    c1c = EOBCalculateRDAmplitudeConstraintedCoefficient1(
        c1f, c2f, sigmaR, nra, nraDot, eta
    )
    c2c = EOBCalculateRDAmplitudeConstraintedCoefficient2(
        c1f, c2f, sigmaR, nra, nraDot, eta
    )
    d1c = EOBCalculateRDPhaseConstraintedCoefficient1(d1f, d2f, sigmaI, nromega)



    # Step 5 - assemble the amplitude and phase
    # First the ansatze part
    Alm = c1c * np.tanh(c1f * (t - t_match) + c2f) + c2c
    philm = phi_match - d1c * np.log(
        (1 + d2f * np.exp(-d1f * (t - t_match))) / (1 + d2f)
    )

    test_omega = -np.real(omega_complex) + 1j * np.imag(omega_complex)
    # hlm = eta*Alm*np.exp(1j*philm)*np.exp(1j*omega_complex*(t-t_match))
    hlm = eta * Alm * np.exp(1j * philm) * np.exp(1j * test_omega * (t - t_match))
    return hlm, philm