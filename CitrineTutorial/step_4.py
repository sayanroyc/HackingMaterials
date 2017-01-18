# Handbook step 4: add formtion energy and density to the learner

import sys
from pymatgen import Composition, Element, MPRester
import numpy as np
from sklearn import linear_model, metrics, ensemble
from sklearn.model_selection import cross_val_score, ShuffleSplit
import pandas as pd
import matplotlib.pyplot as plt

API_KEY = None # key received from Materials Project

if API_KEY is None:
	m = MPRester()
else:
	m = MPRester(API_KEY)


def get_formation_energy_and_density(compound):
	# returns formation energy and density as
	# f_e, d

	print 'working on', compound['compound_name']

	returned_compounds = m.get_data(compound['compound_name']) 
	# returns of a list which matches the given compound
	# multiple hits are returned, we can get the specific one we need by sorting using bandgap
	# we have the bandgap, compare it to each entry, and keep the one which is closest

	band_gap_diffs = []
	for c in returned_compounds:
		# if c['band_gap'] != compound['band_gap']:
			# returned_compounds.remove(c)
		# decimal places are off.. ex. 2.918 vs 2.9180
		band_gap_diffs.append(abs(c['band_gap']-compound['band_gap']))

	# take care of case where compound does not exist in database..
	if band_gap_diffs == []:
		print "Matching compounds for " + compound['compound_name'] + " does not exist. Replacing formation energy and density with 0."
		return 0, 0
	ind = np.argmin(band_gap_diffs)
	matching_compound = returned_compounds[ind]

	# if len(returned_compounds) != 1:
	# 	sys.exit("Matching compounds for " + compound['compound_name'] + " exceeds 1. Matches: " + str(len(returned_compounds)))
		# print "Matching compounds for " + compound_name + " is not 1. Matches: " + len(returned_compounds)

	return pd.Series({'formation_energy':matching_compound['formation_energy_per_atom'], 'density':matching_compound['density']})


def main():

	col_names = ['compound_name', 'band_gap'] # file has no header, so we add our own
	compounds = pd.read_csv('bandgapDFT.csv', names=col_names, header=None)
	print compounds.head()

	a = compounds.apply(get_formation_energy_and_density, axis=1)
	# compounds['formation_energy_density'] = compounds.apply(get_formation_energy_and_density, axis=1)
	# compounds['formation_energy'], compounds['density'] = compounds.apply(get_formation_energy_and_density, axis=1)
	# compounds['formation_energy'] = compounds['formation_energy_density']
	# compounds['density'] = compounds['formation_energy_density'][1]
	# compounds.drop(['formation_energy_density'], axis=1, inplace=True)
	# print a.head()
	compounds =  pd.concat([compounds, a], axis=1)
	print compounds.head()

if __name__ == "__main__":
	main()