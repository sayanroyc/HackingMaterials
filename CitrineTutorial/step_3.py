# Handbook step 3: rewrite Citrine tutorial using Pandas data frame

from pymatgen import Composition, Element
from numpy import zeros, mean
from sklearn import linear_model, metrics, ensemble
from sklearn.model_selection import cross_val_score, ShuffleSplit
import pandas as pd
import matplotlib.pyplot as plt

MAX_Z = 100 # maximum length of vector to hold naive feature set


def naiveVectorize(composition):
    vector = zeros((MAX_Z))
    for element in composition:
        fraction = composition.get_atomic_fraction(element)
        vector[element.Z - 1] = fraction
    return(vector)


def get_physical_features(composition):
	these_features = []
	fraction = []
	atomic_num = []
	eneg = []
	group = []

	for element in composition:
		fraction.append(composition.get_atomic_fraction(element))
		atomic_num.append(float(element.Z))
		eneg.append(element.X)
		group.append(float(element.group))

	# We want to sort this feature set
	# according to which element in the binary compound is more abundant
	must_reverse = False

	if fraction[1] > fraction[0]:
		must_reverse = True

	for features in [fraction, atomic_num, eneg, group]:
		if must_reverse:
			features.reverse()
	these_features.append(fraction[0] / fraction[1])
	these_features.append(eneg[0] - eneg[1])
	these_features.append(group[0])
	these_features.append(group[1])

	return these_features


def main():
	col_names = ['compound', 'bandgap'] # file has no header, so we add our own
	bg = pd.read_csv('bandgapDFT.csv', names=col_names, header=None)
	print bg.head()


	# construct naive feature set and add it to the existing data frame
	compositions = bg['compound'].apply(Composition) # this is a Pandas series containing the compositions
	bg['naive_features'] = compositions.apply(naiveVectorize) # apply the naiveVectorize functinon on the compositions
	print bg.head()


	# Establish baseline accuracy by "guessing the average" of the band gap set
	# A good model should never do worse.
	baselineError = mean(abs(mean(bg.bandgap) - bg.bandgap))
	print("The MAE of always guessing the average band gap is: " + str(round(baselineError, 3)) + " eV")


	# Train linear ridge regression model using naive feature set
	linear = linear_model.Ridge(alpha = 0.5) # alpha is a tuning parameter affecting how regression deals with collinear inputs
	cv = ShuffleSplit(n_splits=10, test_size=0.1, random_state=0)

	naive_scores = cross_val_score(linear, list(bg['naive_features']), bg['bandgap'], cv=cv, scoring='neg_mean_absolute_error')
	print("The MAE of the linear ridge regression band gap model using the naive feature set is: " + str(round(abs(mean(naive_scores)), 3)) + " eV")


	# Let's see which features are most important for the linear model
	print("Below are the fitted linear ridge regression coefficients for each feature (i.e., element) in our naive feature set")
	linear.fit(list(bg['naive_features']), bg['bandgap']) # fit to the whole data set; we're not doing CV here

	print("element: coefficient")
	for i in range(MAX_Z):
	       element = Element.from_Z(i + 1)
	       print(element.symbol + ': ' + str(linear.coef_[i]))


	# Create alternative feature set that is more physically-motivated
	bg['physical_features'] = compositions.apply(get_physical_features)
	print bg.head()

	physical_scores = cross_val_score(linear, list(bg['physical_features']), bg['bandgap'], cv=cv, scoring='neg_mean_absolute_error')
	print("The MAE of the linear ridge regression band gap model using the physical feature set is: " + str(round(abs(mean(physical_scores)), 3)) + " eV")


	# Random forest
	rfr = ensemble.RandomForestRegressor(n_estimators=10) # try 10 trees in the forest

	naive_scores = cross_val_score(rfr, list(bg['naive_features']), bg['bandgap'], cv=cv, scoring='neg_mean_absolute_error')
	print("The MAE of the nonlinear random forest band gap model using the naive feature set is: " + str(round(abs(mean(naive_scores)), 3)) + " eV")

	physical_scores = cross_val_score(rfr, list(bg['physical_features']), bg['bandgap'], cv=cv, scoring='neg_mean_absolute_error')
	print("The MAE of the nonlinear random forest band gap model using the physical feature set is: " + str(round(abs(mean(physical_scores)), 3)) + " eV")


if __name__ == "__main__":
	main()
