import numpy as np
import pandas as pd

def rho(P, eP, a_Rs, ea_Rs, Mp, eMp, Rs, eRs):
    """Stellar density and its error from the Third Kepler (and optionally Stefan-Boltzmann) laws

    Args:
        P (float): Orbital period in days.
        a_Rs (float): Ratio semimajor axis and stellar radius, unitless.
        Mp (float): Planetary mass in earth units.
        Rs (float): Stellar radius in solar units.

    Returns:
        float: Stellar density in solar units.
        float: Stellar density error in solar units.

    Nominal solar values from the IAU B.3 resolution
    on recommended nominal conversion constants for selected solar and planetary properties:
    https://www.iau.org/static/resolutions/IAU2015_English.pdf

    Nominal solar luminosity: Lsun = 3.828 x 10+26 W (exact)
    Nominal solar radius: Rsun = 6.957 x 10+8 m (exact)
    Astronomical unit: au = 149597870700 m (exact)
    Mass of the Earth: Mt = 5.9722(6) x 10+24 kg

    Other physical constants from 2018 CODATA recommended values:
    https://physics.nist.gov/cuu/pdf/wall_2018.pdf

    Stefan-Boltzman constant, sigma = 5.670 374 419 x 10-8 W m-2 K-4 (exact)
    Newtonian constant of gravitation, G = 6.674 30(15) x 10-11 m3 kg-1 s-2

    """
    # Constants
    Lsun = 3.828*1e+26
    Rsun = 6.957*1e+8
    Mt = 5.9722*1e+24
    sigma = 5.670374419*1e-8
    G = 6.67430*1e-11

    # Conversion to SI units
    P = P * 24*3600
    eP = eP * 24*3600
    Mp = Mp * Mt
    eMp = eMp * Mt
    Rs = Rs * 6.957*1e+8
    eRs = eRs * 6.957*1e+8

    # Density
    rho = 3*np.pi/(G*P**2) * a_Rs**2 - 3/(4*np.pi) * Mp/Rs**3
    erho = rho * np.sqrt((3*ea_Rs/a_Rs)**2 + (eP/P)**2 + (3*eRs/Rs)**2 + (eMp/Mp)**2)
    return(rho, erho)
