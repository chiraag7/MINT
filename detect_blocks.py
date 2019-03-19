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

# For detecting 4 blocks - metadata(0), column headings(1), row headings(2), remaining cells(3)

features = []
out = []

def preprocess(filename):

	with open(filename, "r") as csvf:
		rows = csv.reader(csvf, delimiter = ',')

		for i, row in enumerate(rows):
			for j, col in enumerate(row):
				f = [i, j]

				if re.match(r'[a-zA-Z]+', col):
					f += [0]
				elif re.match(r'[0-9]+', col):
					f += [1]
				elif re.match(r'[a-zA-Z0-9\s]+', col):
					f += [2]
				else:
					f += [3]

				features.append(f)

				if i == 0 and j == 0:
					out.append(0)
				elif i == 0:
					out.append(1)
				elif j == 0:
					out.append(2)
				else:
					out.append(3)

	return np.array(features), np.array(out)


#assigning predictor (row, col, celltype) and target variables
x, y = preprocess("IPC_Trend_Analysis-Unity.csv")

#Create a Gaussian Classifier
model = GaussianNB()

# Train the model using the training sets 
model.fit(x, y)

x, y = preprocess("Crops_TrendAnalysis_2014-2016.csv")

#Predict Output 
predicted= model.predict(x.tolist())
for f in range(len(x)):
	print ((x[f][0],x[f][1]), predicted[f])