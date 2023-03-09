import numpy as np 
import pandas as pd
import math

# Data

input_name = 'carmencita.102.beta.013'
output_name = input_name + '_out.csv'

df = pd.read_csv('Data/'+input_name+'.csv')

Karmn = df['Karmn']
Lbol = df['L_Lsol']
eLbol = df['eL_Lsol']
R_Rsol = df['R_Rsol']
eR_Rsol = df['eR_Rsol']
M_Msol = df['M_Msol']
eM_Msol = df['eM_Msol']

# Rounding 

Lbol_round = []
eLbol_round = []
R_Rsol_round = []
eR_Rsol_round = []
M_Msol_round = []
eM_Msol_round = []
for i in range(len(Lbol)):
	eLbol_round.append("%.4g" % eLbol[i])
	eLbol_round_dec = (str(eLbol_round[i])[::-1].find('.')) # Number of decimal places
	Lbol_round.append(round(Lbol[i], eLbol_round_dec))
	eR_Rsol_round.append("%.3g" % eR_Rsol[i])
	eR_Rsol_round_dec = (str(eR_Rsol_round[i])[::-1].find('.'))
	R_Rsol_round.append(round(R_Rsol[i], eR_Rsol_round_dec))
	eM_Msol_round.append("%.3g" % eM_Msol[i])
	eM_Msol_round_dec = (str(eM_Msol_round[i])[::-1].find('.'))
	M_Msol_round.append(round(M_Msol[i], eM_Msol_round_dec))

# Write out

rounded = pd.DataFrame(
    {'Karmn': Karmn, 'L_Lsol': Lbol_round, 'eL_Lsol': eLbol_round, 'R_Rsol': R_Rsol_round, 'eR_Rsol': eR_Rsol_round, 'M_Msol': M_Msol_round, 'eM_Msol': eM_Msol_round})
output = pd.concat([df, rounded], axis=1)
rounded.to_csv(output_name, sep=',', encoding='utf-8')

