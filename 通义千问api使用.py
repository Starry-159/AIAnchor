from http import HTTPStatus
import dashscope


MY_DASHSCOPE_API_KEY = 'sk-7be92278538543e1bfc3a71ab47c9833'

dashscope.api_key= MY_DASHSCOPE_API_KEY
"""
def call_with_messages():
    messages = [{'role': 'system', 'content': '你可以将输入的一大段文本分成几个自然段。段与段之间用\n\n隔开'},
                {'role': 'user', 'content': '三季度中国宏观经济数据即将公布，最新发布的多个先行指标呈现回升向好态势，尤其进入九月份，部分指标回升速度加快，折射出中国经济持续稳定增长的基本态势。产业兴，建设忙。9月份，与工程项目相关的中标数量增速创今年以来新高，企业扩产热度回升明显。'}]

    response = dashscope.Generation.call(
        model="qwen-turbo",
        messages=messages,
        result_format='message',  # 将返回结果格式设置为 message
    )
    if response.status_code == HTTPStatus.OK:
        print(response)
    else:
        print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))


if __name__ == '__main__':
    call_with_messages()
"""

import os
from dashscope import Generation

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
    


def call_with_messages(text):
    messages = [
        {'role': 'system', 'content': '你可以将输入的一大段文本分成几个自然段。'},
        {'role': 'user', 'content': text}
        ]
    response = Generation.call(
        # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key = "sk-xxx",
        #api_key=os.getenv("sk-7be92278538543e1bfc3a71ab47c9833"), 
        model="qwen-turbo",
        messages=messages,
        result_format="message"
    )

    if response.status_code == 200:
        print(response.output.choices[0].message.content)
        return response.output.choices[0].message.content
    else:
        print(f"HTTP返回码：{response.status_code}")
        print(f"错误码：{response.code}")
        print(f"错误信息：{response.message}")
        print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")

def save_files(text, folder_path):
    """
    功能：
        通用型，将text内容保存为txt文件，存储在folder_path的文件夹中
    参数:
        text(str): 需要保存的text内容。
        folder_path (str): 文件夹目录路径。
    """
    # 确保文件夹存在
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, 'test001.txt')
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(text)


if __name__ == '__main__':
    # 确定要处理的文稿
    text_file_path = r"F:\AIAnchor\Input\Paragraphs_Input\test2.txt"
    # 从文本路径所对应的文本读出，存到text里
    text = read_text_from_file(text_file_path)
    # 将text传入大模型，传出分好段的文本（每段以\n\n分隔）并存在text_para(str)里
    text_para = call_with_messages(text)
    # 将text_para存到文件夹目录为folder_path里的.txt文件中
    folder_path = r'F:\AIAnchor'
    save_files(text_para, folder_path)
    # 使用 '\n\n' 分割text_para，存储到paragraphs中
    paragraphs = text_para.split('\n\n')
    # 打印每个自然段
    for i, paragraph in enumerate(paragraphs):
        print(f"段落 {i + 1}:")
        print(paragraph)
        print()  # 打印空行以分隔段落
    
