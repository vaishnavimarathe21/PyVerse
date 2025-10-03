import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class FaceDetectionApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Face Detection App")
        self.geometry("600x600")

        # Load button
        self.load_btn = tk.Button(self, text="Upload Image", command=self.load_image)
        self.load_btn.pack(pady=10)

        # Detect button
        self.detect_btn = tk.Button(self, text="Detect Faces", command=self.detect_faces, state=tk.DISABLED)
        self.detect_btn.pack(pady=10)

        # Image label
        self.image_label = tk.Label(self)
        self.image_label.pack()

        self.original_image = None
        self.processed_image = None
        self.file_path = None

        # Haar Cascade (built-in OpenCV)
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def load_image(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.png *.jpeg")])
        if not self.file_path:
            return

        # Load with OpenCV
        img = cv2.imread(self.file_path)
        if img is None:
            messagebox.showerror("Error", "Could not read the image!")
            return

        self.original_image = img
        self.display_image(img)
        self.detect_btn.config(state=tk.NORMAL)

    def display_image(self, img_cv2):
        # Convert from cv2 BGR to PIL RGB
        img_rgb = cv2.cvtColor(img_cv2, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)

        # Resize for Tkinter window
        img_pil.thumbnail((500, 500))
        img_tk = ImageTk.PhotoImage(img_pil)

        self.image_label.configure(image=img_tk)
        self.image_label.image = img_tk

    def detect_faces(self):
        if self.original_image is None:
            messagebox.showwarning("Warning", "Please upload an image first!")
            return

        gray = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        img_copy = self.original_image.copy()
        for (x, y, w, h) in faces:
            cv2.rectangle(img_copy, (x, y), (x+w, y+h), (255, 0, 0), 2)

        self.display_image(img_copy)

        messagebox.showinfo("Detection Complete", f"Faces found: {len(faces)}")

if __name__ == "__main__":
    app = FaceDetectionApp()
    app.mainloop()
