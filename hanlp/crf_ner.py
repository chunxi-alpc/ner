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

CRFSegmenter = JClass('com.hankcs.hanlp.model.crf.CRFSegmenter')
CRFLexicalAnalyzer = JClass('com.hankcs.hanlp.model.crf.CRFLexicalAnalyzer')
CWSEvaluator = SafeJClass('com.hankcs.hanlp.seg.common.CWSEvaluator')
AbstractLexicalAnalyzer = JClass(
    'com.hankcs.hanlp.tokenizer.lexical.AbstractLexicalAnalyzer')
Utility = JClass('com.hankcs.hanlp.model.perceptron.utility.Utility')
PerceptronSegmenter = JClass(
    'com.hankcs.hanlp.model.perceptron.PerceptronSegmenter')
PerceptronPOSTagger = JClass(
    'com.hankcs.hanlp.model.perceptron.PerceptronPOSTagger')


def train(corpus, model):
    # 零参数的构造函数代表加载配置文件默认的模型，必须用null None 与之区分。
    segmenter = CRFSegmenter(None)             # 创建 CRF 分词器
    segmenter.train(corpus, model)
    return CRFLexicalAnalyzer(segmenter)


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
    file1998 = open('1998.txt', 'r', encoding='utf-8', errors='ignore')
    s = ''
    s = file1998.readline()
    ori = analyzer.analyze(s)
    words = ' '
    for term in ori:
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
