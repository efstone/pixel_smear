import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np


class ImageApp:
    def __init__(self, root):
        self.root = root
        self.setup_ui()
        self.img = None  # This will hold the PIL Image object

    def setup_ui(self):
        self.root.geometry("800x600")  # Adjust size to be about 50% of a common desktop

        top_frame = tk.Frame(self.root)
        top_frame.pack(side='top', fill='x')

        open_image_btn = tk.Button(top_frame, text="Open image", command=self.open_image)
        open_image_btn.pack(side='left')

        # for _ in range(3):  # Create a few blank buttons
        #     tk.Button(top_frame, text=" ").pack(side='left', padx=2)

        bottom_pane = tk.PanedWindow(self.root, orient='horizontal')
        bottom_pane.pack(fill='both', expand=True)

        self.left_pane = tk.Frame(bottom_pane)
        bottom_pane.add(self.left_pane)

        self.right_pane = tk.Frame(bottom_pane)
        bottom_pane.add(self.right_pane)

        self.canvas = tk.Canvas(self.left_pane, bg='grey')
        self.canvas.pack(fill='both', expand=True)

        self.right_canvas = tk.Canvas(self.right_pane, bg='black')
        self.right_canvas.pack(fill='both', expand=True)
        self.canvas.bind("<Motion>", self.track_mouse)

    def open_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.img = Image.open(file_path)
            self.img.thumbnail((self.left_pane.winfo_width(), self.left_pane.winfo_height()))
            photo = ImageTk.PhotoImage(self.img)
            self.canvas.image = photo  # keep a reference!
            self.canvas.create_image(0, 0, anchor='nw', image=photo)

    def track_mouse(self, event):
        if self.img:
            x, y = event.x, event.y
            if 0 <= x < self.img.width and 0 <= y < self.img.height:
                pixels = np.array(self.img.convert('RGB'))
                self.right_canvas.delete("all")  # Clear previous lines
                for i, pixel in enumerate(pixels[:, x]):
                    color = f'#{pixel[0]:02x}{pixel[1]:02x}{pixel[2]:02x}'
                    self.right_canvas.create_line(0, i, self.right_canvas.winfo_width(), i, fill=color)


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageApp(root)
    root.mainloop()
