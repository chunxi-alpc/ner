
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


def train(corpus, model):
    trainer = NERTrainer()
    return PerceptronNERecognizer(trainer.train(corpus, model).getModel())


def test(recognizer):
    # 包装了感知机分词器和词性标注器的词法分析器
    scores = Utility.evaluateNER(recognizer, PKU199801_TEST)
    Utility.printNERScore(scores)


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
