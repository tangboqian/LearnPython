#!/usr/bin/env python3

import sys

def WageCalculator(strs):

	try:
		input = strs.split(':')
		workerID = (int)(input[0])
		wage = (int)(input[1])
		TaxedWage = wage*(1 - 0.165) - 3500
		
	except:
		print("Parameter Must Be Integer")
		# sys.exit()

	tax = 0.00

	if TaxedWage <= 0:
		tax = 0.00
	elif TaxedWage <= 1500:
		tax = TaxedWage*0.03
	elif TaxedWage <= 4500:
		tax = TaxedWage*0.1 - 105
	elif TaxedWage <= 9000:
		tax = TaxedWage*0.2 - 555
	elif TaxedWage <= 35000:
		tax = TaxedWage*0.25 - 1005
	elif TaxedWage <= 55000:
		tax = TaxedWage*0.30 - 2755
	elif TaxedWage <= 80000:
		tax = TaxedWage*0.35 - 5505
	else:
		tax = TaxedWage*0.45 - 13505

	finalWage = wage*(1 - 0.165) - tax

	print(str(workerID) + ":" + str(format(finalWage, ".2f")))

for arg in sys.argv[1:]:
	WageCalculator(arg)

