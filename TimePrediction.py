import pandas as pd
import numpy as np
from array import *
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
df = pd.read_csv('restaurantcustomer.csv')
df.replace('?', np.NaN)

df.dropna()
label_encoder = preprocessing.LabelEncoder()
X1=df.drop(columns="numberofdaysfininshed",axis=1)
Y1=df[['numberofdaysfininshed']]
X=X1
Y=Y1

Y.numberofdaysfininshed.unique()
# One-hot encode the data using pandas get_dummies
features = pd.get_dummies(X1)
# Display the first 5 rows of the last 12 columns
features.iloc[:,5:].head(5)
# Use numpy to convert to arrays
import numpy as np
# Labels are the values we want to predict
labels = np.array(Y['numberofdaysfininshed'])
# Remove the labels from the features
# axis 1 refers to the columns
features= X
# Saving feature names for later use
feature_list = list(features.columns)
# Convert to numpy array
features = np.array(features)
# Using Skicit-learn to split data into training and testing sets
from sklearn.model_selection import train_test_split
# Split the data into training and testing sets
train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size = 0.25, random_state = 42)

# print('Training Features Shape:', train_features.shape)
# print('Training Labels Shape:', train_labels.shape)
# print('Testing Features Shape:', test_features.shape)
# print('Testing Labels Shape:', test_labels.shape)

# Import the model we are using
from sklearn.ensemble import RandomForestRegressor
# Instantiate model with 1000 decision trees
rf = RandomForestRegressor(n_estimators = 1000, random_state = 42)
# Train the model on training data
rf.fit(train_features, train_labels);
# Use the forest's predict method on the test data
predictions = rf.predict(test_features)
# Calculate the absolute errors
errors = abs(predictions - test_labels)
# Print out the mean absolute error (mae)

#print('Mean Absolute Error:', round(np.mean(errors), 2), 'degrees.')

import pickle

filename = 'rftimeseries.sav'
pickle.dump(rf, open(filename, 'wb'))
errors
test_labels

# Calculate mean absolute percentage error (MAPE)
mape = 100 * (errors/ test_labels)
# Calculate and display accuracy
accuracy = 100 - np.mean(mape)
#print('Accuracy:', round(accuracy, 2), '%.')
len(test_labels)
len(predictions)
predictions
test_features[[0]]
item=1
iteminkg=2
people=1
children=4

predictionsof1 = rf.predict([[item,iteminkg,people,children]])



def timePredict(item,iteminkg,people,children):
    pred = rf.predict([[item, iteminkg, people, children]])
    return pred