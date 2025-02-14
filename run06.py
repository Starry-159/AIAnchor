import re
import os
import datetime
import subprocess



def read_text_from_file(text_file_path):
    """
    从指定的文本文件读取内容。
    
    参数:
    file_path (str): 文本文件的路径。
    
    返回:
    str: 文件中的文本内容。
    """
    with open(text_file_path, 'r', encoding='utf-8') as file:
        return file.read()
    


def auto_split_text(text, max_length=None, custom_delimiters=None, preserve_delimiters=True, handle_newlines=True):
    """
    将文本按指定标点符号自动分段，并根据需要进一步分割长句子。
    
    参数:
    text (str): 需要分段的原始文本。
    max_length (int, optional): 每个段落的最大字符长度。默认不限制。
    custom_delimiters (str, optional): 自定义的句末分隔符，默认为中文的句号、问号、感叹号等。
    preserve_delimiters (bool): 是否保留分隔符在每个段落的末尾。默认保留。
    handle_newlines (bool): 是否在分段时处理换行符，将其视为分段标志。默认处理。
    
    返回:
    List[str]: 分段后的文本列表。
    """
    
    # 默认的中文句末标点符号
    default_delimiters = '。！？'
    
    # 使用自定义分隔符，或者默认的句末分隔符
    delimiters = custom_delimiters if custom_delimiters else default_delimiters
    
    # 根据用户选择，决定是否保留分隔符
    if preserve_delimiters:
        split_pattern = rf'(?<=[{delimiters}])'
    else:
        split_pattern = rf'[{delimiters}]'
    
    # 按照标点符号分割文本
    sentences = re.split(split_pattern, text)
    
    # 去除空白段落，并且去掉多余的空格
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
    
    # 如果需要处理换行符，将其视为分段标志
    if handle_newlines:
        expanded_sentences = []
        for sentence in sentences:
            expanded_sentences.extend(sentence.splitlines())
        sentences = [sentence.strip() for sentence in expanded_sentences if sentence.strip()]
    
    # 初始化存储最终段落的列表
    paragraphs = []
    current_paragraph = ''
    
    # 根据最大段落长度控制分段
    for sentence in sentences:
        if max_length is None or len(current_paragraph) + len(sentence) <= max_length:
            current_paragraph += sentence
        else:
            if current_paragraph:
                paragraphs.append(current_paragraph.strip())
            current_paragraph = sentence
    
    # 添加最后一个段落
    if current_paragraph:
        paragraphs.append(current_paragraph.strip())
    
    return paragraphs
    


def save_paragraphs_to_files(paragraphs, folder_path):
    """
    将段落保存为txt文件，依次命名为1、2、3等等。
    
    参数:
    paragraphs (List[str]): 需要保存的段落列表。
    folder_path (str): 文件夹目录路径。
    """
    # 确保文件夹存在
    os.makedirs(folder_path, exist_ok=True)
    
    for i, paragraph in enumerate(paragraphs, start=1):
        file_path = os.path.join(folder_path, f'{i}.txt')
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(paragraph)


def create_output_folder(timestamp, base_folder, file_name):
    """创建以文件名和当前时间结合的文件夹。"""
    folder_name = f"{os.path.splitext(file_name)[0]}_{timestamp}"
    folder_path = os.path.join(base_folder, folder_name)
    os.makedirs(folder_path, exist_ok=True)
    return folder_path


def create_Zi_folder(base_folder, file_name):
    # 用于存放SadTalker生成的一系列不同人物的视频的文件夹

    # 创建完整的文件夹路径
    new_folder_path = os.path.join(base_folder, file_name)

    # 创建文件夹（如果不存在）
    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)
        print(f'文件夹已创建: {new_folder_path}')
    else:
        print(f'文件夹已存在: {new_folder_path}')
    return new_folder_path

# 实现分段功能的程序
def Paragraph(Paragraphs_output_path, text_file_path, max_length=None, custom_delimiters=None, preserve_delimiters=True, handle_newlines=True):
    # 从文本文件读取内容
    text = read_text_from_file(text_file_path)

    # 自动分段（指定自定义分隔符并保留分隔符）
    paragraphs_custom_delimiter = auto_split_text(text, max_length=10, preserve_delimiters=True)

    print("\n使用自定义分隔符且保留分隔符的分段结果：")
    for i, para in enumerate(paragraphs_custom_delimiter):
        print(f"段落 {i+1}: {para}")

    # 保存段落到txt文件
    save_paragraphs_to_files(paragraphs_custom_delimiter, Paragraphs_output_path)

    print(f"段落已保存到文件夹：{Paragraphs_output_path}")


