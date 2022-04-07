import jieba
import math
import time
import os
import re


# 本程序实现参考了CSDN博客：深度学习与自然语言处理实验——中文信息熵的计算。对语料库生成及预处理进行了调整改进，并增加了按字分词情况下信息熵计算
class TraversalFun:
    def __init__(self, rootDir):
        self.rootDir = rootDir

    def getCorpus(self):
        corpus = []
        r1 = u'[a-zA-Z0-9’!"#$%&\'()*+,-./:：;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~「」]'  # 用户也可以在此进行自定义过滤字符
        file_inf = open(r'E:\now\class\NLP\homework1\dataset\inf.txt', "r", encoding='ansi')
        context = file_inf.read()
        listdir = context.split(',')  # 获取书籍名
        count = 0
        for file_txt in listdir:
            file_txt = file_txt + '.txt'
            path = os.path.join(self.rootDir, file_txt)
            with open(os.path.abspath(path), "r", encoding='ansi') as file:
                filecontext = file.read()
                filecontext = filecontext.replace("本书来自www.cr173.com免费txt小说下载站\n更多更新免费电子书请关注www.cr173.com", '')
                filecontext = filecontext.replace("\n", '')
                filecontext = ''.join(filecontext.split())  # 去除所有空格
                filecontext = re.sub(r1, '', filecontext)  # 正则表达式去除标点
                count += len(filecontext)
                corpus.append(filecontext)
        return corpus, count


def get_bigram_tf(tf_dic, words):
    for i in range(len(words) - 1):
        tf_dic[(words[i], words[i + 1])] = tf_dic.get((words[i], words[i + 1]), 0) + 1


def get_trigram_tf(tf_dic, words):
    for i in range(len(words) - 2):
        tf_dic[((words[i], words[i + 1]), words[i + 2])] = tf_dic.get(((words[i], words[i + 1]), words[i + 2]), 0) + 1


def cal_trigram(corpus, count, unit='words'):
    before = time.time()
    split_words = []
    words_len = 0
    line_count = 0
    words_tf = {}
    trigram_tf = {}

    for line in corpus:  # 根据分词单位进行分词
        if unit == 'words':
            for x in jieba.cut(line):
                split_words.append(x)
                words_len += 1
        else:
            for x in line:
                split_words.append(x)
                words_len += 1

        get_bigram_tf(words_tf, split_words)
        get_trigram_tf(trigram_tf, split_words)

        split_words = []
        line_count += 1

    print("语料库字数:", count)
    print("分词个数:", words_len)
    print("平均词长:", round(count / words_len, 5))

    trigram_len = sum([dic[1] for dic in trigram_tf.items()])
    print("三元模型长度:", trigram_len)

    entropy = []
    for tri_word in trigram_tf.items():
        jp_xy = tri_word[1] / trigram_len  # 计算联合概率p(x,y)
        cp_xy = tri_word[1] / words_tf[tri_word[0][0]]  # 计算条件概率p(x|y)
        entropy.append(-jp_xy * math.log(cp_xy, 2))  # 计算三元模型的信息熵
    print("基于词的三元模型的中文信息熵为:", round(sum(entropy), 5), "比特/词")

    after = time.time()
    print("运行时间:", round(after - before, 5), "s")


if __name__ == '__main__':
    unit = 'words'  # 分词单位
    tra = TraversalFun("./dataset")  # ./代表当前所在目录下的某个文件夹或文件
    corpus, count = tra.getCorpus()  # 生成语料库
    cal_trigram(corpus, count, unit)  # 计算信息熵
