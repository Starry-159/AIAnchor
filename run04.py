import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import subprocess
import os
import signal

class SadTalkerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SadTalker GUI")
        
        # Variables to hold file paths
        self.audio_path = tk.StringVar()
        self.image_path = tk.StringVar()
        self.result_path = tk.StringVar()

        # Create and place widgets
        self.create_widgets()
        
        # Variable to hold reference to the running process
        self.process = None

    def create_widgets(self):
        tk.Label(self.root, text="Audio File:").grid(row=0, column=0, padx=10, pady=5)
        tk.Entry(self.root, textvariable=self.audio_path, width=50).grid(row=0, column=1, padx=10, pady=5)
        tk.Button(self.root, text="Browse", command=self.select_audio).grid(row=0, column=2, padx=10, pady=5)

        tk.Label(self.root, text="Image File:").grid(row=1, column=0, padx=10, pady=5)
        tk.Entry(self.root, textvariable=self.image_path, width=50).grid(row=1, column=1, padx=10, pady=5)
        tk.Button(self.root, text="Browse", command=self.select_image).grid(row=1, column=2, padx=10, pady=5)

        tk.Label(self.root, text="Result Directory:").grid(row=2, column=0, padx=10, pady=5)
        tk.Entry(self.root, textvariable=self.result_path, width=50).grid(row=2, column=1, padx=10, pady=5)
        tk.Button(self.root, text="Browse", command=self.select_result_dir).grid(row=2, column=2, padx=10, pady=5)

        tk.Button(self.root, text="Run", command=self.run_script).grid(row=3, column=1, pady=20)
        tk.Button(self.root, text="Stop", command=self.stop_script).grid(row=3, column=2, pady=20)

    def select_audio(self):
        filename = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav")])
        if filename:
            self.audio_path.set(filename)

    def select_image(self):
        filename = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if filename:
            self.image_path.set(filename)

    def select_result_dir(self):
        directory = filedialog.askdirectory()
        if directory:
            self.result_path.set(directory)

    def run_script(self):
        audio_path = self.audio_path.get()
        image_path = self.image_path.get()
        result_path = self.result_path.get()
        
        if not (audio_path and image_path and result_path):
            messagebox.showerror("Error", "Please select all required files and directories.")
            return
        
        command = [
            "F:\\anaconda3\\envs\\sadtalker03\\python.exe",
            "F:\\SadTalker\\SadTalker\\inference.py",
            "--driven_audio", audio_path,
            "--source_image", image_path,
            "--result_dir", result_path,
            "--still",
            "--preprocess", "full",
            "--enhancer", "gfpgan"
        ]
        
        try:
            # Run the command
            self.process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            self.root.after(1000, self.check_process)
            messagebox.showinfo("Running", "Script is running...")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def check_process(self):
        if self.process.poll() is None:
            # Read output and error streams
            stdout, stderr = self.process.communicate(timeout=1)
            if stdout:
                print(f"STDOUT: {stdout}")
            if stderr:
                print(f"STDERR: {stderr}")

            self.root.after(1000, self.check_process)  # Check again in 1 second
        else:
            messagebox.showinfo("Finished", "Video creation completed or failed.")
            self.process = None


    def stop_script(self):
        if self.process:
            self.process.terminate()
            self.process = None
            messagebox.showinfo("Stopped", "Process has been terminated.")

if __name__ == "__main__":
    root = tk.Tk()
    app = SadTalkerApp(root)
    root.mainloop()
