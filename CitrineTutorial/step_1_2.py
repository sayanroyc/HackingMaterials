from pymatgen import Composition, Element
from numpy import zeros, mean
from sklearn import linear_model, metrics, ensemble
from sklearn.model_selection import cross_val_score, ShuffleSplit
import pandas as pd
import matplotlib.pyplot as plt


# Training file containing band gaps extracted from Materials Project
# created in previous blog post and linked here
trainFile = open("bandgapDFT.csv","r").readlines()

# Input: pymatgen Composition object
# Output: length-100 vector representing any chemical formula

def naiveVectorize(composition):
    vector = zeros((MAX_Z))
    for element in composition:
        fraction = composition.get_atomic_fraction(element)
        vector[element.Z - 1] = fraction
    return(vector)

# Extract materials and band gaps into lists, and construct naive feature set
materials = []
bandgaps = []
naiveFeatures = []

MAX_Z = 100 # maximum length of vector to hold naive feature set

for line in trainFile:
    split = str.split(line, ',')
    material = Composition(split[0])
    materials.append(material) #store chemical formulas
    naiveFeatures.append(naiveVectorize(material)) #create features from chemical formula
    bandgaps.append(float(split[1])) #store numerical values of band gaps

# Establish baseline accuracy by "guessing the average" of the band gap set
# A good model should never do worse.
baselineError = mean(abs(mean(bandgaps) - bandgaps))
print("The MAE of always guessing the average band gap is: " + str(round(baselineError, 3)) + " eV")




# Train linear ridge regression model using naive feature set
# alpha is a tuning parameter affecting how regression deals with collinear inputs
linear = linear_model.Ridge(alpha = 0.5)
cv = ShuffleSplit(n_splits=10, test_size=0.1, random_state=0)

naive_scores = cross_val_score(linear, naiveFeatures, bandgaps, cv=cv, scoring='neg_mean_absolute_error')
print("The MAE of the linear ridge regression band gap model using the naive feature set is: " + str(round(abs(mean(naive_scores)), 3)) + " eV")




# Let's see which features are most important for the linear model
print("Below are the fitted linear ridge regression coefficients for each feature (i.e., element) in our naive feature set")
linear.fit(naiveFeatures, bandgaps) # fit to the whole data set; we're not doing CV here

print("element: coefficient")
for i in range(MAX_Z):
       element = Element.from_Z(i + 1)
       print(element.symbol + ': ' + str(linear.coef_[i]))




# Create alternative feature set that is more physically-motivated
physicalFeatures = []

for material in materials:
    theseFeatures = []
    fraction = []
    atomicNo = []
    eneg = []
    group = []

    for element in material:
        fraction.append(material.get_atomic_fraction(element))
        atomicNo.append(float(element.Z))
        eneg.append(element.X)
        group.append(float(element.group))

    # We want to sort this feature set
    # according to which element in the binary compound is more abundant
    mustReverse = False

    if fraction[1] > fraction[0]:
        mustReverse = True

    for features in [fraction, atomicNo, eneg, group]:
        if mustReverse:
            features.reverse()
    theseFeatures.append(fraction[0] / fraction[1])
    theseFeatures.append(eneg[0] - eneg[1])
    theseFeatures.append(group[0])
    theseFeatures.append(group[1])
    physicalFeatures.append(theseFeatures)

physical_scores = cross_val_score(linear, physicalFeatures, bandgaps, cv=cv, scoring='neg_mean_absolute_error')
print("The MAE of the linear ridge regression band gap model using the physical feature set is: " + str(round(abs(mean(physical_scores)), 3)) + " eV")





# Random forest
rfr = ensemble.RandomForestRegressor(n_estimators=10) #try 10 trees in the forest

naive_scores = cross_val_score(rfr, naiveFeatures, bandgaps, cv=cv, scoring='neg_mean_absolute_error')
print("The MAE of the nonlinear random forest band gap model using the naive feature set is: " + str(round(abs(mean(naive_scores)), 3)) + " eV")

physical_scores = cross_val_score(rfr, physicalFeatures, bandgaps, cv=cv, scoring='neg_mean_absolute_error')
print("The MAE of the nonlinear random forest band gap model using the physical feature set is: " + str(round(abs(mean(physical_scores)), 3)) + " eV")




# handbook step 2
df = pd.read_csv('bandgapDFT.csv', header=None, names=['Compound','Band Gap (eV)'])
print df.head(3)
print df.tail(3)

df.hist()
plt.title("Band Gap Distribution")
plt.show()

df["Band Gap Squared (eV^2)"] = df["Band Gap (eV)"]**2
df.plot(kind='scatter', x="Band Gap (eV)", y="Band Gap Squared (eV^2)")
plt.title("Band Gap vs Band Gap Squared")
plt.show()

pd.tools.plotting.scatter_matrix(df)
plt.show()
