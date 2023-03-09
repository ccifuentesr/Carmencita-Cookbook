import numpy as np
import uncertainties
from uncertainties.umath import *
import astropy.constants as const
import pandas as pd

# =============================================================================
# DATA
# =============================================================================

input_file = 'cif03.v01'
output_file = input_file + '_out.csv'
df = pd.read_csv('Data/'+input_file+'.csv', sep=",", header=0)

L_Lsol = [uncertainties.ufloat(df['L_Lsol'][i], df['eL_Lsol'][i]) for i in range(len(df))]
Teff_K = [uncertainties.ufloat(df['Teff_K'][i], df['eTeff_K'][i]) for i in range(len(df))]

# =============================================================================
# CONSTANTS
# =============================================================================

Mterra = 5.97237*1e24 # kg (exact)
Rterra = 6.3781*1e6 # m (exact)
Lsol = 3.828*1e26 # W (exact)
Rsol = 6.957*1e8 # m (exact)
au_m = 149597870700 # m (exact)
G = uncertainties.ufloat(6.67430*1e-11, 0.00015*1e-11) # m3 kg−1 s−2
GM = 1.3271244*1e20 # m3 s−2 (exact)
sigma = 5.670374419*1e-8 # W m-2 K-4 (exact)
Ssol = 1361 # W m-2

# =============================================================================
# FUNCTIONS
# =============================================================================

def Radius_SB(L_Lsol, Teff_K):
    """Stellar radius and its error from the Stefan–Boltzmann law under the black body approximation.

    Args:
        Lbol (float): Bolometric luminosity in solar units.
        Teff (float): Effective temperature in Kelvin.

    Returns:
        float: Stellar radius in solar units.
        float: Stellar radius error in solar units.

    Nominal solar values from the IAU B.3 resolution
    on recommended nominal conversion constants for selected solar and planetary properties:
    https://www.iau.org/static/resolutions/IAU2015_English.pdf

    Nominal solar luminosity: 3.828 x 10+26 W (exact)
    Nominal solar radius: 6.957 x 10+8 m (exact)

    Stefan-Boltzmann constant value from 2018 CODATA recommended values:
    https://physics.nist.gov/cuu/pdf/wall_2018.pdf

    Stefan-Boltzman constant, sigma: 5.670 374 419 x 10-8 W m-2 K-4 (exact)

    """
    R_Rsol = 1/Rsol * sqrt(L_Lsol*Lsol/(4*np.pi*sigma*Teff_K**4))
    return(R_Rsol)

def Teff_SB(L_Lsol, R_Rsol):
    """Effective temperature and its error from the Stefan–Boltzmann law under the black body approximation.

    Args:
        Lbol (float): Bolometric luminosity in solar units.
        Radius (float): Stellar radius in solar units.

    Returns:
        float: Effective temperature in Kelvin.
        float: Effective temperature error in Kelvin.
    """
    Teff_K = (L_Lsol*Lsol / (R_Rsol*Rsol)**2 / (4*np.pi*sigma))**(1/4)
    return(Teff_K)

def Mass_sch19(R_Rsol):
    """Stellar mass and its error from the empirical relation by Schweitzer et al. 2019
    (2019A&A...625A..68S), based on masses and radii of eclipsing binaries.

    Args:
        R_Rsol (float): Stellar radius in solar units.
        eR_Rsol (float): Stellar radius uncertainty in solar units.

    Returns:
        float: Stellar mass in solar units.
        float: Stellar mass error in solar units.

    (See Equation 6 in Schweitzer et al. 2019 and references therein).
    """
    a = uncertainties.ufloat(-0.024048024, 0.007592668)
    b = uncertainties.ufloat(1.0552427, 0.017044148)
    M_Msol = a + b * R_Rsol
    return(M_Msol)

# =============================================================================
# WRITE OUT
# =============================================================================

Radius = [Radius_SB(L_Lsol[i], Teff_K[i]) for i in range(len(df))]
Mass = [Mass_sch19(Radius[i]) for i in range(len(df))]

R_Rsol = [Radius[i].n for i in range(len(df))]
eR_Rsol = [Radius[i].s for i in range(len(df))]
M_Msol = [Mass[i].n for i in range(len(df))]
eM_Msol = [Mass[i].s for i in range(len(df))]


df_append = pd.DataFrame({'ID_star': df['ID_star'], 'R_Rsol': np.round(R_Rsol, 4), 'eR_Rsol': np.round(eR_Rsol, 4),\
'M_Msol': np.round(M_Msol, 4), 'eM_Msol': np.round(eM_Msol, 4)})

save_csv = 'yes'
output_full = 'no'

if save_csv == 'yes':
    df_append = pd.DataFrame(data=df_append)
    if output_full == 'yes':
        output = pd.concat([df, df_append], axis=1)
    else:
        output = df_append
    output.to_csv('Output/' + output_file, sep=',', encoding='utf-8')

# =============================================================================
# MANUAL USE
# =============================================================================

# print([np.round(Radius_SB(L_Lsol, Teff_K).n, 5), np.round(Radius_SB(L_Lsol, Teff_K).s, 5)])
# print([np.round(Mass_sch19(Radius_SB(L_Lsol, Teff_K)).n, 5), np.round(Mass_sch19(Radius_SB(L_Lsol, Teff_K)).s, 5)])
