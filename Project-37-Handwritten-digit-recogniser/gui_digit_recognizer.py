from keras.models import load_model
from tkinter import *
import tkinter as tk
import tkinter.colorchooser as colorchooser
import win32gui
from PIL import ImageGrab, Image
import numpy as np
import os

model = load_model('mnist.h5')

def predict_digit(img):
    # resize image to 28x28 pixels
    img = img.resize((28,28))
    # convert rgb to grayscale
    img = img.convert('L')
    img = np.array(img)
    # reshaping to support model input and normalizing
    img = img.reshape(1,28,28,1)
    img = img/255.0
    # predicting the class
    res = model.predict([img])[0]
    return np.argmax(res), max(res)

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Handwritten Digit Recognizer")
        
        self.x = self.y = 0
        self.pen_color = "black"
        self.pen_size = 8
        self.strokes = []   # to keep track for undo

        # Left side: canvas
        self.canvas = tk.Canvas(self, width=300, height=300, bg="white", cursor="cross")
        self.canvas.grid(row=0, column=0, rowspan=6, pady=2, padx=2)

        # Right side: labels and buttons
        self.label = tk.Label(self, text="Draw a Digit", font=("Helvetica", 36))
        self.label.grid(row=0, column=1, pady=10, padx=10)

        self.classify_btn = tk.Button(self, text="Recognize", command=self.classify_handwriting)
        self.classify_btn.grid(row=1, column=1, pady=5)

        self.button_clear = tk.Button(self, text="Clear", command=self.clear_all)
        self.button_clear.grid(row=2, column=1, pady=5)

        self.button_undo = tk.Button(self, text="Undo", command=self.undo_last)
        self.button_undo.grid(row=3, column=1, pady=5)

        self.button_color = tk.Button(self, text="Pen Color", command=self.choose_color)
        self.button_color.grid(row=4, column=1, pady=5)

        self.button_save = tk.Button(self, text="Save Drawing", command=self.save_drawing)
        self.button_save.grid(row=5, column=1, pady=5)

        # Prediction history
        self.history_label = tk.Label(self, text="Prediction History:", font=("Helvetica", 12))
        self.history_label.grid(row=6, column=0, columnspan=2, pady=5)
        self.history_box = tk.Listbox(self, height=5, width=40)
        self.history_box.grid(row=7, column=0, columnspan=2, pady=5)

        # Binding mouse
        self.canvas.bind("<B1-Motion>", self.draw_lines)

        # Keyboard shortcuts
        self.bind("<Return>", lambda event: self.classify_handwriting())
        self.bind("<c>", lambda event: self.clear_all())

    def clear_all(self):
        self.canvas.delete("all")
        self.strokes.clear()
        self.label.configure(text="Draw a Digit")

    def undo_last(self):
        if self.strokes:
            last = self.strokes.pop()
            self.canvas.delete(last)

    def classify_handwriting(self):
        HWND = self.canvas.winfo_id()  # get the handle of the canvas
        rect = win32gui.GetWindowRect(HWND)  # get the coordinate of the canvas
        a, b, c, d = rect
        rect = (a+4, b+4, c-4, d-4)
        im = ImageGrab.grab(rect)

        digit, acc = predict_digit(im)
        result_text = f"{digit}, {int(acc*100)}%"
        self.label.configure(text=result_text)
        self.history_box.insert(END, result_text)

    def draw_lines(self, event):
        r = self.pen_size
        item = self.canvas.create_oval(event.x-r, event.y-r, event.x+r, event.y+r,
                                       fill=self.pen_color, outline=self.pen_color)
        self.strokes.append(item)

    def choose_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.pen_color = color

    def save_drawing(self):
        HWND = self.canvas.winfo_id()
        rect = win32gui.GetWindowRect(HWND)
        a, b, c, d = rect
        rect = (a+4, b+4, c-4, d-4)
        im = ImageGrab.grab(rect)
        if not os.path.exists("saved_drawings"):
            os.makedirs("saved_drawings")
        file_path = f"saved_drawings/digit_{len(os.listdir('saved_drawings'))+1}.png"
        im.save(file_path)
        self.history_box.insert(END, f"Saved: {file_path}")

app = App()
app.mainloop()
