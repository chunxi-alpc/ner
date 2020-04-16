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
# 以下开始 CRF 命名实体识别

CRFNERecognizer = JClass('com.hankcs.hanlp.model.crf.CRFNERecognizer')
AbstractLexicalAnalyzer = JClass(
    'com.hankcs.hanlp.tokenizer.lexical.AbstractLexicalAnalyzer')
Utility = JClass('com.hankcs.hanlp.model.perceptron.utility.Utility')


def train(corpus, model):
    # 零参数的构造函数代表加载配置文件默认的模型，必须用null None 与之区分。
    recognizer = CRFNERecognizer(None)  # 空白
    recognizer.train(corpus, model)
    return recognizer


def check(pat, pat2, words, testfile):
    ans = []
    anslist = []
    words = pat.findall(words)
    ff = testfile.readlines()
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
    check(name_pat, None, words, testfile)


if __name__ == '__main__':
    recognizer = train(PKU199801_TRAIN, NER_MODEL)
    test(recognizer)
