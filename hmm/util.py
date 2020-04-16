from collections import OrderedDict
import re
import os
'''
准备数据
:filePath 文件路径
:wordlists 句子列表
:taglists 句子列表对应的标签列表
'''


def prepareData(filePath):
    f = open(filePath, 'r', encoding='utf-8', errors='ignore')
    wordlists, taglists = [], []
    wordlist, taglist = [], []
    for line in f.readlines():
        if line == '\n':
            wordlists.append(wordlist)
            taglists.append(taglist)
            wordlist, taglist = [], []
        else:
            word, tag = line.strip('\n').split(' ')
            wordlist.append(word)
            taglist.append(tag)
    if len(wordlist) != 0 or len(taglist) != 0:
        wordlists.append(wordlist)
        taglists.append(taglist)
    f.close()
    return wordlists, taglists


'''
数字标识转化为字符串
: origin是原来的数字标识(字典标识)
: dictionary 是对应的字典
'''


def int2str(origin, dictionary):
    result = []
    keys = list(dictionary.keys())
    if isinstance(origin[0], list):
        for i in range(len(origin)):
            result.append([])
            for j in range(len(origin[i])):
                result[i].append(keys[int(origin[i][j])])
    else:
        for i in range(len(origin)):
            result.append(keys[int(origin[i])])
    return result


'''
字符串转化为字典标识(数字)
: origin是原来的字符串
: dictionary 是对应的字典
'''


def str2int(origin, dictionary):
    result = []
    if isinstance(origin[0], list):
        for i in range(len(origin)):
            result.append([])
            for j in range(len(origin[i])):
                result[i].append(dictionary[origin[i][j]])
    else:
        for i in range(len(origin)):
            result.append(dictionary[origin[i]])
    return result


'''
获取词表、标签表
'''


def acquireDict(fileNameList):
    wordDict = OrderedDict()
    for fileName in fileNameList:
        f = open(fileName, 'r', encoding='utf-8', errors='ignore')
        for line in f.readlines():
            if line == '\n':
                continue

            word, tag = line.strip('\n').split(' ')
            if word not in wordDict:
                wordDict[word] = len(wordDict)
        f.close()
    return wordDict

# 获得词典BMEOS


