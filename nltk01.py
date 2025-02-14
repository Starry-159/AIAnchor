import os
import nltk
from nltk.tokenize import sent_tokenize

#nltk.download('punkt')

import nltk
nltk.download('punkt', download_dir='f:/AIAnchor/GPT-SoVITS-beta0706/runtime/nltk_data')


'''
def divide_text_into_paragraphs(text):
    # 按段落分割
    paragraphs = text.split('\n')
    return paragraphs

def assign_roles_to_paragraphs(paragraphs):
    roles = ["角色1", "角色2"]
    dialogue = []
    for i, paragraph in enumerate(paragraphs):
        sentences = sent_tokenize(paragraph)
        role = roles[i % 2]
        dialogue.append((role, sentences))
    return dialogue

def save_paragraphs_to_files(dialogue, output_folder):
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for i, (role, sentences) in enumerate(dialogue):
        # 创建文件名
        file_name = f"{role}_{i + 1}.txt"
        file_path = os.path.join(output_folder, file_name)
        
        # 将句子写入文件
        with open(file_path, 'w', encoding='utf-8') as file:
            for sentence in sentences:
                file.write(sentence + '\n')

# 示例文本
text = """这是第一段。它有多个句子。例如，这是一句。还有另一句。
这是第二段。它也有多个句子。比如这句。还有这句。"""

# 设置输出文件夹路径
output_folder = r'F:\AIAnchor\Output\Paragraphs_Output'

# 处理文本
paragraphs = divide_text_into_paragraphs(text)
dialogue = assign_roles_to_paragraphs(paragraphs)

# 保存文件
save_paragraphs_to_files(dialogue, output_folder)

'''