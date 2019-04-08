import csv
with open("Test/imf-dm-inflation-2012-2016.csv", "r") as csvf:
	rows = csv.reader(csvf, delimiter = ',')
	for r in rows:
		print(r)