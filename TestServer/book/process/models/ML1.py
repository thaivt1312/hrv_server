
import numpy as np

import pandas as pd
from sklearn import datasets, svm, metrics
import matplotlib.pyplot as plt

import os, os.path as osp

import pickle 

# from google.colab import drive
# drive.mount('/content/drive')

from pathlib import Path

mypath = Path().absolute()
print(mypath/'data_set/test.csv')

trainFilePath = mypath/'data_set/train.csv'
testFilePath = mypath/'data_set/test.csv'

trainFile = pd.read_csv(trainFilePath).drop(columns="datasetId")
testFile = pd.read_csv(testFilePath).drop(columns="datasetId")


#features
X_train = trainFile.drop(columns='condition')
y_train = trainFile['condition']
X_test = testFile.drop(columns='condition')
y_test = testFile['condition']


from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier()
knn.fit(X_train, y_train)
print('Accuracy of K-NN classifier on training set: {:.2f}'
     .format(knn.score(X_train, y_train)))
print('Accuracy of K-NN classifier on test set: {:.2f}'
     .format(knn.score(X_test, y_test)))

i=1
knn.predict([X_test.iloc[i]])

print(X_test.iloc[i])

knnPickle = open('knnpickle_file', 'wb') 
      
# source, destination 
pickle.dump(knn, knnPickle)  

# close the file
knnPickle.close()
