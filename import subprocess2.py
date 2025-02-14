import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import subprocess
import threading
import queue

def select_audio_file():
    filename = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav")])
    audio_path_var.set(filename)

def select_image_file():
    filename = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    image_path_var.set(filename)

def select_result_dir():
    directory = filedialog.askdirectory()
    result_dir_var.set(directory)

def run_sadtalker():
    audio_path = audio_path_var.get()
    image_path = image_path_var.get()
    result_dir = result_dir_var.get()
    
    if not audio_path or not image_path or not result_dir:
        messagebox.showerror("Error", "Please select all paths.")
        return

    output_text.delete(1.0, tk.END)
    
    command = f'"F:\\anaconda3\\envs\\sadtalker03\\python.exe" "F:\\SadTalker\\SadTalker\\inference.py" --driven_audio "{audio_path}" --source_image "{image_path}" --result_dir "{result_dir}" --still --preprocess full --enhancer gfpgan'

    def run_command():
        try:
            global process
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            stdout, stderr = process.communicate()  # 等待进程结束并收集输出
            
            if process.returncode == 0:
                output_queue.put(stdout)
            else:
                output_queue.put(stderr)
            
            output_queue.put("处理完成。\n" if process.returncode == 0 else "处理失败。\n")
        except Exception as e:
            output_queue.put(f"错误: {e}\n")

    def update_output():
        while not output_queue.empty():
            line = output_queue.get()
            output_text.insert(tk.END, line)
            output_text.yview(tk.END)
        root.after(100, update_output)

    global output_queue
    output_queue = queue.Queue()
    threading.Thread(target=run_command).start()
    root.after(100, update_output)

def stop_process():
    global process
    if process:
        process.terminate()
        process.wait()
        output_text.insert(tk.END, "Process terminated by user.\n")

# 创建主窗口
root = tk.Tk()
root.title("SadTalker GUI")

# 创建并布局组件
tk.Label(root, text="Audio File:").grid(row=0, column=0, padx=5, pady=5)
audio_path_var = tk.StringVar()
tk.Entry(root, textvariable=audio_path_var, width=50).grid(row=0, column=1, padx=5, pady=5)
tk.Button(root, text="Browse", command=select_audio_file).grid(row=0, column=2, padx=5, pady=5)

tk.Label(root, text="Image File:").grid(row=1, column=0, padx=5, pady=5)
image_path_var = tk.StringVar()
tk.Entry(root, textvariable=image_path_var, width=50).grid(row=1, column=1, padx=5, pady=5)
tk.Button(root, text="Browse", command=select_image_file).grid(row=1, column=2, padx=5, pady=5)

tk.Label(root, text="Result Directory:").grid(row=2, column=0, padx=5, pady=5)
result_dir_var = tk.StringVar()
tk.Entry(root, textvariable=result_dir_var, width=50).grid(row=2, column=1, padx=5, pady=5)
tk.Button(root, text="Browse", command=select_result_dir).grid(row=2, column=2, padx=5, pady=5)

tk.Button(root, text="Run", command=run_sadtalker).grid(row=3, column=0, columnspan=3, padx=5, pady=5)
tk.Button(root, text="Stop", command=stop_process).grid(row=4, column=0, columnspan=3, padx=5, pady=5)

output_queue = queue.Queue()
# 添加命令行输出文本框
output_text = scrolledtext.ScrolledText(root, height=10, width=80, wrap=tk.WORD)
output_text.grid(row=5, column=0, columnspan=3, padx=5, pady=5)

root.mainloop()
