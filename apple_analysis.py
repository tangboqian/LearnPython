import pandas as pd
from pandas import DataFrame

def quarter_volume():
	second_volume = 0
	data = pd.read_csv('apple.csv', header = 0)
	# transfer a rangeIndex instance to a DatetimeIndex instance

	i = pd.to_datetime(data['Date'])	
	y = np.array(data['Volume'])
	# print(y)
	vol_data = pd.Series(y, index = i)

	# print(vol_data)
	vol_data = vol_data.resample('Q').sum()
	
	print(vol_data)
	#find the second-max volume
	maxV = vol_data.max()
	for v in vol_data[vol_data.index]:
		if v > second_volume and v < maxV:
			second_volume = v
	print(maxV)
	print(second_volume)
	return second_volume

quarter_volume()
