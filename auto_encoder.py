from keras.layers import Input, Dense
from keras.models import Model
import numpy as np


# Creating and training the auto_encoder
def train(callback, set_auto_encoder):
    n_values = 37
    epochs = 5000
	
	# Creating the dataset for training and testing
    x_train = np.identity(n_values)
    x_test = np.identity(n_values)
	
	# Creating the input values
    input_img = Input(shape=(n_values,))
	
	# Creating the model
    l1 = Dense(20, activation='relu')
    l2 = Dense(15, activation='relu')

    l3 = Dense(10, activation='relu', dtype='int4')

    l4 = Dense(15, activation='relu')
    l5 = Dense(20, activation='relu')

    l6 = Dense(37, activation='sigmoid')

	# Defining the model process
    encoded = l3(l2(l1(input_img)))
    decoded = l6(l5(l4((encoded))))

	# Compile the model
    autoencoder = Model(input_img, decoded)
    autoencoder.compile(optimizer='adadelta', loss='binary_crossentropy')

	# Set the model to use in the main
    set_auto_encoder(autoencoder)

	# Start the training 
    autoencoder.fit(x_train, x_train,
                    epochs=epochs,
                    validation_data=(x_test, x_test), callbacks=[callback], verbose=1)

	# Save the weights
    np.save("W1.wb", l1.get_weights())
    np.save("W2.wb", l2.get_weights())
    np.save("W3.wb", l3.get_weights())
    np.save("W4.wb", l4.get_weights())
    np.save("W5.wb", l5.get_weights())
    np.save("W6.wb", l6.get_weights())

