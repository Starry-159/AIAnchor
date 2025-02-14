import re
import os
import datetime


def read_text_from_file(file_path):
    """
    从指定的文本文件读取内容。
    
    参数:
    file_path (str): 文本文件的路径。
    
    返回:
    str: 文件中的文本内容。
    """
    with open(file_path, 'r', encoding='utf-8') as file:
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


def create_output_folder(base_folder, file_name):
    """创建以文件名和当前时间结合的文件夹。"""
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    folder_name = f"{os.path.splitext(file_name)[0]}_{timestamp}"
    folder_path = os.path.join(base_folder, folder_name)
    os.makedirs(folder_path, exist_ok=True)
    return folder_path


# 指定文本文件路径
text_file_path = r'F:\AIAnchor\Input\Paragraphs_Input\test.txt'
base_output_folder = 'F:\\AIAnchor\\Output\\Paragraphs_Output'

# 从文本文件读取内容
text = read_text_from_file(text_file_path)

# 自动分段（指定自定义分隔符并保留分隔符）
paragraphs_custom_delimiter = auto_split_text(text, max_length=10, preserve_delimiters=True)

print("\n使用自定义分隔符且保留分隔符的分段结果：")
for i, para in enumerate(paragraphs_custom_delimiter):
    print(f"段落 {i+1}: {para}")


# 创建以文件名和当前时间结合的文件夹
file_name = os.path.basename(text_file_path)
output_folder = create_output_folder(base_output_folder, file_name)


# 保存段落到txt文件
save_paragraphs_to_files(paragraphs_custom_delimiter, output_folder)

print(f"段落已保存到文件夹：{output_folder}")