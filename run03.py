import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import subprocess

def select_audio():
    filename = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav")])
    if filename:
        audio_entry.delete(0, tk.END)
        audio_entry.insert(0, filename)

def select_image():
    filename = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if filename:
        image_entry.delete(0, tk.END)
        image_entry.insert(0, filename)

def select_result_dir():
    directory = filedialog.askdirectory()
    if directory:
        result_entry.delete(0, tk.END)
        result_entry.insert(0, directory)

def run_script():
    audio_path = audio_entry.get()
    image_path = image_entry.get()
    result_path = result_entry.get()
    
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
        subprocess.run(command, check=True)
        messagebox.showinfo("Success", "Video created successfully!")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

app = tk.Tk()
app.title("SadTalker GUI")

tk.Label(app, text="Audio File:").grid(row=0, column=0, padx=10, pady=5)
audio_entry = tk.Entry(app, width=50)
audio_entry.grid(row=0, column=1, padx=10, pady=5)
tk.Button(app, text="Browse", command=select_audio).grid(row=0, column=2, padx=10, pady=5)

tk.Label(app, text="Image File:").grid(row=1, column=0, padx=10, pady=5)
image_entry = tk.Entry(app, width=50)
image_entry.grid(row=1, column=1, padx=10, pady=5)
tk.Button(app, text="Browse", command=select_image).grid(row=1, column=2, padx=10, pady=5)

tk.Label(app, text="Result Directory:").grid(row=2, column=0, padx=10, pady=5)
result_entry = tk.Entry(app, width=50)
result_entry.grid(row=2, column=1, padx=10, pady=5)
tk.Button(app, text="Browse", command=select_result_dir).grid(row=2, column=2, padx=10, pady=5)

tk.Button(app, text="Run", command=run_script).grid(row=3, column=1, pady=20)

app.mainloop()
