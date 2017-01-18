# a few methods and attributes for the DataFrame class

import pandas as pd

# ACTIONS == METHODS (use ())
# ATTRIBUTES (no ())

def attributes_methods():
	movies = pd.read_csv('http://bit.ly/imdbratings')
	print movies.head()

	print movies.describe() # general summary of columns with numerical values

	print movies.shape # prints num rows and cols

	print movies.dtypes # prints data types of each column


if __name__ == "__main__":
	attributes_methods()
