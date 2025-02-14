# -*- coding: utf-8 -*-


import subprocess
import sys

"""
def install_package(package_name):
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package_name])

# 安装jieba和scikit-learn
# jieba: 中文分词库
install_package('jieba')
# scikit-learn: 机器学习库，用于主题建模
install_package('scikit-learn')
"""


# jieba: 用于中文文本分词
import jieba
# CountVectorizer: 用于将文本转换为词频矩阵
from sklearn.feature_extraction.text import CountVectorizer
# LatentDirichletAllocation: 用于主题建模
from sklearn.decomposition import LatentDirichletAllocation

# 函数：分词
def segment_text(text):
    """
    jieba.cut(text): 将文本分词
    ' '.join(): 将分词结果以空格分隔，形成适合CountVectorizer的格式
    """
    return ' '.join(jieba.cut(text))

# 函数：使用LDA进行主题建模
def perform_lda(sentences, n_topics=3):
    # CountVectorizer: 将文本转换为词频矩阵，stop_words参数用于移除常见的无用词
    vectorizer = CountVectorizer(stop_words=['的', '是', '在', '了', '和'])
    # fit_transform(sentences): 生成词频矩阵
    X = vectorizer.fit_transform(sentences)
    
    # LatentDirichletAllocation: 创建LDA模型，n_components指定主题数量
    lda = LatentDirichletAllocation(n_components=n_topics, random_state=42)
    # lda.fit(X): 拟合模型
    lda.fit(X)
    
    # feature_names: 获取词汇表中的词
    feature_names = vectorizer.get_feature_names_out()
    topics = []
    # lda.components_: 获取每个主题的词分布
    for topic_idx, topic in enumerate(lda.components_):
        # topic.argsort()[:-10 - 1:-1]: 获取每个主题中最重要的前10个词
        topic_keywords = [feature_names[i] for i in topic.argsort()[:-10 - 1:-1]]
        # topics: 存储每个主题的关键词
        topics.append(f"主题 {topic_idx}: {' '.join(topic_keywords)}")
    
    return topics, X

# 函数：根据主题将文本分段
def segment_by_topic(sentences, X, n_topics=3):
    lda = LatentDirichletAllocation(n_components=n_topics, random_state=42)
    lda.fit(X)
    
    # lda.transform(X): 计算每个文档对各主题的分布
    # argmax(axis=1): 获取每个文档的主要主题
    topic_assignments = lda.transform(X).argmax(axis=1)
    
    # segments: 存储按主题分段的文本
    segments = {i: [] for i in range(n_topics)}
    for idx, sentence in enumerate(sentences):
        topic = topic_assignments[idx]
        segments[topic].append(sentence)
    
    return segments


# 示例文本
text = """
文化安全是指主权国家的主流文化价值体系与国家政治、经济发展及相应的意识形态、社会生活制度、语言符号、信息知识、宗教信仰等发展协调一致、良性互动，在保持高度民族文化认同的同时，具有延绵不断的文化传承和创新能力[3]。或者说，文化安全就是指文化处于能够延续、不被侵略的状态。
公共生活活动范围广泛。随着交通的迅速发展，互联网技术的不断进步，公共生活的范围不断扩大。我们可以在物理空间上行走，我们既可以乘坐高铁、飞机等快速交通工具，从一座城市到另一座城市，扩大了我们的公共生活，也可以乘坐轮船等慢速交通工具，在水面上缓慢行驶，拉长了我们的公共生活，还可以通过步行、骑车的方式到具体的地点，精细了我们的公共生活；也可以在网络空间里漫游，现在各种各样的通信工具，大大丰富了人们的通信方式，拓宽了我们的公共生活，我们可以与别人更方便地交流，方便了我们的公共生活。回顾十四个五年计划的目的，工业建设、社会主义改造、加强国防、经济建设、外交建设、调整、改革开放、经济体制改革、社会主义市场经济体制、小康生活、缩小地区间的发展差异、提高自主创新能力、基础设施、科技创新等等。究其根本，是围绕人民生活展开的。也就是说，十四个五年计划的终极目的都是为了提高人民生活水平，十四五规划亦是如此。

"""





# 分词
sentences = [segment_text(text)]

# 进行LDA主题建模
topics, X = perform_lda(sentences)

print("识别的主题:")
for topic in topics:
    print(topic)

# 根据主题进行分段
segments = segment_by_topic(sentences, X, 3)

print("\n按主题分段的文本:")
for topic_id, segment in segments.items():
    print(f"\n--- 主题 {topic_id} ---")
    for sentence in segment:
        print(sentence)
