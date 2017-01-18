# sort/filter the DataFrame by column values

import pandas as pd

def sort():
	movies = pd.read_csv('http://bit.ly/imdbratings')
	print movies.head()

	# if you want to see titles only..
	print movies.title.sort_values(ascending=False)
	
	# if you want to see all of thedata, but sorted by title
	print movies.sort_values('title')

	# to sort by multiple values
	movies.sort_values(['content_rating', 'duration']) # first sort by content_rating, then "ties" are broken by duration


def filter_by_col():
	movies = pd.read_csv('http://bit.ly/imdbratings')

	# booleans = []
	# for length in movies.duration:
	# 	if length >= 200:
	# 		append(True)
	# 	else:
	# 		append(False)
	# is_long = pd.Series(booleans) # converts list to Pandas Series
	# movies[is_long] # retrieves Pandas DataFrame with all movies >200 mins

	is_long = movies.duration >= 200
	print movies[is_long]

	# or most succinctly..
	print movies[movies.duration >= 200]

	# pull out genres of movies over 200 mins
	print movies[movies.duration >= 200].genre
	# equivalently (better method)
	print movies.loc(movies.duration >= 200, 'genre')


def filter_mult():
	movies = pd.read_csv('http://bit.ly/imdbratings')


if __name__ == "__main__":
	# sort()
	# filter_by_col()
	filter_mult()