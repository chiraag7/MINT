#Import Library of Gaussian Naive Bayes model
from sklearn.naive_bayes import GaussianNB
import numpy as np
import csv
import re
import pickle

# cell type
# 1. text 0
# 2. numbers 1
# 3. text + numbers 2
# 4. others

# For detecting 4 blocks - metadata(0), column headings(1), row headings(2), remaining cells(3), none(4)

letters = r'[a-zA-Z]+'
digits = r'[0-9]+'
alphanumeric = r'[a-zA-Z0-9\s]+'

trainDir = 'Train/'
testDir = 'Test/'

trainFiles = [('Central Equatorial 2014 Rainfall.csv', 2), ('IPC_Trend_Analysis-Unity.csv',2), ('Lakes_2014_Rainfall.csv',2)] 
# trainFiles =[('FAOSTAT_South_Sudan_Food_Security_Indicators_data_2014-2016.csv',1)]

def preprocess(filename, type):

	features = [] # A combination of row index (0), column index(1), cell type(2), up cell block type(3), left cell block type(4)
	out = []

	with open(filename, "r") as csvf:

		rows = csv.reader(csvf, delimiter = ',')
		
		for i, row in enumerate(rows):
			for j, col in enumerate(row):
				f = [i, j]

				if re.match(letters, col):
					f += [0]
				elif re.match(digits, col):
					f += [1]
				elif re.match(alphanumeric, col):
					f += [2]
				else:
					f += [3]

				# 2D data
				if type == 2:
					if i == 0 and j == 0:
						out.append(0)
						f.append(4)
						f.append(4)
					elif i == 0:
						out.append(1)
						f.append(4)
						if j == 1:
							f.append(0)
						else:
							f.append(1)
					elif j == 0:
						out.append(2)
						if i == 1:
							f.append(0)
						else:
							f.append(2)
						f.append(4)
					else:
						out.append(3)
						if i == 1 and j == 1:
							f.append(1)
							f.append(2)
						elif i == 1:
							f.append(1)
							f.append(3)
						elif j == 1:
							f.append(3)
							f.append(2)
						else:
							f.append(3)
							f.append(3)


				# 1D data
				elif type == 1:			
					if i == 0:
						out.append(1)
						f.append(4)
						if j == 0:
							f.append(4)
						else:
							f.append(1)
					else:
						out.append(3)
						if j == 0 and i == 1:
							f.append(1)
							f.append(4)
						elif i == 1:
							f.append(1)
							f.append(3)
						else:
							f.append(3)
							f.append(3)

				# f = f[:2] +f[3:]
				features.append(f)
				# print(",".join(map(str,f))+","+str(out[-1]))
			# print(i+1)
	# print (file)
	# print (features, out)
	return features, out

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


testFiles = ["Crops_Trend_Analysis_2014-2016.csv", "2014-01-01-2017-04-30-Eastern_Africa-South_Sudan.csv", 
			 "LivestockLoss_Cattle_Warrap_2017.csv", "South Sudan Statistics Summary WHO.csv", "imf-dm-inflation-2012-2016.csv",
			 "imf-dm-GDP-2012-2016.csv", "Crops_EstimatedProductionConsumptionBalance_2014.csv",
			 "South Sudan Life Expectancy WHO.csv", "Ground_Nuts_Unshelled-1kg-Jonglei-SSP-data_table.csv",
			 "rice_import_at_Kaya_2014-2017_data_table.csv"]

types = [1, 2]
for file in testFiles:
	accuracies = []
	for type in types:

		x, y = preprocess(testDir + file, type)

		pkl_file = open('pkl-1d.pkl', 'rb')
		model_1d = pickle.load(pkl_file)
		pkl_file.close()

		pkl_file = open('pkl-2d.pkl', 'rb')
		model_2d = pickle.load(pkl_file)
		pkl_file.close()

		# Predict Ensemble Output 
		predicted1 = model_1d.predict(np.array(x).tolist())
		predicted2 = model_2d.predict(np.array(x).tolist())

		correct1 = 0
		total1 = 0
		for f in range(len(x)):
			# print ((x[f][0],x[f][1]), predicted[f])
			if y[f] == predicted1[f]:
				correct1 += 1
			total1 += 1

		correct2 = 0
		total2 = 0
		for f in range(len(x)):
			# print ((x[f][0],x[f][1]), predicted[f])
			if y[f] == predicted2[f]:
				correct2 += 1
			total2 += 1

		accuracies.append(max(correct1 * 100.0 / total1, correct2 * 100.0 / total2))


	print(file + ": " + str(max(accuracies))+ '%')