import tkinter as tk
from tkinter import filedialog
import requests
import os

# 假设的 TTS API URL 和 API 密钥
API_URL = 'https://api.example.com/tts'
API_KEY = 'your_api_key_here'

def choose_file():
    # 创建文件对话框选择文件
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    file_path = filedialog.askopenfilename(title="选择文本文档", filetypes=[("Text files", "*.txt")])
    return file_path

def save_audio(response, filename):
    # 将 API 返回的音频数据保存为文件
    with open(filename, 'wb') as f:
        f.write(response.content)

def text_to_speech(text, language='en', voice='default'):
    # 使用 TTS API 将文本转换为音频
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json',
    }
    data = {
        'text': text,
        'language': language,
        'voice': voice
    }
    response = requests.post(API_URL, headers=headers, json=data)
    
    if response.status_code == 200:
        return response
    else:
        print("错误:", response.status_code, response.text)
        return None

def main():
    # 选择文本文档
    file_path = choose_file()
    if not file_path:
        print("没有选择文本文档。")
        return

    # 选择角色（语言和声音）
    language = 'en'  # 默认使用英语
    voice = 'default'  # 默认声音
    print("请输入角色（语言代码，例如 'en'、'es'）：")
    language = input().strip() or language
    print("请输入声音类型（例如 'default'）：")
    voice = input().strip() or voice

    # 读取文本文件
    with open(file_path, 'r') as file:
        text = file.read()

    # 将文本转换为音频
    response = text_to_speech(text, language, voice)
    if not response:
        print("文本转语音失败。")
        return

    # 选择保存音频文件的路径
    save_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3")])
    if not save_path:
        print("没有选择保存路径。")
        return

    # 保存音频文件
    save_audio(response, save_path)
    print("音频文件已保存到：", save_path)

if __name__ == '__main__':
    main()
