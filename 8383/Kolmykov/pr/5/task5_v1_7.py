import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import numpy as np
from keras.layers import Input, Dense
from keras.models import Model


train_data = np.genfromtxt('train.csv', delimiter=';')
test_data = np.genfromtxt('test.csv', delimiter=';')

train_x = np.reshape(train_data[:, 0], (len(train_data), 1))
train_y = np.reshape(train_data[:, 1], (len(train_data), 1))
test_x = np.reshape(test_data[:, 0], (len(test_data), 1))
test_y = np.reshape(test_data[:, 1], (len(test_data), 1))

coded_train_x = train_x * 2
coded_test_x = test_x * 2

main_input = Input(shape=(1,), name='main_input')

# encoding_layer = Dense(16, activation='relu')(main_input)
# encoding_layer = Dense(16, activation='relu')(encoding_layer)
# encoding_layer = Dense(16, activation='relu')(encoding_layer)
# encoding_output = Dense(1, name='encoding_output')(encoding_layer)
encoding_output = Dense(1, name='encoding_output')(main_input)

# decoding_layer = Dense(16, activation='relu')(encoding_output)
# decoding_layer = Dense(16, activation='relu')(decoding_layer)
# decoding_layer = Dense(16, activation='relu')(decoding_layer)
# decoding_output = Dense(1, name='decoding_output')(decoding_layer)
decoding_output = Dense(1, name='decoding_output')(encoding_output)

regression_layer = Dense(64, activation='relu')(encoding_output)
# regression_layer = Dense(64, activation='relu')(regression_layer)
regression_layer = Dense(64, activation='relu')(regression_layer)
regression_output = Dense(1, name='regression_output')(regression_layer)

model = Model(inputs=[main_input], outputs=[regression_output, encoding_output, decoding_output])
model.compile(optimizer='rmsprop', loss='mse', metrics='mae')
model.fit([train_x], [train_y, coded_train_x, train_x], epochs=200, batch_size=5, validation_split=0)

# model = Model(inputs=[main_input], outputs=[encoding_output])
# model.compile(optimizer='rmsprop', loss='mse', metrics='mae')
# model.fit([train_x], [coded_train_x], epochs=150, batch_size=5, validation_split=0)

test = np.array([[3], [4], [5], [6], [7], [8], [9], [10]])

regression_model = Model(inputs=[main_input], outputs=[regression_output])
print(regression_model.predict(test))
regression_prediction = regression_model.predict(test_x)

encoding_model = Model(inputs=[main_input], outputs=[encoding_output])
print(encoding_model.predict(test))
encoding_prediction = encoding_model.predict(test_x)

decoding_model = Model(inputs=[main_input], outputs=[decoding_output])
print(decoding_model.predict(test))
decoding_prediction = decoding_model.predict(test_x)

regression_model.save('regression_model.h5')
encoding_model.save('encoding_model.h5')
decoding_model.save('decoding_model.h5')

np.savetxt('regression_results.csv', np.hstack((test_y, regression_prediction)), delimiter=';')
np.savetxt('encoding_results.csv', np.hstack((coded_test_x, encoding_prediction)), delimiter=';')
np.savetxt('decoding_results.csv', np.hstack((test_x, decoding_prediction)), delimiter=';')
