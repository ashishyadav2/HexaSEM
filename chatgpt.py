import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2

root = tk.Tk()
root.title("Steganography")

# Function to open an image file and display it on the canvas
def open_image():
    file_path = filedialog.askopenfilename(title="Select Image",
                                           filetypes=(("PNG files", "*.png"), ("JPEG files", "*.jpg")))
    global image
    image = Image.open(file_path)
    image.thumbnail((500, 500))
    photo = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, anchor=tk.NW, image=photo)
    canvas.image = photo

# Function to open a video file and display its first frame on the canvas
def open_video():
    file_path = filedialog.askopenfilename(title="Select Video",
                                           filetypes=(("MP4 files", "*.mp4"), ("AVI files", "*.avi")))
    global video
    video = cv2.VideoCapture(file_path)
    ret, frame = video.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = Image.fromarray(frame)
        frame.thumbnail((500, 500))
        photo = ImageTk.PhotoImage(frame)
        canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        canvas.image = photo

# Function to hide a message in an image
def hide_message_in_image():
    message = message_entry.get()
    if not message:
        return
    pixels = image.load()
    width, height = image.size
    index = 0
    for i in range(width):
        for j in range(height):
            r, g, b = pixels[i, j]
            if index < len(message):
                ascii_value = ord(message[index])
                r = (r & 254) | (ascii_value & 1)
                index += 1
            pixels[i, j] = (r, g, b)
    image.save("image_with_message.png")
    message_entry.delete(0, tk.END)
    canvas.delete("all")
    canvas.create_text(250, 250, text="Message hidden in image successfully.")

# Function to hide a message in a video
def hide_message_in_video():
    message = message_entry.get()
    if not message:
        return
    codec = cv2.VideoWriter_fourcc(*"mp4v")
    video_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    video_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(video.get(cv2.CAP_PROP_FPS))
    out = cv2.VideoWriter("video_with_message.mp4", codec, fps, (video_width, video_height))
    index = 0
    while True:
        ret, frame = video.read()
        if not ret:
            break
        if index < len(message):
            ascii_value = ord(message[index])
            pixel = list(frame[0, 0])
            pixel[0] = (pixel[0] & 254) | (ascii_value & 1)
            frame[0, 0] = pixel
            index += 1
        out.write(frame)
    video.release()
    out.release()
    message_entry.delete(0, tk.END)
    canvas.delete("all")
    canvas.create_text(250, 250, text="Message hidden in video successfully.")

# Function to extract a message from an image or a video
def extract_message():
    file_path = filedialog.askopenfilename(title="Select Image or Video",
                                           filetypes=(("PNG files", "*.png"), ("JPEG files", "*.jpg"),
                                                      ("MP4 files", "*.mp4"), ("AVI files", "*.avi")))
    if file_path.endswith(".mp4") or file_path.endswith(".avi"):
        video = cv2.VideoCapture(file_path)
        message = ""
        while True:
            ret, frame = video.read()
            if not ret:
                break
            pixel = list(frame[0, 0])
            message += str(pixel[0] & 1)
            if len(message) == 8:
                ascii_value = int(message, 2)
                if ascii_value == 0:
                    break
                message += chr(ascii_value)
                if message[-1] == "\x00":
                    message = message[:-1]
                message += ""
        video.release()
        canvas.delete("all")
        canvas.create_text(250, 250, text=message)
    else:
        image = Image.open(file_path)
        pixels = image.load()
        width, height = image.size
        message = ""
        for i in range(width):
            for j in range(height):
                r, g, b = pixels[i, j]
                message += str(r & 1)
                if len(message) == 8:
                    ascii_value = int(message, 2)
                    if ascii_value == 0:
                        break
                    message += chr(ascii_value)
                    if message[-1] == "\x00":
                        message = message[:-1]
                    message += ""
            if len(message) >= 8 and message[-8:] == "\x00" * 8:
                message = message[:-8]
                break
        image.save("extracted_message.png")
        canvas.delete("all")
        canvas.create_text(250, 250, text=message)

# Create the GUI
canvas = tk.Canvas(root, width=500, height=500)
canvas.pack(side=tk.LEFT)

message_label = tk.Label(root, text="Message:")
message_label.pack()

message_entry = tk.Entry(root)
message_entry.pack()

open_image_button = tk.Button(root, text="Open Image", command=open_image)
open_image_button.pack()

open_video_button = tk.Button(root, text="Open Video", command=open_video)
open_video_button.pack()

hide_message_in_image_button = tk.Button(root, text="Hide Message in Image", command=hide_message_in_image)
hide_message_in_image_button.pack()

hide_message_in_video_button = tk.Button(root, text="Hide Message in Video", command=hide_message_in_video)
hide_message_in_video_button.pack()

extract_message_button = tk.Button(root, text="Extract Message", command=extract_message)
extract_message_button.pack()

root.mainloop()