def run_command_GSV(GSV_work_dir, gpt_model_path, sovits_model_path, ref_audio_path, ref_text_path, ref_language, target_text_path, target_language_path, GSV_output_path):


    
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
        '--output_path', GSV_output_path
    ]

    # 运行GPT-SoVITS命令
    os.chdir(GSV_work_dir)
    subprocess.run(cmd, check=True)
   


def run_command_SD(SD_work_dir, driven_audio, source_image, SD_output_path, preprocess, enhancer):

    
    cmd = [
        r'F:\anaconda3\envs\sadtalker03\python.exe',
        r'F:\AIAnchor\SadTalker\inference.py',
        '--driven_audio', driven_audio,
        '--source_image', source_image,
        '--result_dir', SD_output_path,
        '--still',
        '--preprocess', preprocess,
        '--enhancer', enhancer
    ]


    # 运行SadTalker命令
    os.chdir(SD_work_dir)
    subprocess.run(cmd, check=True)


# 获取GPT模型人物音色(person)路径
def get_gpt_model_path(code):
    return gpt_model_paths.get(code, "GPT模型人物音色(person)路径未找到")

# 获取SoVITS模型人物音色(person)路径
def get_sovits_model_path(code):
    return sovits_model_paths.get(code, "SoVITS模型人物音色(person)路径未找到")

# 获取人物参考音频（语气）(emotion)路径
def get_ref_audio_path(code):
    return ref_audio_paths.get(code, "人物参考音频（语气）(emotion)路径未找到")

# 获取人物参考音频（语气）(emotion)内容路径
def get_ref_text_path(code):
    return ref_text_paths.get(code, "人物参考音频（语气）(emotion)内容路径未找到")

# 获取人物图像路径
def get_source_image(code):
    return source_images.get(code, "人物图像路径未找到")





# 测试
# text
text_file_path = r'F:\AIAnchor\Input\Paragraphs_Input\test.txt'

# Paragraphs
base_Paragraphs_output_path = r'F:\AIAnchor\Output\Paragraphs_Output'





# GPT-SoVITS

# GPT-SoVITS目录
GSV_work_dir = r'F:\AIAnchor\GPT-SoVITS-beta0706'

# GPT-SoVITS参数

# 定义“GPT模型人物音色(person)”路径字典
gpt_model_paths = {
    'HuTao_1': 'F:\\AIAnchor\\Input\\models\\HuTao\\voice_1\\hutao-e75.ckpt',
    'HuaHuo_1': "F:\\AIAnchor\\Input\\models\\HuaHuo\\voice_1\\huahuo-e100.ckpt"
    # 添加其他GPT模型路径
}

# 定义“SoVITS模型人物音色(person)”路径字典
sovits_model_paths = {
    'HuTao_1': "F:\\AIAnchor\\Input\\models\\HuTao\\voice_1\\hutao_e60_s3360.pth",
    'HuaHuo_1': r"F:\AIAnchor\Input\models\HuaHuo\voice_1\huahuo_e100_s1100.pth"
    # 添加其他SoVITS模型路径
}

# 定义“人物参考音频（语气）(emotion)”路径字典
ref_audio_paths = {
    'HuTao_1_1': "F:\\AIAnchor\\Input\\models\\HuTao\\voice_1\\emotion_1\\参考音频_村里的气氛还不错，我随便转转就有了诗性。.wav",
    'HuaHuo_1_1': r"F:\AIAnchor\Input\models\HuaHuo\voice_1\emotion_1\参考音频_哎呀，别板着脸嘛～还一本正经地引经据典，干嘛这么严肃？.wav",
    # 添加其他人物参考音频（语气）路径
}

# 定义“人物参考音频（语气）(emotion)”路径字典
ref_text_paths = {
    'HuTao_1_1': "F:\\AIAnchor\\Input\\models\\HuTao\\voice_1\\emotion_1\\参考音频内容.txt",
    'HuaHuo_1_1': r"F:\AIAnchor\Input\models\HuaHuo\voice_1\emotion_1\参考音频内容.txt",
    # 添加其他人物参考音频（语气）内容路径
}

ref_language = '中文'
#target_text_path = r'F:\AIAnchor\Input\GPT-SoVITS_Input\文本\测试用.txt'
target_language_path = '中文'
base_GSV_output_path = r'F:\AIAnchor\Output\GPT-SoVITS_Output'





# SadTalker
# SadTalker目录
SD_work_dir = r'F:\AIAnchor\SadTalker'
# SadTalker参数
#driven_audio = r'F:\AIAnchor\Output\GPT-SoVITS_Output\output.wav'

# 定义“人物图像”路径字典
source_images = {
    'HuTao': r"F:\AIAnchor\Input\models\HuTao\test.jpg",
    'HuaHuo': r"F:\AIAnchor\Input\models\HuaHuo\test.jpg",
    # 添加其他人物图像路径
}

