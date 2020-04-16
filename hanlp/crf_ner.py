from pyhanlp import *
import os
from pyhanlp.static import download, remove_file, HANLP_DATA_PATH

# 指定 PKU 语料库
PKU98 = '../data/pku98'
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


def test(recognizer):
    scores = Utility.evaluateNER(recognizer, PKU199801_TEST)
    Utility.printNERScore(scores)


if __name__ == '__main__':
    recognizer = train(PKU199801_TRAIN, NER_MODEL)
    test(recognizer)
