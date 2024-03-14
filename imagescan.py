import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np


def open_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        img = Image.open(file_path)
        img.thumbnail((left_pane.winfo_width(), left_pane.winfo_height()))
        photo = ImageTk.PhotoImage(img)
        canvas.image = photo  # keep a reference!
        canvas.create_image(0, 0, anchor='nw', image=photo)


def track_mouse(event):
    x, y = event.x, event.y
    if 0 <= x < canvas.image.width() and 0 <= y < canvas.image.height():
        img = canvas.image._PhotoImage__photo  # Access the PhotoImage object.
        pixels = list(img.getdata(band=0))
        width, height = img.width(), img.height()
        pixels = np.array(pixels).reshape((height, width))

        right_canvas.delete("all")  # Clear previous lines
        for i, pixel in enumerate(pixels[:, x]):
            color = f'#{pixel:02x}{pixel:02x}{pixel:02x}'
            right_canvas.create_line(0, i, right_canvas.winfo_width(), i, fill=color)


app = tk.Tk()
app.geometry("800x600")  # Adjust size to be about 50% of a common desktop

top_frame = tk.Frame(app)
top_frame.pack(side='top', fill='x')

open_image_btn = tk.Button(top_frame, text="Open image", command=open_image)
open_image_btn.pack(side='left')

for _ in range(3):  # Create a few blank buttons
    tk.Button(top_frame, text=" ").pack(side='left', padx=2)

bottom_pane = tk.PanedWindow(app, orient='horizontal')
bottom_pane.pack(fill='both', expand=True)

left_pane = tk.Frame(bottom_pane)
bottom_pane.add(left_pane)

right_pane = tk.Frame(bottom_pane)
bottom_pane.add(right_pane)

canvas = tk.Canvas(left_pane, bg='grey')
canvas.pack(fill='both', expand=True)
canvas.bind("<Motion>", track_mouse)

right_canvas = tk.Canvas(right_pane, bg='white')
right_canvas.pack(fill='both', expand=True)

app.mainloop()
