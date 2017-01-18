# methods for selecting, renaming, and removing columns (Series)

import pandas as pd

def select_series():
	ufo = pd.read_csv('http://bit.ly/uforeports')
	print type(ufo) # confirm we have a DataFrame object
	print ufo.head()

	type(ufo['City']) # confirm we have a Series object - (aka column)
	# ufo.City also is an attribute
	# if column name has a space in it OR conflicts with a DataFrame attribute, dot notation will not work!

	ufo['Location'] = ufo.City + ', ' + ufo.State # must use bracket notation in order to create a new column to the DataFrame
	print ufo.head()


def rename_columns():
	ufo = pd.read_csv('http://bit.ly/uforeports')
	print ufo.columns

	# Method 1
	ufo.rename(columns={'Colors Reported':'Colors_Reported', 'Shape Reported': 'Shape_Reported'}, inplace=True) # pass a dictionary where key is old name and value is the new name
	print ufo.columns


	# Method 2
	ufo_cols = ['city', 'colors reported', 'shape reported', 'state', 'time']
	ufo.columns = ufo_cols
	print ufo.columns

	# Method 3
	ufo = pd.read_csv('http://bit.ly/uforeports', names=ufo_cols, header=0) # row 0 has the header, but rewrite the column names

	# say there are a lot of column headers with spaces and we want to cut out all of the spaces and replace with _
	ufo.columns = ufo.columns.str.replace(' ', '_')


def remove_columns():
	ufo = pd.read_csv('http://bit.ly/uforeports')
	print ufo.head()

	# say we want to get rid of the "Colors Reported" column
	ufo.drop('Colors Reported', axis=1, inplace=True) # axis 0 = row, axis 1 = column
	print ufo.head()

	# now the City and State columns..
	ufo.drop(['City', "State"], axis=1, inplace=True)
	print ufo.head()

	# to remove rows, just use axis=0!
	ufo.drop([0, 1], axis=0, inplace=True)
	print ufo.head()


if __name__ == "__main__":
	# select_series()
	# rename_columns()
	remove_columns()
