import numpy as np
import pandas as pd
import csv

input_name = 'carmencita.101_references.csv'
# input_name = 'carmencita.101_description.csv'
output_name = 'out_' + input_name

df = pd.read_csv('Data/'+input_name)

# %%
# Use for log

Abb = df['Abbreviation']
Art = df['Article']
Jou = df['Journal']
Vol = df['Volume']
Num = df['Number']

with open(output_name, mode='w') as mycsv:
    writer = csv.writer(mycsv, delimiter='\n')
    rows = []
    for i in range(len(Abb)):
        rows.append(("{}:\t{} ({}, {}, {})").format(
            Abb[i].strip(), Art[i], Jou[i], Vol[i], Num[i]))
    writer.writerow(rows)

text = open(output_name, 'r')
text = ''.join([i for i in text]).replace(", nan", "")
x = open(output_name, 'w')
x.writelines(text)
x.close()

# %%
# Use for description

# Col = df['Column']
# Lab = df['Label']
# For = df['Format']
# Uni = df['Units']
# Rem = df['Remarks']
# Exp = df['Explanations']
#
# with open(output_name, mode='w') as mycsv:
#     writer = csv.writer(mycsv, delimiter='\n')
#     #header = []
#     rows = []
#     for i in range(len(Col)):
#         rows.append(("\t{}\t{}\t\t\t\t{}\t{}\t{}\t{}").format(
#             Col[i], Lab[i].strip(), For[i].strip(), Uni[i].strip(), Rem[i], Exp[i]))
#     writer.writerow(rows)
#
# # Reopen file and tune up.
# # Copy in clipboard to paste directly in LaTeX table.
#
# text = open(output_name, 'r')
# text = ''.join([i for i in text]).replace("nan", "")
# x = open(output_name, 'w')
# x.writelines(text)
# # pyperclip.copy(text)  # copies into clipboard
# x.close()
