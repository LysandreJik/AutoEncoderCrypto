from auto_encoder import train
from keras.layers import Input, Dense
from keras.models import Model
import numpy as np
import sys

alphabet = "abcdefghijklmnopqrstuvwxyz1234567890 "


def one_hot_encode_letter(letter):
    return np.identity(len(alphabet))[alphabet.index(letter)]


def one_hot_decode_letter(letter):
    return alphabet[np.argmax(letter)]


def encode(text):
    n_values = 37
    input_img = Input(shape=(n_values,))

    [W1, b1] = np.load('W1.wb.npy')
    [W2, b2] = np.load('W2.wb.npy')
    [W3, b3] = np.load('W3.wb.npy')

    l1 = Dense(20, activation='relu', weights=[W1, b1])
    l2 = Dense(15, activation='relu', weights=[W2, b2])
    l3 = Dense(10, activation='relu', weights=[W3, b3], dtype='int32')

    encoded = l3(l2(l1(input_img)))
    autoencoder = Model(input_img, encoded)

    encoded_text = []

    for letter in text:
        letter = np.array([one_hot_encode_letter(letter)])
        encoded_text.append(autoencoder.predict(letter).astype('int8'))

    return encoded_text


def decode(encoded_text):
    n_values = 10
    input_img = Input((n_values, ))

    [W4, b4] = np.load('W4.wb.npy')
    [W5, b5] = np.load('W5.wb.npy')
    [W6, b6] = np.load('W6.wb.npy')

    l4 = Dense(15, activation='relu', weights=[W4, b4])
    l5 = Dense(20, activation='relu', weights=[W5, b5])
    l6 = Dense(37, activation='sigmoid', weights=[W6, b6])

    decoded = l6(l5(l4((input_img))))
    autoencoder = Model(input_img, decoded)

    text = []

    for encoded_letter in encoded_text:
        letter = autoencoder.predict(encoded_letter)
        text.append(one_hot_decode_letter(letter))

    return text


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

