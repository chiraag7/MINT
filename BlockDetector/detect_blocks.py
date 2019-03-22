#Import Library of Gaussian Naive Bayes model
from sklearn.naive_bayes import GaussianNB
import numpy as np
import csv
import re

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

trainFiles = ['Central Equatorial 2014 Rainfall.csv', 'IPC_Trend_Analysis-Unity.csv', 'Lakes_2014_Rainfall.csv']

def preprocess(filename):

	features = [] # A combination of row index, column index, cell type, up cell block type, left cell block type
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
				f = f[:2] + f[3:]
				features.append(f)
	print (features)
	return features, out

x_train, y_train = [], []
for file in trainFiles:
	x, y = preprocess(trainDir + file)
	x_train += x
	y_train += y
x, y = np.array(x_train), np.array(y_train)

# Create a Gaussian Classifier
model = GaussianNB()

# Train the model using the training sets 
model.fit(x, y)

x, y = preprocess(testDir + "Crops_Trend_Analysis_2014-2016.csv")

#Predict Output 
predicted= model.predict(np.array(x).tolist())

correct = 0
total = 0
for f in range(len(x)):
	# print ((x[f][0],x[f][1]), predicted[f])
	if y[f] == predicted[f]:
		correct += 1
	total += 1
print(str(correct * 100.0 / total) + '%')