base_SD_output_path = r'F:\AIAnchor\Output\SadTalker_Output'
preprocess = 'full'
enhancer = 'gfpgan'



#记录时间
timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

# 获取txt文件的名称
file_name = os.path.basename(text_file_path)

# 创建以文件名和当前时间结合的文件夹
Paragraphs_output_path = create_output_folder(timestamp, base_Paragraphs_output_path, file_name)
GSV_output_path = create_output_folder(timestamp, base_GSV_output_path, file_name)
SD_output_path = create_output_folder(timestamp, base_SD_output_path, file_name)

# Paragraph开始运行
Paragraph(Paragraphs_output_path, text_file_path, max_length=None, custom_delimiters=None, preserve_delimiters=True, handle_newlines=True)


# 获取Paragraphs处理完之后文件夹中的所有文件
processed_files = os.listdir(Paragraphs_output_path)

# 遍历文件
for processed_file in processed_files:
    # 只处理 .txt 文件
    if processed_file.endswith('.txt'):
        # 获取文件名的数字部分
        try:
            # 提取文件名中的数字部分
            processed_file_name = os.path.splitext(processed_file)[0]
            processed_file_number = int(processed_file_name)
            
            # 判断奇偶性并执行不同的操作
            if processed_file_number % 2 == 1:
                # 奇数文件，给HuTao
                print("现在是",f'{processed_file}')
                new_GSV_output_path = create_Zi_folder(GSV_output_path, processed_file_name)
                new_SD_output_path = create_Zi_folder(SD_output_path, processed_file_name)
                # GPT-SoVITS开始运行
                gpt_model_path = get_gpt_model_path('HuTao_1')
                sovits_model_path = get_sovits_model_path('HuTao_1')
                ref_audio_path = get_ref_audio_path('HuTao_1_1')
                ref_text_path = get_ref_text_path('HuTao_1_1')
                source_image = get_source_image('HuTao')
                target_text_path = os.path.join(Paragraphs_output_path, processed_file)
                run_command_GSV(GSV_work_dir, gpt_model_path, sovits_model_path, ref_audio_path, ref_text_path, ref_language, target_text_path, target_language_path, new_GSV_output_path)
                # SadTalker开始运行
                driven_audio = os.path.join(new_GSV_output_path,'output.wav')
                run_command_SD(SD_work_dir, driven_audio, source_image, new_SD_output_path, preprocess, enhancer)
            else:
                # 偶数文件，给HuaHuo
                print("现在是",f'{processed_file}')
                new_GSV_output_path = create_Zi_folder(GSV_output_path, processed_file_name)
                new_SD_output_path = create_Zi_folder(SD_output_path, processed_file_name)
                # GPT-SoVITS开始运行
                gpt_model_path = get_gpt_model_path('HuaHuo_1')
                sovits_model_path = get_sovits_model_path('HuaHuo_1')
                ref_audio_path = get_ref_audio_path('HuaHuo_1_1')
                ref_text_path = get_ref_text_path('HuaHuo_1_1')
                source_image = get_source_image('HuaHuo')
                target_text_path = os.path.join(Paragraphs_output_path, processed_file)
                run_command_GSV(GSV_work_dir, gpt_model_path, sovits_model_path, ref_audio_path, ref_text_path, ref_language, target_text_path, target_language_path, new_GSV_output_path)
                # SadTalker开始运行
                driven_audio = os.path.join(new_GSV_output_path,'output.wav')
                run_command_SD(SD_work_dir, driven_audio, source_image, new_SD_output_path, preprocess, enhancer)
                
        except ValueError:
            # 如果文件名不是数字格式，跳过该文件
            print(f'Skipping non-numeric file: {processed_file_name}')
            





'''
# GPT-SoVITS开始运行

"""
gpt_model_path = get_gpt_model_path('HuTao_1')
sovits_model_path = get_sovits_model_path('HuTao_1')
ref_audio_path = get_ref_audio_path('HuTao_1_1')
ref_text_path = get_ref_text_path('HuTao_1_1')
source_image = get_source_image('HuTao')
"""
gpt_model_path = get_gpt_model_path('HuaHuo_1')
sovits_model_path = get_sovits_model_path('HuaHuo_1')
ref_audio_path = get_ref_audio_path('HuaHuo_1_1')
ref_text_path = get_ref_text_path('HuaHuo_1_1')
source_image = get_source_image('HuaHuo')


run_command_GSV(GSV_work_dir, gpt_model_path, sovits_model_path, ref_audio_path, ref_text_path, ref_language, target_text_path, target_language_path, GSV_output_path)


# SadTalker开始运行
driven_audio = os.path.join(GSV_output_path,'output.wav')
run_command_SD(SD_work_dir, driven_audio, source_image, SD_output_path, preprocess, enhancer)
'''
