
from pyhanlp import *
import os
import re
# 指定 PKU 语料库
PKU98 = '../../data/pku98'
PKU199801 = os.path.join(PKU98, '199801.txt')
PKU199801_TRAIN = os.path.join(PKU98, '199801-train.txt')
PKU199801_TEST = os.path.join(PKU98, '199801-test.txt')
POS_MODEL = os.path.join(PKU98, 'pos.bin')
NER_MODEL = os.path.join(PKU98, 'ner.bin')

# ===============================================
# 以下开始 感知机 命名实体识别

NERTrainer = JClass('com.hankcs.hanlp.model.perceptron.NERTrainer')
PerceptronNERecognizer = JClass(
    'com.hankcs.hanlp.model.perceptron.PerceptronNERecognizer')
PerceptronSegmenter = JClass(
    'com.hankcs.hanlp.model.perceptron.PerceptronSegmenter')
PerceptronPOSTagger = JClass(
    'com.hankcs.hanlp.model.perceptron.PerceptronPOSTagger')
Sentence = JClass('com.hankcs.hanlp.corpus.document.sentence.Sentence')
Utility = JClass('com.hankcs.hanlp.model.perceptron.utility.Utility')
AbstractLexicalAnalyzer = JClass(
    'com.hankcs.hanlp.tokenizer.lexical.AbstractLexicalAnalyzer')


def train(corpus, model):
    trainer = NERTrainer()
    return PerceptronNERecognizer(trainer.train(corpus, model).getModel())


def check(pat, pat2, words, ff):
    ans = []
    anslist = []
    words = pat.findall(words)
    for line in ff:
        ans.extend(pat.findall(line))
        if pat2 != None:
            ans.extend(pat2.findall(line))
    for each in ans:
        anslist.append(re.sub('[a-z\s/\[\]]+', '', each))

    myset = set(words)
    ansset = set(anslist)
    TP_set = myset & ansset
    FN_set = ansset - myset
    FP_set = myset - ansset
    TP = len(TP_set)
    FN = len(FN_set)
    FP = len(FP_set)
    precision = TP/(TP+FP)
    recall = TP/(TP+FN)
    print(FN_set)
    print("recall: ", recall)
    print("precision: ", precision)
    print("F1: ", 2*precision*recall/(precision+recall))


def test(recognizer):
    # 包装了感知机分词器和词性标注器的词法分析器
    # scores = Utility.evaluateNER(recognizer, PKU199801_TEST)
    # Utility.printNERScore(scores)
    analyzer = AbstractLexicalAnalyzer(
        PerceptronSegmenter(), PerceptronPOSTagger(), recognizer)
    testfile = open(PKU199801_TEST, 'r', encoding='utf-8', errors='ignore')
    original = open('1998.txt', 'r', encoding='utf-8', errors='ignore')
    original = original.readline()
    original = analyzer.analyze(original)
    words = ' '
    for term in original:
        words += str(term)+' '

    org_mulpat = re.compile('\[([^]]*?)]/nt[a-z]*')
    org_pat = re.compile('[\[\s](\S*?)/nt[a-z]*')
    name_pat = re.compile('[\[\s](\S*?)/nr[a-z]*')
    time_mulpat = re.compile('\[([^]]*?)]/t[a-z]*')
    time_pat = re.compile('[\[\s](\S*?)/t[a-z]*')
    loc_mulpat = re.compile('\[([^]]*?)]/ns[a-z]*')
    loc_pat = re.compile('[\[\s](\S*?)/ns[a-z]*')
    ff = testfile.readlines()
    check(name_pat, None, words, ff)
    check(loc_pat, loc_mulpat, words, ff)
    check(org_pat, org_mulpat, words, ff)


if __name__ == '__main__':
    recognizer = train(PKU199801_TRAIN, NER_MODEL)
    test(recognizer)
"""
    # 支持在线学习
    # 创建了感知机词法分析器
    analyzer = PerceptronLexicalAnalyzer(
        PerceptronSegmenter(), PerceptronPOSTagger(), recognizer)  # ①
    # 根据标注样本的字符串形式创建等价的 Sentence对象
    sentence = Sentence.create(
        "与/c 特朗普/nr 通/v 电话/n 讨论/v [太空/s 探索/vn 技术/n 公司/n]/nt")  # ②
    # 测试词法分析器对样本的分析结果是否与标注一致，若不一致重复在线学习，直到两者一致。
    while not analyzer.analyze(sentence.text()).equals(sentence):  # ③
        analyzer.learn(sentence)
"""
