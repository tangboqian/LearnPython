import pandas as pd
from pandas import DataFrame

def quarter_volume():
	second_volume = 0
	data = pd.read_csv('apple.csv', header = 0)
	# df  = DataFrame(data)
	i = pd.data_range(data['Date'])
	dd = pd.Series(data.Volume, index = i)

	dd = dd.resample('M').sum()
	print(dd.head(10))
	return second_volume

quarter_volume()
