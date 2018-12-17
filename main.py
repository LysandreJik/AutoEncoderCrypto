from Diffie_Hellman import dh_exchange
import numpy as np
from tkinter import *
from PIL import Image, ImageTk
from time import sleep


master = Tk()
master.resizable(False, False)

top_frame = Frame(master)
top_frame.pack()

side_frame = Frame(master)
side_frame.pack()

bottom_frame = Frame(master)
bottom_frame.pack(side=BOTTOM)


w = Label(master, text="the brown quick fox jumps over the lazy dog 0123456789")
w.config(font=("Courier", 24))
w.pack(side=TOP)

image = Image.fromarray(np.zeros((37, 20)))
image = image.resize((200, 370), Image.ANTIALIAS)
photo = ImageTk.PhotoImage(image)
panel = Label(side_frame, image=photo)
panel.pack(side=LEFT)

image2 = Image.fromarray(np.zeros((20, 15)))
image2 = image.resize((150, 200), Image.ANTIALIAS)
photo2 = ImageTk.PhotoImage(image2)
panel2 = Label(side_frame, image=photo2)
panel2.pack(side=LEFT)

image3 = Image.fromarray(np.zeros((15, 10)))
image3 = image.resize((100, 150), Image.ANTIALIAS)
photo3 = ImageTk.PhotoImage(image3)
panel3 = Label(side_frame, image=photo3)
panel3.pack(side=LEFT)

image4 = Image.fromarray(np.zeros((10, 15)))
image4 = image.resize((100, 150), Image.ANTIALIAS)
photo4 = ImageTk.PhotoImage(image4)
panel4 = Label(side_frame, image=photo4)
panel4.pack(side=LEFT)

image5 = Image.fromarray(np.zeros((15, 20)))
image5 = image.resize((150, 200), Image.ANTIALIAS)
photo5 = ImageTk.PhotoImage(image5)
panel5 = Label(side_frame, image=photo5)
panel5.pack(side=LEFT)

image6 = Image.fromarray(np.zeros((20, 37)))
image6 = image.resize((200, 370), Image.ANTIALIAS)
photo6 = ImageTk.PhotoImage(image6)
panel6 = Label(side_frame, image=photo6)
panel6.pack(side=LEFT)

v = StringVar()
label = Label(bottom_frame, textvariable=v)
label.config(font=("Courier", 24))
label.pack(side=TOP)

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
            array = np.array(
                auto_encoder.layers[1].get_weights()[0] * 255/np.max(np.max(auto_encoder.layers[1].get_weights()[0])))
            image = Image.fromarray(array)
            image = image.resize((200, 370), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(image)

            panel.configure(image=photo)
            panel.image = photo
            print(array.shape)

            array2 = np.array(
                auto_encoder.layers[2].get_weights()[0] * 255 / np.max(np.max(auto_encoder.layers[2].get_weights()[0])))
            image2 = Image.fromarray(array2)
            image2 = image2.resize((150, 200), Image.ANTIALIAS)
            photo2 = ImageTk.PhotoImage(image2)

            panel2.configure(image=photo2)
            panel2.image2 = photo2
            print(array2.shape)

            array3 = np.array(
                auto_encoder.layers[3].get_weights()[0] * 255 / np.max(np.max(auto_encoder.layers[3].get_weights()[0])))
            image3 = Image.fromarray(array3)
            image3 = image3.resize((100, 150), Image.ANTIALIAS)
            photo3 = ImageTk.PhotoImage(image3)

            panel3.configure(image=photo3)
            panel3.image3 = photo3
            print(array3.shape)

            array4 = np.array(
                auto_encoder.layers[4].get_weights()[0] * 255 / np.max(np.max(auto_encoder.layers[4].get_weights()[0])))
            image4 = Image.fromarray(array4.T)
            image4 = image4.resize((100, 150), Image.ANTIALIAS)
            photo4 = ImageTk.PhotoImage(image4)

            panel4.configure(image=photo4)
            panel4.image4 = photo4
            print(array4.shape)

            array5 = np.array(
                auto_encoder.layers[5].get_weights()[0] * 255 / np.max(np.max(auto_encoder.layers[5].get_weights()[0])))
            image5 = Image.fromarray(array5.T)
            image5 = image5.resize((150, 200), Image.ANTIALIAS)
            photo5 = ImageTk.PhotoImage(image5)

            panel5.configure(image=photo5)
            panel5.image5 = photo5
            print(array5.shape)

            array6 = np.array(
                auto_encoder.layers[6].get_weights()[0] * 255 / np.max(np.max(auto_encoder.layers[6].get_weights()[0])))
            image6 = Image.fromarray(array6.T)
            image6 = image6.resize((200, 370), Image.ANTIALIAS)
            photo6 = ImageTk.PhotoImage(image6)

            panel6.configure(image=photo6)
            panel6.image6 = photo6
            print(array6.shape)


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
    img = Image.fromarray(np.array(
        encrypted_sentence).reshape((18, 10))*255/np.max(np.max(np.array(encrypted_sentence).reshape((18, 10)))))
    img.show()
    print('Decrypted sentence is', decrypted_sentence)


b = Button(bottom_frame, text="OK", command=start_training)
b.pack(side=BOTTOM)


mainloop()
