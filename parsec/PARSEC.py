# PARSEC Stellar Evolution Code
# Evolutionary tracks
# https://people.sissa.it/~sbressan/parsec.html

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rc
from matplotlib.ticker import FormatStrFormatter

def parsec(star_number, p, k, Age, plot):
    """
    Estimate the masses given the bolometric luminosity and the Age
    in Gigayears by fitting the PARSEC models to a k-degree polynomial.
    """
    df_data = pd.read_csv('Input/Carmencita.overluminous.v12.csv', header=0)
    Age_Ma = df_data['Age_' + Age + '_Ma'][star_number]
    #
    Karmn = df_data['Karmn'][star_number]
    L_Lsol = df_data['L_Lsol'][star_number]
    eL_Lsol = df_data['eL_Lsol'][star_number]
    Teff_min_K = df_data['Teff_min_K'][star_number]
    Teff_mean_K = df_data['Teff_mean_K'][star_number]
    Teff_max_K = df_data['Teff_max_K'][star_number]
    #
    cmd_model = 'CMD_' + str(Age_Ma)
    df_model = pd.read_csv('CMD3.4/' + cmd_model + '.txt', header=0, sep="\s+")
    logL = df_model[df_model['Mass'] < 1]['logL']
    Mass = df_model[df_model['Mass'] < 1]['Mass']
    Teff = df_model[df_model['Mass'] < 1]['logTe']

    def parsec_fitting(x, y, x_input, k, p = p, print_results = 'n'):
        """
        Model fitting for the PARSEC models.
        x_input is the luminosity in solar units (decimal).
        """
        x_input = np.log10(x_input)
        xfit = [i for i in x if i >= x_input-p and i <= x_input+p]
        indices = []
        for j in range(len(xfit)):
            indices.append(x[x==xfit[j]].index.item())
        yfit = []
        for i in indices:
            yfit.append(y[i])
        #
        p, cov = np.polyfit(xfit, yfit, k, cov=True)
        model = np.poly1d(p)
        #
        xfitp = np.sort(xfit)
        yfitp = model(xfitp)  # Equivalent to np.polyval(p, xfit)
        #
        perr = np.sqrt(np.diag(cov))
        #
        R2 = np.corrcoef(yfit, 10**model(xfit))[0, 1]**2
        #
        resid = yfit - 10**model(xfit)
        n = len(yfit)
        m = p.size
        dof = n - m
        #
        chi2 = np.sum((resid/model(xfit))**2)
        chi2red = chi2/(dof)
        if print_results == 'y':
            print('Polynomial fitting:\n')
            print('degree =', k, '\nR2 =', R2, '\nchi2 =', chi2, '\nchi2_red =',
                  chi2red, '\ncoeffs a-c =', p, '\nerr_coeffs a-c =', perr)
        else:
            pass
        return(xfitp, yfitp, np.round(model(x_input), degree))

    def Radius_SB(L_Lsol, eL_Lsol, Teff_K):
        """
        Stellar radius from the Stefan–Boltzmann law
        under the black body approximation.
        It tries to maximize the error in the uncertainty.
        """
        Lsol = 3.828*1e26 # W (exact)
        Rsol = 6.957*1e8 # m (exact)
        sigma = 5.670374419*1e-8 # W m-2 K-4 (exact)
        #
        if Age == 'min':
            L_Lsol = L_Lsol-eL_Lsol
            Teff_K = Teff_max_K
        elif Age == 'mean':
            L_Lsol = L_Lsol
            Teff_K = Teff_mean_K
        elif Age == 'max':
            L_Lsol = L_Lsol+eL_Lsol
            Teff_K = Teff_min_K
        #
        R_Rsol = 1/Rsol * np.sqrt((L_Lsol)*Lsol/(4*np.pi*sigma*Teff_K**4))
        return(np.round(R_Rsol, 7))

    def plotting(x, y, xfitp, yfitp, savefig = 'n'):
        """
        Plotting model and fitting region in PARSEC models.
        """
        rc('font', **{'family': 'serif', 'serif': ['DejaVu Serif']})
        rc('text', usetex=False)
        plt.rcParams['mathtext.fontset'] = 'dejavuserif'
        #
        xlabel = r'$\log\,{L/L_\odot}$'
        if np.mean(y) < 1:
            ylabel = r'$\mathcal{M}/\mathcal{M}_\odot$'
        elif np.mean(y) > 1000:
            ylabel = r'$T_{\rm eff}$ [K]'
        #
        figsize = (12, 10)
        pointsize = 20
        tickssize = 22
        labelsize = 22
        #
        fig, ax = plt.subplots(figsize=figsize)
        #
        ax.scatter(x, y, s=pointsize, c='grey')
        ax.plot(xfitp, yfitp, 'b--', lw=2)
        #
        ax.set_xlabel(xlabel, size=labelsize)
        ax.set_ylabel(ylabel, size=labelsize)
        ax.xaxis.set_major_formatter(FormatStrFormatter('%.1f'))
        ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
        #
        ax.tick_params(axis='x', labelsize=tickssize, direction='in',
                       top=True, labeltop=False, which='both')
        ax.tick_params(axis='y', labelsize=tickssize, direction='in',
                       right=True, labelright=False, which='both')
        ax.tick_params('both', length=10, width=1, which='major')
        ax.tick_params('both', length=5, width=1, which='minor')
        ax.minorticks_on()
        ax.xaxis.set_tick_params(which='minor', bottom=True, top=True)
        plt.show()
        if savefig == 'y':
            plt.savefig('figure.png', bbox_inches='tight')
        else:
            pass
    #
    mass = np.round(parsec_fitting(logL, Mass, L_Lsol, k)[2], 7)
    Teff = np.round(10**parsec_fitting(logL, Teff, L_Lsol, k)[2], 2)
    radius = Radius_SB(L_Lsol, eL_Lsol, Teff)
    if plot == 'y':
        plotting(logL, Mass, parsec_fitting(logL, Mass, L_Lsol, k)[0], parsec_fitting(logL, Mass, L_Lsol, k)[1])
    return[Karmn, mass, Teff, radius]


