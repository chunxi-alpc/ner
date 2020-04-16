# -*- coding: utf-8 -*-
#!/usr/bin/python
# location

import re
import os
import jieba
import jieba.posseg as pseg
from collections import Counter

suffix = re.compile(
    '\S*城|\S*山|\S*厅|\S*区|\S*高速|\S*路|\S*超市|\S*道|\S*处|\S*遗址|\S*公园|\S*庙|\S*市|\S*入口|\S*县|\S*[东西南北]面'
    '|\S*村|\S*岛|\S*广场|\S*店|\S*郡|\S*单元|\S*庄|\S*河|\S*镇|\S*中心|\S*门口|\S*海|\S*场|\S*地|\S*路|\S*坳|\S*省|\S*市'
    '|\S*馆|\S*店|\S*沙漠|\S*隧道|\S*海域|\S*机场|\S*桥|\S*庙|\S*站|\S*商圈|\S*府|\S*[小中大]学|\S*高速|\S*部|\S*道|\S*商城')
province = '京津沪渝蒙宁新藏桂台港澳黑吉辽冀晋鲁苏浙皖赣湘鄂豫粤闽琼川滇黔陕甘青'
for i in province:
    jieba.add_word(i, tag='ns')
jieba.add_word('法', tag='ns')
jieba.add_word('英', tag='ns')
jieba.add_word('没', tag='ns')
jieba.add_word('台', tag='ns')
jieba.add_word('晋', tag='ns')


pattern = re.compile('location:(\S*?)}')
mylist = []
loclist = []
plist = []
allseq = ""
words = []
with open('../data/BosonNLP_NER_6C.txt', 'r', encoding='UTF-8') as f:
    file = f.readlines()
    for line in file:
        T = pattern.findall(line)
        if T != []:
            for each in T:
                loclist.append(each)
                word = pseg.cut(each)
                seq = ""
                for w in word:
                    seq = seq+w.flag+','
                plist.append(seq)
        # 统计地名序列
        result = Counter(plist)

# 统计所有词的词性
        word = pseg.cut(line)
        for w in word:
            words.append((w.word, w.flag))
            allseq += w.flag+','

# 统计序列个数
pre = []
Pn = 0.5
for w, p in result.items():
    b = len(re.findall(w, allseq))
    result[w] = p/b
    if p/b >= Pn:
        pre.append(w[0:w.find(',')-1])


# 根据规则和统计匹配地名
num = len(words)
words.append(('.', 'x'))
i = 0
seq = ''
word = ''
while i < num:
    if words[i][1] in ['p', 'u', 'b', 'v', 'w', 'x']:
        if result[seq] >= Pn:
            mylist.append(word)
        else:
            seq = ''
            word = ''
    else:
        if seq == '' and words[i][1] in pre:
            seq = words[i][1]+','
            word = words[i][0]
        else:
            seq += words[i][1]+','
            word += words[i][0]
    i += 1

i = 0
while i < num:
    if words[i][1] == 'ns':
        if words[i+1][1] in ['p', 'u', 'b', 'v', 'w', 'x']:
            mylist.append(words[i][0])
        elif words[i+1][1] == 'ns' or suffix.search(words[i+1][0]):
            words[i+1] = (words[i][0]+words[i+1][0], 'ns')
    i += 1


loclist = list(set(loclist))
mylist = list(filter(None, mylist))
myset = set(mylist)
ansset = set(loclist)
TP_set = myset & ansset
FN_set = ansset - myset
FP_set = myset-ansset
'''
print(FN_set)
for w in FN_set:
    p = pseg.cut(w)
    print(list(p))

'''
print(FN_set)
TP = len(TP_set)
FN = len(FN_set)
FP = len(FP_set)
precision = TP/(TP+FP)
recall = TP/(TP+FN)
print("recall: ", recall)
print("precision: ", precision)
print("F1: ", 2*precision*recall/(precision+recall))