def pre_Boson():
    trainfile = open('data\\train.char.bmes', 'w',
                     encoding='utf-8', errors='ignore')
    testfile = open('data\\test.char.bmes', 'w',
                    encoding='utf-8', errors='ignore')
    org_pat = re.compile('org_name:(\S*?)}')
    loc_pat = re.compile('location:(\S*?)}')
    time_pat = re.compile('time:(\S*?)}')
    name_pat = re.compile('person_name:(\S*?)}')
    with open('../data/BosonNLP_NER_6C.txt', 'r', encoding='UTF-8') as ff:
        file = ff.readlines()
        totline = len(file)
        limit = int(totline*0.9)
        for k in range(limit):
            line = re.sub(' +', '', file[k])
            line = line.replace('\n', '').replace('\t', '')
            if line == '':
                continue
            orglist_B = []
            loclist_B = []
            timelist_B = []
            namelist_B = []
            E = {}
            orglist_S = []
            loclist_S = []
            timelist_S = []
            namelist_S = []
            w = org_pat.finditer(line)
            for it in w:
                s = it.span()
                s = (s[0]+9, s[1]-1)
                if s[1]-s[0] == 1:
                    orglist_S.append(s[0])
                else:
                    orglist_B.append(s[0])
                    E[s[0]] = s[1]
            w = loc_pat.finditer(line)
            for it in w:
                s = it.span()
                s = (s[0]+9, s[1]-1)
                if s[1]-s[0] == 1:
                    loclist_S.append(s[0])
                else:
                    loclist_B.append(s[0])
                    E[s[0]] = s[1]
            w = time_pat.finditer(line)
            for it in w:
                s = it.span()
                s = (s[0]+5, s[1]-1)
                if s[1]-s[0] == 1:
                    timelist_S.append(s[0])
                else:
                    timelist_B.append(s[0])
                    E[s[0]] = s[1]
            w = name_pat.finditer(line)
            for it in w:
                s = it.span()
                s = (s[0]+12, s[1]-1)
                if s[1]-s[0] == 1:
                    namelist_S.append(s[0])
                else:
                    namelist_B.append(s[0])
                    E[s[0]] = s[1]

            tot = len(line)
            i = 0
            while i < tot:
                if i in timelist_B:
                    trainfile.write(line[i]+' B-TIME\n')
                    l = E[i]-i-2
                    while l:
                        i += 1
                        l -= 1
                        trainfile.write(line[i]+' M-TIME\n')
                    i += 1
                    trainfile.write(line[i]+' E-TIME\n')
                elif i in timelist_S:
                    trainfile.write(line[i]+' S-TIME\n')

                elif i in loclist_B:
                    trainfile.write(line[i]+' B-LOC\n')
                    l = E[i]-i-2
                    while l:
                        i += 1
                        l -= 1
                        trainfile.write(line[i]+' M-LOC\n')
                    i += 1
                    trainfile.write(line[i]+' E-LOC\n')
                elif i in loclist_S:
                    trainfile.write(line[i]+' S-LOC\n')

                elif i in orglist_B:
                    trainfile.write(line[i]+' B-ORG\n')
                    l = E[i]-i-2
                    while l:
                        i += 1
                        l -= 1
                        trainfile.write(line[i]+' M-ORG\n')
                    i += 1
                    trainfile.write(line[i]+' E-ORG\n')
                elif i in orglist_S:
                    trainfile.write(line[i]+' S-ORG\n')

                elif i in namelist_B:
                    trainfile.write(line[i]+' B-NAME\n')
                    l = E[i]-i-2
                    while l:
                        i += 1
                        l -= 1
                        trainfile.write(line[i]+' M-NAME\n')
                    i += 1
                    trainfile.write(line[i]+' E-NAME\n')
                elif i in namelist_S:
                    trainfile.write(line[i]+' S-NAME\n')

                elif line[i] != '':
                    trainfile.write(line[i]+' O\n')
                    #print(line[i]+' O')
                i += 1
            trainfile.write('\n')
        for k in range(limit, totline):
            line = re.sub(' +', '', file[k])
            line = line.replace('\n', '').replace('\t', '')
            if line == '':
                continue
            orglist_B = []
            loclist_B = []
            timelist_B = []
            namelist_B = []
            E = {}
            orglist_S = []
            loclist_S = []
            timelist_S = []
            namelist_S = []
            w = org_pat.finditer(line)
            for it in w:
                s = it.span()
                s = (s[0]+9, s[1]-1)
                if s[1]-s[0] == 1:
                    orglist_S.append(s[0])
                else:
                    orglist_B.append(s[0])
                    E[s[0]] = s[1]
            w = loc_pat.finditer(line)
            for it in w:
                s = it.span()
                s = (s[0]+9, s[1]-1)
                if s[1]-s[0] == 1:
                    loclist_S.append(s[0])
                else:
                    loclist_B.append(s[0])
                    E[s[0]] = s[1]
            w = time_pat.finditer(line)
            for it in w:
                s = it.span()
                s = (s[0]+5, s[1]-1)
                if s[1]-s[0] == 1:
                    timelist_S.append(s[0])
                else:
                    timelist_B.append(s[0])
                    E[s[0]] = s[1]
            w = name_pat.finditer(line)
            for it in w:
                s = it.span()
                s = (s[0]+12, s[1]-1)
                if s[1]-s[0] == 1:
                    namelist_S.append(s[0])
                else:
                    namelist_B.append(s[0])
                    E[s[0]] = s[1]

            tot = len(line)
            i = 0
            while i < tot:
                if i in timelist_B:
                    testfile.write(line[i]+' B-TIME\n')
                    l = E[i]-i-2
                    while l:
                        i += 1
                        l -= 1
                        testfile.write(line[i]+' M-TIME\n')
                    i += 1
                    testfile.write(line[i]+' E-TIME\n')
                elif i in timelist_S:
                    testfile.write(line[i]+' S-TIME\n')

                elif i in loclist_B:
                    testfile.write(line[i]+' B-LOC\n')
                    l = E[i]-i-2
                    while l:
                        i += 1
                        l -= 1
                        testfile.write(line[i]+' M-LOC\n')
                    i += 1
                    testfile.write(line[i]+' E-LOC\n')
                elif i in loclist_S:
                    testfile.write(line[i]+' S-LOC\n')

                elif i in orglist_B:
                    testfile.write(line[i]+' B-ORG\n')
                    l = E[i]-i-2
                    while l:
                        i += 1
                        l -= 1
                        testfile.write(line[i]+' M-ORG\n')
                    i += 1
                    testfile.write(line[i]+' E-ORG\n')
                elif i in orglist_S:
                    testfile.write(line[i]+' S-ORG\n')

                elif i in namelist_B:
                    testfile.write(line[i]+' B-NAME\n')
                    l = E[i]-i-2
                    while l:
                        i += 1
                        l -= 1
                        testfile.write(line[i]+' M-NAME\n')
                    i += 1
                    testfile.write(line[i]+' E-NAME\n')
                elif i in namelist_S:
                    testfile.write(line[i]+' S-NAME\n')

                elif line[i] != ' ':
                    testfile.write(line[i]+' O\n')
                i += 1
            testfile.write('\n')
    """
    tot:
        time:  4216
        location:  4581
        organization:  2672
    """
    trainfile.close()
    testfile.close()


def pre():
    trainfile = open('data\\train.char.bmes', 'w',
                     encoding='utf-8', errors='ignore')
    testfile = open('data\\test.char.bmes', 'w',
                    encoding='utf-8', errors='ignore')
    PKU98 = '../data/pku98'
    PKU199801_TRAIN = os.path.join(PKU98, '199801-train.txt')
    PKU199801_TEST = os.path.join(PKU98, '199801-test.txt')
    org_pat = re.compile('\[([^]]*?)]/nt')
    with open(PKU199801_TRAIN, 'r', encoding='UTF-8') as ff:
        file = ff.readlines()
        org_list = []
        for line in file:
            org = org_pat.findall(line)
            for each in org:
                org_list.append(re.sub('[a-z\s/]+', '', each))

        print(org_list)


pre()
