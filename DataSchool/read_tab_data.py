# how to import data into a DataFrame

import pandas as pd

def read_tab_data():
	orders = pd.read_table('http://bit.ly/chiporders')
	print orders.head()

	user_cols = ['user_id', 'age', 'gender', 'occupation', 'zip_code']
	users = pd.read_table('http://bit.ly/movieusers', sep='|', header = None, names = user_cols)
	print users.head()

if __name__ == "__main__":
	read_tab_data()
