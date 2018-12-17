from auto_encoder import train
from keras.layers import Input, Dense
from keras.models import Model
import numpy as np
import sys


# Training dataset (all the possible values)
# As the dataset is exhaustive, we want to overfit the model
alphabet = "abcdefghijklmnopqrstuvwxyz1234567890 "

# We use One Hot encoding for letters
def one_hot_encode_letter(letter):
    return np.identity(len(alphabet))[alphabet.index(letter)]


def one_hot_decode_letter(letter):
    return alphabet[np.argmax(letter)]

# To encrypt the text we use only the first half of the network
def encode(text):
    n_values = 37
    input_img = Input(shape=(n_values,))

	# Loading the 3 first trained weights
    [W1, b1] = np.load('W1.wb.npy')
    [W2, b2] = np.load('W2.wb.npy')
    [W3, b3] = np.load('W3.wb.npy')

	# Loading the layers with the weights
    l1 = Dense(20, activation='relu', weights=[W1, b1])
    l2 = Dense(15, activation='relu', weights=[W2, b2])
    l3 = Dense(10, activation='relu', weights=[W3, b3], dtype='int32')

	# Run the text through the network
    encoded = l3(l2(l1(input_img)))
    autoencoder = Model(input_img, encoded)
	
	# Define the cipher text array
    encoded_text = []

	# And putting encrypted letters in the cipher text
    for letter in text:
        letter = np.array([one_hot_encode_letter(letter)])
        encoded_text.append(autoencoder.predict(letter).astype('int8'))

    return encoded_text

# To decrypt the cipher text, we use the second half of the network
def decode(encoded_text):
    n_values = 10
    input_img = Input((n_values, ))

	# Loading the 3 next trained weights
    [W4, b4] = np.load('W4.wb.npy')
    [W5, b5] = np.load('W5.wb.npy')
    [W6, b6] = np.load('W6.wb.npy')

	# Loading the layers with the weights
    l4 = Dense(15, activation='relu', weights=[W4, b4])
    l5 = Dense(20, activation='relu', weights=[W5, b5])
    l6 = Dense(37, activation='sigmoid', weights=[W6, b6])

	# Run the cipher text through the network
    decoded = l6(l5(l4((input_img))))
    autoencoder = Model(input_img, decoded)

	# Define the decoded text
    text = []

	# And putting decrypted letters in the decoded text
    for encoded_letter in encoded_text:
        letter = autoencoder.predict(encoded_letter)
        text.append(one_hot_decode_letter(letter))

    return text

# This is useless wtf. 
def test():
    print(one_hot_encode_letter('b'))
    print(one_hot_decode_letter(one_hot_encode_letter('5')))

    sentence = 'hello my good sir 123'
    encoded_text = encode(sentence)
    decoded_text = decode(encoded_text)

    print('Original sentence', sentence)
    print('Encoded text', encoded_text)
    print('Decoded text', decoded_text)


# train(0)
#
# if len(sys.argv) > 2 and sys.argv[2] == "encode":
#     print(encode(sys.argv[1]))
# elif len(sys.argv) > 2 and sys.argv[2] == "decode":
#     print(decode(sys.argv[1]))
# else:
#     print('Text', sys.argv[1])
#     print('Encoded text', encode(sys.argv[1]))
#     print('Decoded text', decode(encode(sys.argv[1])))

