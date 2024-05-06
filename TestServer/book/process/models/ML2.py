
#math/data libs
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import OneHotEncoder

#ml libs
# import keras
from keras import backend as K
from keras.models import Sequential
# from keras. layers import Activation
# from keras.layers.core import Dense
from keras.layers import Dense, Activation, Dropout, Reshape, Permute
# from keras.optimizers import Adam
from tensorflow.keras.optimizers import Adam
import pickle
# from keras.optimizers import adam_v2
# from keras.metrics import categorical_crossentropy
# from keras.utils import to_categorical


from pathlib import Path

mypath = Path().absolute()
print(mypath/'data_set/test.csv')

trainFilePath = mypath/'data_set/train.csv'
testFilePath = mypath/'data_set/test.csv'

trainFile = pd.read_csv(trainFilePath).drop(columns="datasetId")
testFile = pd.read_csv(testFilePath).drop(columns="datasetId")


#train
train_samples = trainFile.drop(columns='condition').to_numpy()
train_labels = trainFile['condition'].to_numpy()

#test
test_samples = testFile.drop(columns='condition').to_numpy()
test_labels = testFile['condition'].to_numpy()


#normalizing features
scaler = MinMaxScaler(feature_range=(0,1))
train_samples = scaler.fit_transform(train_samples)
test_samples = scaler.fit_transform(test_samples)

#one-hot-encoding labels
one_hot_encoder = OneHotEncoder(categories='auto')
train_labels = one_hot_encoder.fit_transform(train_labels.reshape(-1, 1)).toarray()
test_labels = one_hot_encoder.fit_transform(test_labels.reshape(-1, 1)).toarray()


#build the model
model = Sequential([
    Dense(34, input_shape=[34,], activation='relu'),
#     Dense(20, activation='relu'),
    Dense(10, activation='relu'),
    Dense(3, activation='softmax')
])


model.summary()

opt = Adam(learning_rate=0.0001)

model.compile(
            optimizer=opt,
            loss='categorical_crossentropy',
            metrics=['accuracy'])


model.fit(train_samples, train_labels, validation_split=0.1, batch_size=10, epochs=3, shuffle=True, verbose=2)


# model.save('model2')

knnPickle = open('model2', 'wb') 
      
# source, destination 
pickle.dump(model, knnPickle)  


model.predict(test_samples)

knnPickle.close()

# test_samples





