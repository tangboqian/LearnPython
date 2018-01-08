import pandas as pd
from pandas import DataFrame

def quarter_volume():
	second_volume = 0
	data = pd.read_csv('apple.csv', header = 0)
	# transfer a rangeIndex instance to a DatetimeIndex instance
	i = pd.to_datetime(data.index)
	vol_data = pd.Series(data.Volume, index = i)

	vol_data = vol_data.resample('3M').sum()
	print(dd.head(10))
	
	#find the second-max volume
	maxV = vol_data.max()
	for v in vol_data.Volume:
		if v > second_volume && v < max:
			second_volume = v
	
	return second_volume

quarter_volume()
