# DUSTY00
# Interior models
# http://perso.ens-lyon.fr/isabelle.baraffe/DUSTY00_models

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rc
from matplotlib.ticker import FormatStrFormatter

# =============================================================================
# DATA & MODEL
# =============================================================================

df_data = pd.read_csv('Input/Carmencita.104.v01.csv', header=0)

p = .5
k = 2
Age = 5 # Choose 1, 5 or 10
plot = 'n'
output = 'y'

def dusty_model(star_number, p, k, Age, plot):
    """
    Estimate the mass, radius and Teff given the bolometric luminosity
    and the Age in Gigayears by fitting the DUSTY00 models.
    Specify the range of fitting (p) and the degree of the polynomial (k).
    If error ValueError: can only convert an array of size 1 to a Python scalar
    Change p value that defines the range of fitting.
    Specify if a plot must be also served (y) or not (n).
    """
    # Input data
    Karmn = df_data['Karmn'][star_number]
    L_Lsol = df_data['L_Lsol'][star_number]
    eL_Lsol = df_data['eL_Lsol'][star_number]
    Teff_K = df_data['Teff_K'][star_number]

    # Model data
    dusty_model = 'DUSTY00_' + str(Age)
    df_model = pd.read_csv('Dusty00/' + dusty_model + '.txt', header=0, sep="\s+")
    logL = df_model['L/Ls']
    Mass = df_model['M/Ms']
    Teff = df_model['Teff']
    Radius = df_model['R']

    # Polynomial fitting
    x = logL
    y1, y2, y3 = Teff, Mass, Radius
    #
    x_input = np.log10(L_Lsol) # Input luminosity
    xfit = [i for i in x if i >= x_input-p and i <= x_input+p] # Fitting range
    indices = []
    for j in range(len(xfit)):
        indices.append(x[x==xfit[j]].index.item())
    yfit1, yfit2, yfit3 = [], [], []
    for i in indices:
        yfit1.append(y1[i])
        yfit2.append(y2[i])
        yfit3.append(y3[i])
    #
    p1 = np.polyfit(xfit, yfit1, k, cov=False)
    p2 = np.polyfit(xfit, yfit2, k, cov=False)
    p3 = np.polyfit(xfit, yfit3, k, cov=False)
    #
    model1 = np.poly1d(p1)
    model2 = np.poly1d(p2)
    model3 = np.poly1d(p3)
    #
    xfitp = np.arange(min(xfit), max(xfit), 0.01)
    yfitp1 = model1(xfitp)
    yfitp2 = model2(xfitp)
    yfitp3 = model3(xfitp)
    #
    Teff = np.round(model1(x_input), 1)
    mass = np.round(model2(x_input), 6)
    radius = np.round(model3(x_input), 6)
    #
    if plot == 'y':
        plt.scatter(x, y2)
        plt.plot(xfitp, yfitp2, c='r')
        plt.show()
    else:
        pass
    return(Teff, mass, radius)

# =============================================================================
# RESULTS
# =============================================================================
Karmn, Teff, mass, radius, logL = [], [], [], [], []

for star_number in range(len(df_data)): #len(df_data)
    Karmn.append(df_data['Karmn'][star_number])
    logL.append(np.log10(df_data['L_Lsol'][star_number]))
    Teff.append(dusty_model(star_number, p, k, Age, plot)[0])
    mass.append(dusty_model(star_number, p, k, Age, plot)[1])
    radius.append(dusty_model(star_number, p, k, Age, plot)[2])

print(Karmn, logL, Teff, mass, radius)

# =============================================================================
# OUTPUT
# =============================================================================

if output == 'y':
    output_name = 'dusty_out_' + str(Age) + 'G.csv'
    file_out = pd.DataFrame({'Karmn': Karmn, 'logL': logL, 'Teff': Teff, 'mass': mass, 'radius': radius})
    file_out.to_csv('Output/' + output_name, sep=',', encoding='utf-8')
else:
    pass
