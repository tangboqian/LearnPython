import sys

import json

import pandas as pandas

import numpy as np

from pandas import DataFrame

def analysis(file, id):

	df = pandas.read_json(file)

	# minutes = df[df['user_id'] == id]['minutes'].sum()

	df = df[df['user_id'] == id].minutes



	times = df.count()

	minutes = df.sum()

	

	return times, minutes

# analysis(sys.argv[1], sys.argv[2])


# import sys
# import json
# import pandas as pd


# def analysis(file, user_id):
#     """? file json ?????? user_id ?????????
#     Args:
#         file(str): json file name
#         user_id(int): user id
#     """

#     try:
#         df = pd.read_json(file)
#     except ValueError:
#         return 0, 0

#     df = df[df['user_id'] == user_id].minutes
#     print(df.count())
#     print(df.sum())
#     return df.count(), df.sum()

# analysis(sys.argv[1], sys.argv[2])
