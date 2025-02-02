import os
import base64
from hashlib import sha256
from tkinter import Tk, Label, filedialog, Frame, Entry, messagebox, Canvas, PhotoImage, LEFT, RIGHT, BOTH
from tkinter import ttk
from ttkthemes import ThemedTk
from PIL import Image, ImageTk
import io
import cv2
import numpy as np

class DecryptionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Photos App")
        self.root.geometry("1000x800")

        self.init_ui()

    def init_ui(self):
        self.style = ttk.Style()
        self.style.theme_use('equilux')  # A polished theme
        self.style.configure('TFrame', background='#08012b', relief="flat")  # Dark background
        self.style.configure('Custom.TButton', font=('Helvetica', 12), borderwidth=0, background='red', foreground='white')  # Updated button background
        self.style.configure('TLabel', font=('Helvetica', 12), background='#08012b', foreground='white')
        self.style.configure('TEntry', font=('Helvetica', 12), background='white', foreground='white')
        self.style.map('Custom.TButton', background=[('active', '#08012b'), ('!disabled', '#08012b')], foreground=[('active', 'white'), ('!disabled', 'white')])

        self.frame = ttk.Frame(self.root, style='TFrame', relief='flat', padding=10)
        self.frame.pack(fill=BOTH, expand=True, padx=0, pady=0)

        self.top_frame = ttk.Frame(self.frame, style='TFrame')
        self.top_frame.pack(fill=BOTH, pady=10)

        self.key_label = ttk.Label(self.top_frame, text="Enter your decryption key:", style='TLabel')
        self.key_label.pack(side=LEFT, padx=5)

        self.key_entry = ttk.Entry(self.top_frame, show="*", style='TEntry')
        self.key_entry.pack(side=LEFT, padx=5, fill=BOTH, expand=True)

        self.key_button = ttk.Button(self.top_frame, text="Submit Key and Browse Folder", command=self.submit_key, style='Custom.TButton')
        self.key_button.pack(side=LEFT, padx=5)

        self.canvas_frame = ttk.Frame(self.frame, style='TFrame', relief="flat", borderwidth=0)  # Removed border
        self.canvas_frame.pack(fill=BOTH, expand=True)

        self.canvas = Canvas(self.canvas_frame, relief="flat", bd=0, background='#08012b', borderwidth=0)
        self.canvas.pack(fill=BOTH, expand=True)
        self.canvas_image = None

        self.file_name_label = ttk.Label(self.frame, text="", style='TLabel')
        self.file_name_label.pack(pady=5)

        self.prev_icon = self.create_transparent_image('img\\prev_arrow.png')  # Ensure you have these image files in the same directory
        self.next_icon = self.create_transparent_image('img\\next_arrow.png')

        self.prev_button = ttk.Button(self.frame, image=self.prev_icon, command=self.show_prev, style='Custom.TButton')
        self.prev_button.place(relx=0.01, rely=0.5, anchor='w')

        self.next_button = ttk.Button(self.frame, image=self.next_icon, command=self.show_next, style='Custom.TButton')
        self.next_button.place(relx=0.99, rely=0.5, anchor='e')

        self.files = []
        self.current_index = -1
        self.key = None

    def create_transparent_image(self, image_path):
        img = Image.open(image_path).convert("RGBA")
        datas = img.getdata()

        new_data = []
        for item in datas:
            if item[0] == 255 and item[1] == 255 and item[2] == 255:  # Check for white color
                new_data.append((255, 255, 255, 0))  # Replace white with transparent
            else:
                new_data.append(item)

        img.putdata(new_data)
        return ImageTk.PhotoImage(img)

    def pad(self, data):
        return data + b"\0" * (16 - len(data) % 16)

    def decrypt_data(self, data):
        key = sha256(self.key.encode()).digest()  # Ensure key is 32 bytes long
        decrypted_data = bytearray()

        for i in range(0, len(data), 16):
            block = data[i:i+16]
            decrypted_block = bytearray([b ^ k for b, k in zip(block, key[:16])])
            decrypted_data.extend(decrypted_block)

        decrypted_data = decrypted_data.rstrip(b"\0")
        return decrypted_data

    def open_image(self, data):
        img = Image.open(io.BytesIO(data))
        img.thumbnail((1024, 768))
        img = ImageTk.PhotoImage(img)
        self.canvas.create_image(self.canvas.winfo_width() // 2, self.canvas.winfo_height() // 2, anchor='center', image=img)
        self.canvas_image = img

    def open_video(self, data):
        video_file = 'temp_video.mp4'
        with open(video_file, 'wb') as f:
            f.write(data)
        cap = cv2.VideoCapture(video_file)
        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img_pil = Image.fromarray(frame_rgb)
                img_tk = ImageTk.PhotoImage(image=img_pil)
                self.canvas.create_image(self.canvas.winfo_width() // 2, self.canvas.winfo_height() // 2, anchor='center', image=img_tk)
                self.canvas.image = img_tk
                self.root.update_idletasks()
                self.root.after(10)  # Delay for 10 milliseconds
            else:
                break
        cap.release()
        os.remove(video_file)

    def clear_canvas(self):
        self.canvas.delete("all")
        self.canvas_image = None

    def browse_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.files = []
            self.current_index = -1
            self.clear_canvas()
            self.file_name_label.config(text="")

            for root, dirs, files in os.walk(folder_path):
                for filename in files:
                    if filename.lower().endswith(('png', 'jpg', 'jpeg', 'gif', 'bmp', 'mp4', 'avi', 'mkv', 'mov')):
                        input_file = os.path.join(root, filename)
                        with open(input_file, 'rb') as f:
                            encrypted_data = f.read()
                        self.files.append((input_file, encrypted_data))
            if self.files:
                self.current_index = 0
                self.show_file()

    def show_file(self):
        self.clear_canvas()
        if self.files:
            file_path, encrypted_data = self.files[self.current_index]
            decrypted_data = self.decrypt_data(encrypted_data)
            if file_path.lower().endswith(('png', 'jpg', 'jpeg', 'gif', 'bmp')):
                self.open_image(decrypted_data)
            elif file_path.lower().endswith(('mp4', 'avi', 'mkv', 'mov')):
                self.open_video(decrypted_data)
            self.file_name_label.config(text=os.path.basename(file_path))

    def show_prev(self):
        if self.files and self.current_index > 0:
            self.current_index -= 1
            self.show_file()

    def show_next(self):
        if self.files and self.current_index < len(self.files) - 1:
            self.current_index += 1
            self.show_file()

    def submit_key(self):
        self.key = self.key_entry.get()
        if not self.key:
            messagebox.showerror("Error", "Please enter a decryption key.")
            return
        self.browse_folder()

def create_app():
    root = ThemedTk(theme="equilux")  # Using ThemedTk to apply a polished theme
    style = ttk.Style(root)
    style.configure('Transparent.TButton', background='#08012b', borderwidth=0)  # Transparent button style
    app = DecryptionApp(root)
    root.mainloop()

# Run the app
create_app()