# =============================================================================
# RUNNING
# =============================================================================

"""
ACHTUNG!
If error ValueError: can only convert an array of size 1 to a Python scalar
Change p value that defines the range of fitting (default p = 0.2).
"""

# star_number = int(input())
# p = float(input())
# Age = str(input())
# plot = str(input())
#
star_number = int(input('Star number: '))
p = 0.4
k = 2
Age = 'max'
plot = 'n'

print(parsec(star_number, p, k, Age, plot))

# =============================================================================
# WRITE OUT
# =============================================================================

# params_min = [] ; params_mean = [] ; params_max = []
# Karmn_min = [] ; Karmn_mean = [] ; Karmn_max = []
# mass_min = [] ; mass_mean = [] ; mass_max = []
# Teff_min = [] ; Teff_mean = [] ; Teff_max = []
# radius_min = [] ; radius_mean = [] ; radius_max = []

# for i in range(23):
#     p = 0.2
#     try:
#         params_min = parsec(i, p, 'min', 'n')
#         Karmn_min.append(params_min[0])
#         mass_min.append(params_min[1])
#         Teff_min.append(params_min[2])
#         radius_min.append(params_min[3])
#         #
#         params_mean = parsec(i, p, 'mean', 'n')
#         Karmn_mean.append(params_mean[0])
#         mass_mean.append(params_mean[1])
#         Teff_mean.append(params_mean[2])
#         radius_mean.append(params_mean[3])
#         #
#         params_max = parsec(i, p, 'max', 'n')
#         Karmn_max.append(params_max[0])
#         mass_max.append(params_max[1])
#         Teff_max.append(params_max[2])
#         radius_max.append(params_max[3])
#     except:
#         pass

# output_name = 'parsec_out.csv'
# file_out = pd.DataFrame({
#       # 'Karmn_min': Karmn_min, 'M_min_Msol': mass_min, 'Teff_min_K': Teff_min, 'R_min_Rsol': radius_min
#        # 'Karmn_mean': Karmn_mean, 'M_mean_Msol': mass_mean, 'Teff_mean_K': Teff_mean, 'R_mean_Rsol': radius_mean
#        'Karmn_max': Karmn_max, 'M_max_Msol': mass_max, 'Teff_max_K': Teff_max, 'R_max_Rsol': radius_max
#       })
# file_out.to_csv('Output/' + output_name, sep=',', encoding='utf-8')
