#Import Library of Gaussian Naive Bayes model
from sklearn.naive_bayes import GaussianNB
import numpy as np
import csv
import re
import pickle
import yaml

# cell type as feature
# 1. text 0
# 2. numbers 1
# 3. text + numbers 2
# 4. others

# Block type as output for each cell
# 1. Metadata 0 
# 2. Column headings 1 
# 3. Row headings 2 
# 4. Remaining cells 3
# 5. None(4)


# Regular expression definitions
LETTERS = r'[a-zA-Z]+'
DIGITS = r'[0-9]+'
ALPHANUMERIC = r'[a-zA-Z0-9\s]+'

# YAML files directory
DATASET_DIR = '../Dataset/'
CSV_DIR = 'csv_files/'
YAML_DIR = 'yaml_files/'

files = ["2014-01-01-2017-04-30-Eastern_Africa-South_Sudan.csv", "Central Equatorial 2014 Rainfall.csv" ,"Crops_TrendAnalysis_2014-2016.csv",
		 "FAOSTAT_South_Sudan_Food_Security_Indicators_data_2014-2016.csv", "Ground_Nuts_Unshelled-1kg-Jonglei-SSP-data_table.csv",
		 "IPC_Trend_Analysis-Unity.csv", "Lakes 2014 Rainfall.csv", "LivestockLoss_Cattle_Warrap_2017.csv", 
		 "rice_import_at_Kaya_2014-2017_data_table.csv", "South Sudan CHIRP PrecipitationInMM 1-1-2014to4-17-2017.csv", 
		 "South Sudan Statistics Summary WHO.csv"]

'''
# @params
# resourceFile - CSV resource file
# yamlFile - Corresponding YAML file containing details about blocks

# Processes the yaml file to identify block type for 
# every cell in the data resource file.
'''
def preprocess(resourceFile, yamlFile):

	# A combination of row index (0), column index(1), cell type(2), up cell block type(3), left cell block type(4)
	features = [] 
	out = []

	with open(resourceFile, "r") as csvf:

		rows = csv.reader(csvf, delimiter = ',')
		
		for i, row in enumerate(rows):			
			for j, col in enumerate(row):				
				featureVector = [i, j]

				if re.match(LETTERS, col):
					featureVector += [0]
				elif re.match(DIGITS, col):
					featureVector += [1]
				elif re.match(ALPHANUMERIC, col):
					featureVector += [2]
				else:
					featureVector += [3]

				fileStream = open(yamlFile, 'r')
				yamlObj = yaml.load(fileStream.read())
				fileStream.close()

				print(yamlObj['layout'])
				
				features.append(featureVector)

	return features, out


def train():
	for file in files:
		preprocess(DATASET_DIR + CSV_DIR + file, DATASET_DIR + YAML_DIR + file[:-4] + ".yaml")
		break

# x_train, y_train = [], []
# for file, type in trainFiles:
# 	x, y = preprocess(trainDir + file, type)
# 	x_train += x
# 	y_train += y
# x, y = np.array(x_train), np.array(y_train)

# # Create a Gaussian Classifier
# model = GaussianNB()

# # Train the model using the training sets 
# model.fit(x, y)

# output = open('pkl-2d.pkl', 'wb')
# pickle.dump(model, output)
# output.close()

train()


# types = [1, 2]
# for file in testFiles:
# 	accuracies = []
# 	for type in types:

# 		x, y = preprocess(testDir + file, type)

# 		pkl_file = open('pkl-1d.pkl', 'rb')
# 		model_1d = pickle.load(pkl_file)
# 		pkl_file.close()

# 		pkl_file = open('pkl-2d.pkl', 'rb')
# 		model_2d = pickle.load(pkl_file)
# 		pkl_file.close()

# 		# Predict Ensemble Output 
# 		predicted1 = model_1d.predict(np.array(x).tolist())
# 		predicted2 = model_2d.predict(np.array(x).tolist())

# 		correct1 = 0
# 		total1 = 0
# 		for f in range(len(x)):
# 			# print ((x[f][0],x[f][1]), predicted[f])
# 			if y[f] == predicted1[f]:
# 				correct1 += 1
# 			total1 += 1

# 		correct2 = 0
# 		total2 = 0
# 		for f in range(len(x)):
# 			# print ((x[f][0],x[f][1]), predicted[f])
# 			if y[f] == predicted2[f]:
# 				correct2 += 1
# 			total2 += 1

# 		accuracies.append(max(correct1 * 100.0 / total1, correct2 * 100.0 / total2))


# 	print(file + ": " + str(max(accuracies))+ '%')