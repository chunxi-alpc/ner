# -*- coding: utf-8 -*-
#!/usr/bin/python
# organization

import re
import os

suffix = re.compile(
    '\w+分局|\w+[案估小防挥]组|\w+院|\w+[协委商字监]会|\w+[院校]|\w+队|\w+[女男]篮|\w+联盟|\w+警方|\w+中心|\w+[大中小]学|\w+银?行|\w+部门?|\w+所|\w+厅|\w+省'
    '|\w+局|\w+社|\w+国|\w+军|\w+党|\w+委|\w+府|\w+区|\w+村|\w+署|\w*[商银足妇苏曼]联|\w+站|\w+办|\w+公司|\w+团|\w+社|\w+办公室|\w+派|\w+司|\w+组织|\w+街道')
proper = re.compile('中国?|美国?|中[共央]\w+|中统|伊朗|日本?|军方|119|CBA|法|福建|党中央|CFCA|CBI')
pattern = re.compile('org_name:(\S*?)}')
mylist = []
orglist = []
with open('../data/BosonNLP_NER_6C.txt', 'r', encoding='UTF-8') as f:
    file = f.readlines()
    for line in file:
        w = pattern.findall(line)
        orglist.extend(w)
        w = suffix.findall(line)
        mylist.extend(w)
        w = proper.findall(line)
        mylist.extend(w)
myset = set(mylist)
ansset = set(orglist)
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
