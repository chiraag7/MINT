import csv


if __name__ == '__main__':	

	columnHead = ''
	rowHead = ''

	with open('Dataset/Crops_TrendAnalysis_2014-2016.csv', 'r') as csvfile:

		reader = csv.reader(csvfile, delimiter = ',')

		for index, row in enumerate(reader):

			if index == 0: #First row
				rowCol = row[index].split('/')
				if len(rowCol) == 2:
					rowHead = rowCol[0].strip()
					columnHead = rowCol[1].strip()
					print("layout")
					print("\t"+rowHead)
					print("\t\tlocation: " + "1:1...")
					print("\t"+columnHead)
					print("\t\tlocation: " +  "1...:1")
					print("\tresult")
					print("\t\tlocation: 1...:1...")

