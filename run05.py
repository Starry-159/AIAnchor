import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os
import threading
import signal

class SadTalkerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SadTalker GUI")

        # Variables to hold file paths
        self.audio_file = tk.StringVar()
        self.image_file = tk.StringVar()
        self.result_dir = tk.StringVar()

        # Create and place widgets
        tk.Label(root, text="Audio File").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(root, textvariable=self.audio_file, width=50).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(root, text="Browse", command=self.browse_audio).grid(row=0, column=2, padx=10, pady=10)

        tk.Label(root, text="Image File").grid(row=1, column=0, padx=10, pady=10)
        tk.Entry(root, textvariable=self.image_file, width=50).grid(row=1, column=1, padx=10, pady=10)
        tk.Button(root, text="Browse", command=self.browse_image).grid(row=1, column=2, padx=10, pady=10)

        tk.Label(root, text="Result Directory").grid(row=2, column=0, padx=10, pady=10)
        tk.Entry(root, textvariable=self.result_dir, width=50).grid(row=2, column=1, padx=10, pady=10)
        tk.Button(root, text="Browse", command=self.browse_result_dir).grid(row=2, column=2, padx=10, pady=10)

        tk.Button(root, text="Start", command=self.start_sadtalker).grid(row=3, column=0, columnspan=3, pady=20)
        tk.Button(root, text="Stop", command=self.stop_sadtalker).grid(row=4, column=0, columnspan=3, pady=20)

        self.process = None
        self.process_thread = None

    def browse_audio(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav")])
        if file_path:
            self.audio_file.set(file_path)

    def browse_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.image_file.set(file_path)

    def browse_result_dir(self):
        dir_path = filedialog.askdirectory()
        if dir_path:
            self.result_dir.set(dir_path)

    def start_sadtalker(self):
        audio = self.audio_file.get()
        image = self.image_file.get()
        result_dir = self.result_dir.get()

        if not all([audio, image, result_dir]):
            messagebox.showerror("Error", "Please provide all the required files and directory.")
            return

        command = [
            "F:\\anaconda3\\envs\\sadtalker03\\python.exe",
            "F:\\SadTalker\\SadTalker\\inference.py",
            "--driven_audio", audio,
            "--source_image", image,
            "--result_dir", result_dir,
            "--still",
            "--preprocess", "full",
            "--enhancer", "gfpgan"
        ]

        self.process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.process_thread = threading.Thread(target=self.monitor_process)
        self.process_thread.start()

    def stop_sadtalker(self):
        if self.process:
            self.process.terminate()
            self.process = None
            self.process_thread.join()
            messagebox.showinfo("Info", "SadTalker process stopped.")

    def monitor_process(self):
        while True:
            output = self.process.stdout.readline()
            if output == b'' and self.process.poll() is not None:
                break
            if output:
                print(output.decode().strip())

if __name__ == "__main__":
    root = tk.Tk()
    app = SadTalkerApp(root)
    root.mainloop()
