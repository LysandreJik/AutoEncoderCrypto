from Diffie_Hellman import dh_exchange
import numpy as np
from tkinter import *
from PIL import Image, ImageTk


from time import sleep

master = Tk()

w = Label(master, text="the brown quick fox jumps over the lazy dog 0123456789")
w.config(font=("Courier", 24))
w.pack()

image = Image.fromarray(np.zeros((37, 20)))
photo = ImageTk.PhotoImage(image)
panel = Label(master, image=photo)
panel.pack()

v = StringVar()
label = Label(master, textvariable=v)
label.config(font=("Courier", 24))
label.pack()

v.set("xxxxxxxxxxxxxxxxxx")
x = 0

from keras.callbacks import Callback

auto_encoder = ""


def set_auto_encoder(trained_auto_encoder):
    global auto_encoder
    auto_encoder = trained_auto_encoder

alphabet = "abcdefghijklmnopqrstuvwxyz1234567890 "


def one_hot_encode_letter(letter):
    return np.identity(len(alphabet))[alphabet.index(letter)]


def one_hot_decode_letter(letter):
    return alphabet[np.argmax(letter)]

class Callback2(Callback):
    def on_train_begin(self, logs={}):
        print('Start!')

    def on_epoch_end(self, epoch, logs=None):
        if epoch % 100 == 0:
            global auto_encoder
            text = "the brown quick fox jumps over the lazy dog 0123456789"

            encoded_text = []

            for letter in text:
                # print('Before encoding', letter)
                print(letter, auto_encoder.layers[1].get_weights()[0][0][0])
                letter = np.array([one_hot_encode_letter(letter)])
                # print('After encoding', letter)
                # print('Predicted', auto_encoder.predict(letter))
                encoded_text.append(one_hot_decode_letter(auto_encoder.predict(letter, batch_size=1, verbose=0)))
            # print(auto_encoder.layers[1].get_weights()[0][0][0])
            array = np.array(auto_encoder.layers[1].get_weights()[0] * 255/np.max(np.max(auto_encoder.layers[1].get_weights()[0])))
            image = Image.fromarray(array)
            image = image.resize((250, 250), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(image)

            panel.configure(image=photo)
            panel.image = photo
            print(array)

            v.set(''.join(encoded_text))
            Tk.update(master)


def start_training():
    alice_key, bob_key = dh_exchange()
    print('Key has been chosen !', alice_key, bob_key)
    np.random.seed(alice_key)

    from auto_encoder import train
    from encode import encode, decode

    print('Starting training ...')
    train(Callback2(), set_auto_encoder)

    alice_sentence = "bonjour bob 123456"

    encrypted_sentence = encode(alice_sentence)

    decrypted_sentence = decode(encrypted_sentence)

    print('Original sentence was', alice_sentence)
    print('Encrypted sentence was', np.array(encrypted_sentence).reshape((18, 10)))
    img = Image.fromarray(np.array(encrypted_sentence).reshape((18, 10))*255/np.max(np.max(np.array(encrypted_sentence).reshape((18, 10)))))
    img.show()
    print('Decrypted sentence is', decrypted_sentence)


b = Button(master, text="OK", command=start_training)
b.pack()


mainloop()



