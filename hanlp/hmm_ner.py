from pyhanlp import *
import os
import re
# 指定 PKU 语料库
PKU98 = '../../data/pku98'
PKU199801 = os.path.join(PKU98, '199801.txt')
PKU199801_TRAIN = os.path.join(PKU98, '199801-train.txt')
PKU199801_TEST = os.path.join(PKU98, '199801-test.txt')

# ===============================================
# 以下开始 HMM 命名实体识别

HMMNERecognizer = JClass('com.hankcs.hanlp.model.hmm.HMMNERecognizer')
Utility = JClass('com.hankcs.hanlp.model.perceptron.utility.Utility')
PerceptronSegmenter = JClass(
    'com.hankcs.hanlp.model.perceptron.PerceptronSegmenter')
PerceptronPOSTagger = JClass(
    'com.hankcs.hanlp.model.perceptron.PerceptronPOSTagger')
AbstractLexicalAnalyzer = JClass(
    'com.hankcs.hanlp.tokenizer.lexical.AbstractLexicalAnalyzer')


def train(corpus):
    recognizer = HMMNERecognizer()
    recognizer.train(corpus)
    return recognizer


def check(pat, pat2, ww, ff):
    ans = []
    anslist = []
    ww = pat.findall(ww)
    for line in ff:
        ans.extend(pat.findall(line))
        if pat2 != None:
            ans.extend(pat2.findall(line))
    for each in ans:
        anslist.append(re.sub('[a-z\s/\[\]]+', '', each))

    myset = set(ww)
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

    scores = Utility.evaluateNER(recognizer, PKU199801_TEST)
    Utility.printNERScore(scores)


if __name__ == '__main__':
    recognizer = train(PKU199801_TRAIN)
    test(recognizer)
