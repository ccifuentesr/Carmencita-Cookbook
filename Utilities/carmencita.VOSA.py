# Exports a txt file ready to be digested by VOSA
# Uses Gaia EDR3 (2020).
# See http://svo2.cab.inta-csic.es/theory/fps/

import numpy as np
import pandas as pd
# import pyperclip
import csv

# Data

input_name = 'Carmencita.104'
output_name = 'Output/' + input_name + '_out.csv'
df = pd.read_csv('Data/' + input_name + '.csv')

# Filters

filters = ['BP', 'G', 'RP', 'B', 'V', 'g', 'r',
           'i', 'J', 'H', 'Ks', 'W1', 'W2', 'W3', 'W4']
filters_name = ['BP_mag', 'GG_mag', 'RP_mag', 'B_mag', 'V_mag', 'g_mag', 'r_mag', 'i_mag',
                'J_mag', 'H_mag', 'Ks_mag', 'W1_mag', 'W2_mag', 'W3_mag', 'W4_mag']
efilters_name = ['eBP_mag', 'eGG_mag', 'eRP_mag', 'eB_mag', 'eV_mag', 'eg_mag', 'er_mag', 'ei_mag',
                 'eJ_mag', 'eH_mag', 'eKs_mag', 'eW1_mag', 'eW2_mag', 'eW3_mag', 'eW4_mag']
VOSA_filters = ['GAIA/GAIA3.Gbp', 'GAIA/GAIA3.G', 'GAIA/GAIA3.Grp', 'Misc/UCAC.B', 'Misc/UCAC.V', 'Misc/UCAC.sdss_g', 'Misc/UCAC.sdss_r', 'Misc/UCAC.sdss_i', '2MASS/2MASS.J', '2MASS/2MASS.H',
                '2MASS/2MASS.Ks', 'WISE/WISE.W1', 'WISE/WISE.W2', 'WISE/WISE.W3', 'WISE/WISE.W4']

# Variables

Name = df['Karmn']
RA = df['RA_J2016_deg']
DE = df['DE_J2016_deg']
d_pc = np.round(df['d_pc'], 5)
ed_pc = np.round(df['ed_pc'], 5)

mags = [[] for i in range(len(filters))]
e_mags = [[] for i in range(len(filters))]
for i in range(len(filters)):
    mags[i] = df[filters_name[i]]
    e_mags[i] = df[efilters_name[i]]

# To csv

with open(output_name, mode='w') as mycsv:
    writer = csv.writer(mycsv, delimiter='\n')
    header = []
    rows = []
    for i in range(len(Name)):
        for j in range(len(filters)):
            rows.append(("{} {} {} {}+-{} --- {} {} {} --- ---").format(
                Name[i], np.round(RA[i], 2), np.round(DE[i], 2), d_pc[i], ed_pc[i], VOSA_filters[j], mags[j][i], e_mags[j][i]))
    writer.writerow(rows)

# Reopen file and tune up.
# Copy in clipboard to paste directly in LaTeX table.

text = open(output_name, 'r')
text = ''.join([i for i in text]).replace("   ---", " --- --- ---")
text = ''.join([i for i in text]).replace("nan", "---")
x = open(output_name, 'w')
x.writelines(text)
# pyperclip.copy(text)  # copies into clipboard
x.close()

# %%
