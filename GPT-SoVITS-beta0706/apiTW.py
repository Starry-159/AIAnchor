import os
import subprocess
import requests
import logging

def run_batch_file(batch_file_path):
    """运行指定的batch文件"""
    try:
        # 运行 batch 文件
        subprocess.run(batch_file_path, check=True, shell=True)
        logging.info(f"Successfully ran: {batch_file_path}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to run {batch_file_path}: {e}")
        raise

def read_txt_file(file_path):
    """读取txt文件并返回每一行的列表"""
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
    return [line.strip() for line in lines]

def text_to_speech_api(
    api_url, refer_wav_path, prompt_text, prompt_language, text, text_language, cut_punc
):
    """调用TTS API，将文本转换为音频"""
    params = {
        "refer_wav_path": refer_wav_path,
        "prompt_text": prompt_text,
        "prompt_language": prompt_language,
        "text": text,
        "text_language": text_language,
        "cut_punc": cut_punc,
    }
    try:
        response = requests.get(api_url, params=params, timeout=10)
        response.raise_for_status()
        return response.content
    except requests.RequestException as e:
        raise Exception(f"API请求失败: {e}")

def save_audio_file(audio_content, output_path):
    """将音频内容保存为文件"""
    with open(output_path, "wb") as audio_file:
        audio_file.write(audio_content)

def convert_texts_to_wav(
    input_txt_path,
    output_dir,
    api_url,
    refer_wav_path=None,
    prompt_text=None,
    prompt_language=None,
    text_language=None,
    cut_punc=None,
):
    """读取txt文件，将每行文本转换为音频并保存为wav文件"""
    os.makedirs(output_dir, exist_ok=True)

    lines = read_txt_file(input_txt_path)

    for i, line in enumerate(lines):
        if line:  # 忽略空行
            logging.info(f"Processing line {i+1}: {line}")
            try:
                audio_content = text_to_speech_api(
                    api_url,
                    refer_wav_path,
                    prompt_text,
                    prompt_language,
                    line,
                    text_language,
                    cut_punc,
                )
                output_path = os.path.join(output_dir, f"line_{i+1}.wav")
                save_audio_file(audio_content, output_path)
                logging.info(f"Saved: {output_path}")
            except Exception as e:
                logging.error(f"Failed to process line {i+1}: {e}")

# 设置日志配置
logging.basicConfig(level=logging.INFO)

# 运行 batch 文件
batch_file_path = "F:\\AIAnchor\\GPT-SoVITS-beta0706\\api.bat"
run_batch_file(batch_file_path)

# 执行文本转换
input_txt_path = "F:\\AIAnchor\\GPT-SoVITS-beta0706\\test\\测试用.txt"
output_dir = "F:\\AIAnchor\\GPT-SoVITS-beta0706\\test"
api_url = "http://127.0.0.1:9880"

convert_texts_to_wav(
    input_txt_path,
    output_dir,
    api_url,
    refer_wav_path="F:\\AIAnchor\\GPT-SoVITS-beta0706\\trained_models\\Hang_vocal\\参考音频_还体现出管理能力，对于活性染料染色缸差的控制。.wav",
    prompt_text="还体现出管理能力，对于活性染料染色缸差的控制。",
    prompt_language="中文",
    text_language="中文",
    cut_punc="，",
)
