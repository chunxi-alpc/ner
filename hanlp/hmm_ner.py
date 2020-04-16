from pyhanlp import *
import os

# 指定 PKU 语料库
PKU98 = '../../data/pku98'
PKU199801 = os.path.join(PKU98, '199801.txt')
PKU199801_TRAIN = os.path.join(PKU98, '199801-train.txt')
PKU199801_TEST = os.path.join(PKU98, '199801-test.txt')
POS_MODEL = os.path.join(PKU98, 'pos.bin')
NER_MODEL = os.path.join(PKU98, 'ner.bin')

# ===============================================
# 以下开始 HMM 命名实体识别

HMMNERecognizer = JClass('com.hankcs.hanlp.model.hmm.HMMNERecognizer')
Utility = JClass('com.hankcs.hanlp.model.perceptron.utility.Utility')


def train(corpus):
    recognizer = HMMNERecognizer()
    recognizer.train(corpus)
    return recognizer


def test(recognizer):
    # 包装了感知机分词器和词性标注器的
    # 词法分析器
    scores = Utility.evaluateNER(recognizer, PKU199801_TEST)
    Utility.printNERScore(scores)


if __name__ == '__main__':
    recognizer = train(PKU199801_TRAIN)
    test(recognizer)
