import csv
import sys
import getopt
import json

def usage():	
	print('Usage: python generateLayout.py -i <input_file> [ -o <output_file>]')
	print('<input_file> must be in CSV file format.')
	print('<ouput_file> (optional) contains a JSON object of the layout.')
	

def main(argv):
	inputFile = ''
	outputFile = ''

	columnHead = ''
	rowHead = ''

	try:
		options, args = getopt.getopt(argv, "hi:o:",["ifile=","ofile="])
	except getopt.GetoptError:
		print('Incorrect usage')
		usage()
		sys.exit(2)		

	for option, arg in options:
		if option == 'h':
			usage()
			sys.exit()
		if option in ("-i", "--ifile"):
			inputFile = arg
		elif option in ("-o", "--ofile"):
			outputFile = arg

	if inputFile == '':
		print('Please enter input file in CSV file format')
		usage()
		sys.exit(2)

	with open(inputFile, 'r') as csvfile:
		try:
			reader = csv.reader(csvfile, delimiter = ',')
		except Exception:
			print(inputFile + ' not in CSV file format.')

		layoutDic = {"layout":{}}

		for index, row in enumerate(reader):

			if index == 0: #First row
				rowCol = row[index].split('/')

				if len(rowCol) == 2:
					rowHead = rowCol[0].strip()
					columnHead = rowCol[1].strip()
					layoutDic[rowHead] = {"location": "1:1..."}
					layoutDic[columnHead] = {"location": "1...:1"}
					layoutDic["result"] = {"location": "1...:1..."}

				else:
					print("Input file is not in the required format.")
					sys.exit(1)

		jsonOut = json.dumps(layoutDic, indent = 4)

		if outputFile == '':
			print(jsonOut)
			return

		with open(outputFile, 'w') as writer:
			writer.write(jsonOut)
			writer.close()

		csvfile.close()
					
if __name__ == '__main__':
	main(sys.argv[1:])