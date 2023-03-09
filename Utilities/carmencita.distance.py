import numpy as np

def d_pc(pi_mas, epi_mas):
	"""Calculate the distance in parsec from the parallax in milliarcsec.
	"""
	d_pc = 1000/pi_mas
	ed_pc = d_pc*epi_mas/pi_mas
	return print(d_pc, ed_pc)