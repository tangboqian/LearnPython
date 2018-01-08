import json, sys
import pandas as pd
from pandas import DataFrame
import numpy as np
import matplotlib.pyplot as plt


def datafigure(file):
	df = pd.read_json(file)
	data = df[['user_id', 'minutes']].groupby('user_id').sum()
	# user_id = df.user_id
	# print(data)

	# min = user_id.min()
	# max = user_id.max()

	# list = []
	# for i in range(min, max + 1):
	# 	list.append(df[df['user_id'] == i]['minutes'].sum())
	# x = np.linspace(min, max, max - min + 1)
	# y = np.array(list)
	fig = plt.figure()
	ax = fig.add_subplot(1,1,1)
	ax.set_title("StudyData")
	ax.set_xlabel("User ID")
	ax.set_ylabel("Study Time")



	ax.plot(data.index, data.minutes)
	# fig.show()
	plt.show()

datafigure(sys.argv[1])
