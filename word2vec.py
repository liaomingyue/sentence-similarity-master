from gensim.models import word2vec
import os
import gensim
# 此函数作用是对初始语料进行分词处理后，作为训练模型的语料
def cut_txt(old_file):
    import jieba
    global cut_file     # 分词之后保存的文件名
    cut_file = old_file + '_cut.txt'

    try:
        fi = open(old_file, 'r', encoding='utf-8')
    except BaseException as e:  # 因BaseException是所有错误的基类，用它可以获得所有错误类型
        print(Exception, ":", e)    # 追踪错误详细信息

    text = fi.read()  # 获取文本内容
    jieba.load_userdict("userDict.txt")
    jieba.add_word('蝶儿姐姐')
    new_text = jieba.cut(text, cut_all=False)  # 精确模式
    str_out = ' '.join(new_text).replace('，', '').replace('。', '').replace('？', '').replace('！', '') \
        .replace('“', '').replace('”', '').replace('：', '').replace('…', '').replace('（', '').replace('）', '') \
        .replace('—', '').replace('《', '').replace('》', '').replace('、', '').replace('‘', '') \
        .replace('’', '')     # 去掉标点符号
    fo = open(cut_file, 'w', encoding='utf-8')
    fo.write(str_out)
def model_train(train_file_name, save_model_file):  # model_file_name为训练语料的路径,save_model为保存模型名
    from gensim.models import word2vec
    import gensim
    import logging
    # 模型训练，生成词向量
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    sentences = word2vec.Text8Corpus(train_file_name)  # 加载语料
    model = gensim.models.Word2Vec(sentences, size=200)  # 训练skip-gram模型; 默认window=5
    model.save(save_model_file)
    model.wv.save_word2vec_format(save_model_file + ".bin", binary=True)   # 以二进制类型保存模型以便重用

cut_txt('倚天屠龙记.txt')  # 须注意文件必须先另存为utf-8编码格式

save_model_name = '倚天屠龙记.model'
if not os.path.exists(save_model_name):     # 判断文件是否存在
    model_train(cut_file, save_model_name)
else:
    print('此训练模型已经存在，不用再次训练')

# 加载已训练好的模型
model_1 = word2vec.Word2Vec.load(save_model_name)
# 计算两个词的相似度/相关程度
y1 = model_1.similarity("明兰", "齐衡")
print(u"明兰和齐衡的相似度为：", y1)
print("-------------------------------\n")

# 计算某个词的相关词列表
y2 = model_1.most_similar("蝶儿", topn=20)  # 10个最相关的
print(u"和蝶儿 最相关的词有：\n")
for item in y2:
    print(item[0], item[1])
print("-------------------------------\n")





































































# def savefile(savepath,content):
#     fp = open(savepath,'w',encoding='utf8',errors='ignore')
#     fp.write(content)
#     fp.close()
#
# # 读取文件的函数
# def readfile(path):
#     fp = open(path, "r", encoding='utf8', errors='ignore')
#     content = fp.read()
#     fp.close()
#     return content
#
# def readline(path):
#     file_obj =  open(path, "r", encoding='utf-8', errors='ignore')
#     out_str=[]
#     all_lines = file_obj.readlines()
#     i=0
#     for line in all_lines:
#         if(i==0):
#             line = line.strip('\n').strip('\u3000').strip('\ufeff')
#             i=i+1
#         else:
#             line = line.strip('\n').strip('\u3000')
#         if(line==''):
#             continue
#         else:
#             out_str.append(line)
#     return out_str
# def stopwordslist(filepath):
#     stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
#     return stopwords
#
# def movestopwords(sentence,stopwords):
#     # stopwords = stopwordslist('语料/hlt_stop_words.txt')  # 这里加载停用词的路径
#     outstr = ''
#     for word in sentence:
#         if word not in stopwords:
#             if word != '\t'and'\n':
#                 outstr += word
#                 # outstr += " "
#     return outstr
#
# stopwords=stopwordslist('input/novel/stopword.txt')
# # sentence=readfile('input/novel/xiuxian.txt')
# sentence=readline('input/novel/xiuxian.txt')
# sentences=[]
# for line in sentence:
#     seg_list = jieba.cut(line, cut_all=False)
#     sentence=" ".join(seg_list)
#     sentence=sentence.split(' ')
#     sentences.append(sentence)
# print(sentences)
# #
# path = get_tmpfile("word2vec.model") #创建临时文
# model = Word2Vec(sentences=sentences, size=300, min_count=1)
# model.wv.save_word2vec_format('model/token_vec_300.bin', binary=False)

# print(movestopwords(sentence,stopwords))