import jieba

datafile = './dataset'
text = ["笑傲江湖", "神雕侠侣", "射雕英雄传", "天龙八部", "倚天屠龙记"]


# 语料预处理，进行断句，去除一些广告和无意义内容
def content_deal(content): 
    ad = ['本书来自www.cr173.com免费txt小说下载站\n更多更新免费电子书请关注www.cr173.com', '----〖新语丝电子文库(www.xys.org)〗', '新语丝电子文库',
          '\u3000', '\n', '。', '？', '！', '，', '；', '：', '、', '《', '》', '“', '”', '‘', '’', '［', '］', '....', '......',
          '『', '』', '（', '）', '…', '「', '」', '\ue41b', '＜', '＞', '+', '\x1a', '\ue42b']
    for a in ad:
        content = content.replace(a, '')
    return content


# 读取文件夹文件
def read_data(path):
    data_txt = []
    files = text  # 返回指定的文件夹包含的文件列表
    for file in files:
        position = path + '\\' + file + '.txt' # 构造绝对路径，"\\"，其中一个'\'为转义符

        with open(position, 'r', encoding='ANSI') as f:
            data = f.read()
            data = content_deal(data)
            data = jieba.lcut(data)
            data_txt.append(data)
        f.close()
    return data_txt, files


def get_fragment(txt, file):
    num = len(txt)
    interval = int(num/40)
    for i in range(40):
        fragment = txt[interval*i:interval*i+500]
        position = '.\\data' + '\\' + file + str(i) + '.txt' 
        with open(position, 'w', encoding='ANSI') as f:
            for item in fragment:
                f.write(item)


if __name__ == '__main__':
    data_txt, files = read_data(datafile)
    for txt, file in zip(data_txt, files):
        get_fragment(txt, file)
    str = "generate all!"
    print(str)
