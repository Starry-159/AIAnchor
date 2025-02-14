import subprocess
import os

# 测试
gpt_model_path = r'F:\AIAnchor\Input\GPT-SoVITS_Input\models\Hang_vocal\音色_1\Hang-e15.ckpt'
sovits_model_path = r'F:\AIAnchor\Input\GPT-SoVITS_Input\models\Hang_vocal\音色_1\Hang_e8_s96.pth' 
ref_audio_path = r'F:\AIAnchor\Input\GPT-SoVITS_Input\models\Hang_vocal\音色_1\语气_1\参考音频_还体现出管理能力，对于活性染料染色缸差的控制。.wav'
ref_text_path = r'F:\AIAnchor\Input\GPT-SoVITS_Input\models\Hang_vocal\音色_1\语气_1\参考音频内容.txt'
ref_language = '中文'
target_text_path = r'F:\AIAnchor\Input\GPT-SoVITS_Input\文本\测试用.txt'
target_language_path = '中文'
output_path = r'F:\AIAnchor\Output\GPT-SoVITS_Output'
driven_audio = r'F:\AIAnchor\Output\GPT-SoVITS_Output\output.wav'
source_image = r'F:\AIAnchor\Input\SadTalker_Input\Hang\Hang2.png'
result_dir = r'F:\AIAnchor\Output\SadTalker_Output'
preprocess = 'full'
enhancer = 'gfpgan'

def run_command_GSV(gpt_model_path, sovits_model_path, ref_audio_path, ref_text_path, ref_language, target_text_path, target_language_path, output_path):
    # GPT-SoVITS目录和命令
    work_dir = r'F:\AIAnchor\GPT-SoVITS-beta0706'
    cmd = [
        r'F:\AIAnchor\GPT-SoVITS-beta0706\runtime\python.exe',
        r'F:\AIAnchor\GPT-SoVITS-beta0706\GPT_SoVITS\inference_cli.py',
        '--gpt_model', gpt_model_path,
        '--sovits_model', sovits_model_path,
        '--ref_audio', ref_audio_path,
        '--ref_text', ref_text_path,
        '--ref_language', ref_language,
        '--target_text', target_text_path,
        '--target_language', target_language_path,
        '--output_path', output_path
    ]

    # 运行GPT-SoVITS命令
    os.chdir(work_dir)
    subprocess.run(cmd, check=True)



def run_command_SD(driven_audio, source_image, result_dir, preprocess, enhancer):

    # SadTalker目录和命令
    work_dir = r'F:\AIAnchor\SadTalker'
    cmd = [
        r'F:\anaconda3\envs\sadtalker03\python.exe',
        r'F:\AIAnchor\SadTalker\inference.py',
        '--driven_audio', driven_audio,
        '--source_image', source_image,
        '--result_dir', result_dir,
        '--still',
        '--preprocess', preprocess,
        '--enhancer', enhancer
    ]


    # 运行SadTalker命令
    os.chdir(work_dir)
    subprocess.run(cmd, check=True)

if __name__ == "__main__":
    run_command_GSV(gpt_model_path, sovits_model_path, ref_audio_path, ref_text_path, ref_language, target_text_path, target_language_path, output_path)
    run_command_SD(driven_audio, source_image, result_dir, preprocess, enhancer)
