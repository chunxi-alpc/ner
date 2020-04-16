from util import *
from HMM import *
import re
import os


wordDict = acquireDict(
    ['data\\test.char.bmes', 'data\\train.char.bmes'])

# 定义标签字典
tagDict = {'B-TIME': 0, 'M-TIME': 1, 'E-TIME': 2, 'O': 3, 'B-LOC': 4, 'M-LOC': 5, 'E-LOC': 6, 'B-ORG': 7,
           'M-ORG': 8, 'E-ORG': 9, 'B-NAME': 10, 'M-NAME': 11, 'E-NAME': 12, 'S-TIME': 13, 'S-LOC': 14, 'S-ORG': 15,  'S-NAME': 16, }

# 训练集数据
trainWordLists, trainTagLists = prepareData('data\\train.char.bmes')

# 测试集数据
testWordLists, testTagLists = prepareData('data\\test.char.bmes')

# HMM方法
print('-----------------------------------HMM-----------------------------')
hmm = HMM(len(wordDict), len(tagDict))
hmm.trainSup(str2int(trainWordLists, wordDict),
             str2int(trainTagLists, tagDict))
hmm.test(str2int(testWordLists, wordDict), str2int(
    testTagLists, tagDict), wordDict, tagDict)
print('\n')
