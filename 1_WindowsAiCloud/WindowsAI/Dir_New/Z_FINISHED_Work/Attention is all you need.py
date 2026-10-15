### 单词长度、下一词随机预测也是一种信息，根据历史已有信息生成出现频率高的单词，可以提高效率
import random
import string

# 这个是最基本的随机字符生成函数
# 我需要让他有语义、句意，并保持一定程度的随机性

# # 生成1000个随机字符的文本
# def generate_random_text(length):
#     return ''.join(random.choice(string.ascii_lowercase + ' ') for _ in range(length))
#
#
# while True:
#     random_text = generate_random_text(1000)
#     print(random_text)

# 这个是带有单词的随机字符生成函数
import random
import nltk

# 下载NLTK的资源（如果尚未下载）
nltk.download('words')

# 获取所有英语单词的列表
word_list = nltk.corpus.words.words()


def generate_random_text(length):
    text = []
    for _ in range(length):
        # 按照一定概率选择生成单词或空格
        if random.random() < 0.5:  # 调整这个概率以控制单词生成的频率
            word = random.choice(word_list)
            text.append(word)
        else:
            text.append(' ')
    return ''.join(text)


# 生成包含单词的文本
random_text = generate_random_text(1000)
print(random_text)
