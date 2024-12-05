# data format: 
# [longitude, latitude, avg_summer_max, avg_summer_low, total_summer_rain, average_previous_snowfall, lanina_data, elnino_data, laninaintensity_data, elninointensity_data, carbon_data, elevation, season, yearly_snow]
# Constants for var locations:
LONGITUDE = 0
LATITUDE = 1
AVG_SUMMER_MAX = 2
AVG_SUMMER_LOW = 3
TOTAL_SUMMER_RAIN = 4
AVERAGE_PREVIOUS_SNOWFALL = 5
LANINA_DATA = 6
ELNINO_DATA = 7
LANINAINTENSITY_DATA = 8
ELNINOINTENSITY_DATA = 9
CARBON_DATA = 10
ELEVATION = 11
SEASON = 12
YEARLY_SNOW = 13


import numpy as np
import tensorflow as tf
from tensorflow import keras

#get data from numpy array
data = np.load("processed_data.npy", allow_pickle=True)

#split train and test data without a function, test data is past 2015
train_data = []
test_data = []
for row in data:
    if row[SEASON] < 2015:
        train_data.append(row)
    else:
        test_data.append(row)

#remove season
train_data = np.delete(train_data, SEASON, 1)
test_data = np.delete(test_data, SEASON, 1)

#split into x and y
train_x = train_data[:, :-1]
train_y = train_data[:, -1]

test_x = test_data[:, :-1]
test_y = test_data[:, -1]

#scale data between 0 and 1
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
train_x = scaler.fit_transform(train_x)
test_x = scaler.transform(test_x)

#build model with regression output
model = keras.Sequential([
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(64, activation='relu'),
    keras.layers.Dense(32, activation='relu'),
    keras.layers.Dense(1)
])

model.compile(optimizer='adam', loss='mean_squared_error')

model.fit(train_x, train_y, epochs=100, batch_size=32)

#save model
model.save('snow_model')

def evaluate_model(test_x, test_y):

    model = keras.models.load_model('snow_model')
    predictions = model.predict(test_x)
    
    return predictions


predictions = evaluate_model(test_x, test_y)
for i in range(len(predictions)):
    print(f'Actual: {test_y[i]}, Predicted: {predictions[i]}')


#get other statistics from the model
from sklearn.metrics import mean_squared_error, r2_score

mse = mean_squared_error(test_y, predictions)
r2 = r2_score(test_y, predictions)

print(f'Mean Squared Error: {mse}')
print(f'R2 Score: {r2}')

