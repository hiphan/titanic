import numpy as np
import tensorflow
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import GridSearchCV
import csv

from utils import *

# pd.set_option('display.max_columns', 500)


# 3-layer NN
def titanic_model(layer_1=25, layer_2=35):
    model = Sequential()
    model.add(Dense(layer_1, input_shape=(5, )))
    model.add(Activation('relu'))
    model.add(Dropout(rate=0.5))

    model.add(Dense(layer_2))
    model.add(Activation('relu'))
    model.add(Dropout(rate=0.5))

    model.add(Dense(2))
    model.add(Activation('sigmoid'))

    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model


x_train, y_train, x_test = read_data_nn()

# Grid search: number of hidden units in layer 1 and layer 2 
layer_1 = [10, 15, 20, 25, 30, 35, 40]
layer_2 = [10, 15, 20, 25, 30, 35, 40]
param_grid = dict(layer_1=layer_1, layer_2=layer_2)
keras_tt = KerasClassifier(build_fn=titanic_model, epochs=25, batch_size=16, verbose=0)
grid = GridSearchCV(estimator=keras_tt, param_grid=param_grid, cv=5, verbose=2)
grid.fit(x_train, y_train)
results = grid.cv_results_
params = grid.best_params_
print(params)       
# {'layer_1': 25, 'layer_2': 35}

layer_1_units = params['layer_1']
layer_2_units = params['layer_2']
tt_model = titanic_model(layer_1=layer_1_units, layer_2=layer_2_units)
tt_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
tt_model.fit(x_train, y_train, epochs=100, batch_size=16, verbose=1)
test_prediction = tt_model.predict_classes(x_test)

with open('result.csv', mode='w') as result_file:
    writer = csv.writer(result_file, delimiter=',')
    writer.writerow(['PassengerId', 'Survived'])
    for p in range(892, 1310):
        writer.writerow([p, test_prediction[p - 892]])

# Accuracy (Kaggle score): 0.77990
