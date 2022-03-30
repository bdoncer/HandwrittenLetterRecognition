from tkinter import *
from tkinter.colorchooser import askcolor
from PIL import ImageGrab
import numpy as np
import cv2
from keras.models import  load_model
from matplotlib import pyplot as plt
import imutils

def guess_image(path):
    model = load_model("model.h5")
    # Load the image
    img = cv2.imread(path)
    img = cv2.blur(img, (30,30))
    img_copy = img.copy()

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # Image for display
    img = cv2.resize(img, (400, 440))

    img_final = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)

    # Resize image for the model
    img_final = cv2.resize(img_final, (28, 28))



    img_final_shor = img_final.copy()

    img_final = np.reshape(img_final, (1, 28, 28, 1))
    img_final = np.divide(img_final, 255.0)

    img_final = np.subtract(1, img_final)

    img_pred = chr(np.argmax(model.predict(img_final)) + 65)
    # print(model.predict(img_final))
    # plt.imshow(img_final[0], cmap="Greys")
    # plt.xlabel("Prediction: " + img_pred)
    # plt.show()
    return img_pred
class Paint(object):

    def __init__(self):
        self.root = Tk()

        self.guess_button = Button(self.root, text='Guess', command=self.guess)
        self.guess_button.grid(row=0, column=3,columnspan=1)
        # Crete and position a clear button
        self.clear_button = Button(self.root, text='Clear', command=self.clear)
        self.clear_button.grid(row=0, column=1,columnspan=1)
        self.root.title("Write your letter below  :)")
        # The label_text has to be a Variable String because it changes
        self.label_text = StringVar()
        self.label_text.set("The prediction will be displayed here!")
        self.label = Label(self.root, textvariable = self.label_text, font=15)
        self.label.grid(row=2, columnspan = 5)


        self.c = Canvas(self.root, bg='white', width=600, height=600)
        self.c.grid(row=1, columnspan=5)

        self.setup()
        self.root.mainloop()

    def setup(self):
        self.x = None
        self.y = None
        self.c.bind('<B1-Motion>', self.paint)
        self.c.bind('<ButtonRelease-1>', self.reset)

    def guess(self):
        x = self.root.winfo_rootx() + self.c.winfo_x()
        y = self.root.winfo_rooty() + self.c.winfo_y()
        x1 = x + self.c.winfo_width()
        y1 = y + self.c.winfo_height()
        path = "to_guess.jpg"
        ImageGrab.grab().crop((x, y, x1, y1)).save(path)
        res = guess_image(path)
        self.label_text.set("Prediction: "+ res)


    def paint(self, event):
        if self.x and self.y:
            self.c.create_line(self.x, self.y, event.x, event.y,
                               width=30, fill='black',
                               capstyle=ROUND, smooth=TRUE, splinesteps=36)
        self.x = event.x
        self.y = event.y

    def reset(self, _):
        self.x, self.y = None, None

    def clear(self):
        self.c.delete("all")
if __name__ == '__main__':
    Paint()
