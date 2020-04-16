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


def BMEOS(line, ty, B, E, file):
    tot = len(line)
    i = 0
    num = len(ty)
    while i < tot:
        flag = 0
        for j in range(num):
            if i in B[j]:
                l = E[i]-i-2

                if l == -1:
                    file.write(line[i]+' S-'+ty[j]+'\n')
                else:
                    file.write(line[i]+' B-'+ty[j]+'\n')
                    while l:
                        i += 1
                        l -= 1
                        file.write(line[i]+' M-'+ty[j]+'\n')
                    i += 1
                    file.write(line[i]+' E-'+ty[j]+'\n')
                flag = 1
                break
        if flag == 0:
            file.write(line[i]+' O\n')
        i += 1
    file.write('\n')


def pre_Boson():
    trainfile = open('data\\train.char.bmes', 'w',
                     encoding='utf-8', errors='ignore')
    testfile = open('data\\test.char.bmes', 'w',
                    encoding='utf-8', errors='ignore')
    org_pat = re.compile('org_name:(\S*?)}')
    loc_pat = re.compile('location:(\S*?)}')
    time_pat = re.compile('time:(\S*?)}')
    name_pat = re.compile('person_name:(\S*?)}')
    with open('../../data/BosonNLP_NER_6C.txt', 'r', encoding='UTF-8') as ff:
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
            w = org_pat.finditer(line)
            for it in w:
                s = it.span()
                s = (s[0]+9, s[1]-1)
                orglist_B.append(s[0])
                E[s[0]] = s[1]
            w = loc_pat.finditer(line)
            for it in w:
                s = it.span()
                s = (s[0]+9, s[1]-1)
                loclist_B.append(s[0])
                E[s[0]] = s[1]
            w = time_pat.finditer(line)
            for it in w:
                s = it.span()
                s = (s[0]+5, s[1]-1)
                timelist_B.append(s[0])
                E[s[0]] = s[1]
            w = name_pat.finditer(line)
            for it in w:
                s = it.span()
                s = (s[0]+12, s[1]-1)
                namelist_B.append(s[0])
                E[s[0]] = s[1]
            BMEOS(line, ['TIME', 'LOC', 'ORG', 'NAME', ],
                  [timelist_B, loclist_B, orglist_B, namelist_B], E, trainfile)

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
            BMEOS(line, ['TIME', 'LOC', 'ORG', 'NAME', ],
                  [timelist_B, loclist_B, orglist_B, namelist_B], E, testfile)

    """
    tot:
        time:  4216
        location:  4581
        organization:  2672
    """


def find_all(sub, s):
    index_list = []
    index = s.find(sub)
    while index != -1:
        index_list.append(index)
        index = s.find(sub, index+1)

    if len(index_list) > 0:
        return index_list
    else:
        return -1


def origin(fin, fout):
    with open(fin, 'r', encoding='UTF-8') as ff:
        file = ff.readlines()
        for line in file:
            sentence = re.sub('[a-z\s/\[\]]+', '', line)
            fout.write(sentence)


def pre(fin, fout):
    article = ''
    org_mulpat = re.compile('\[([^]]*?)]/nt[a-z]*')
    org_pat = re.compile('[\[\s](\S*?)/nt[a-z]*')
    name_pat = re.compile('[\[\s](\S*?)/nr[a-z]*')
    time_mulpat = re.compile('\[([^]]*?)]/t[a-z]*')
    time_pat = re.compile('[\[\s](\S*?)/t[a-z]*')
    loc_mulpat = re.compile('\[([^]]*?)]/ns[a-z]*')
    loc_pat = re.compile('[\[\s](\S*?)/ns[a-z]*')
    with open(fin, 'r', encoding='UTF-8') as ff:
        file = ff.readlines()
        for line in file:
            org_list = []
            loc_list = []
            time_list = []
            name_list = []
            article = line
            org = org_pat.findall(line)
            for each in org:
                org_list.append(re.sub('[a-z\s/\[\]]+', '', each))
            org = org_mulpat.findall(line)
            for each in org:
                org_list.append(re.sub('[a-z\s/\[\]]+', '', each))
            org_list = list(set(org_list))
            loc = org_pat.findall(line)
            for each in loc:
                loc_list.append(re.sub('[a-z\s/\[\]]+', '', each))
            loc = loc_mulpat.findall(line)
            for each in loc:
                loc_list.append(re.sub('[a-z\s/\[\]]+', '', each))
            loc_list = list(set(loc_list))
            time = time_pat.findall(line)
            for each in time:
                time_list.append(re.sub('[a-z\s/\[\]]+', '', each))
            time = time_mulpat.findall(line)
            for each in time:
                time_list.append(re.sub('[a-z\s/\[\]]+', '', each))
            time_list = list(set(time_list))
            name = name_pat.findall(line)
            for each in name:
                name_list.append(re.sub('[a-z\s/\[\]]+', '', each))
            name_list = list(set(name_list))
            article = re.sub('[a-z\s/\[\]]+', '', article)

            orglist_B = []
            loclist_B = []
            timelist_B = []
            namelist_B = []
            E = {}
            for w in org_list:
                indexlist = find_all(w, article)
                l = len(w)
                for b in indexlist:
                    orglist_B.append(b)
                    E[b] = b+l
            for w in loc_list:
                indexlist = find_all(w, article)
                l = len(w)
                for b in indexlist:
                    loclist_B.append(b)
                    E[b] = b+l
            for w in time_list:
                indexlist = find_all(w, article)
                l = len(w)
                for b in indexlist:
                    timelist_B.append(b)
                    E[b] = b+l
            for w in name_list:
                indexlist = find_all(w, article)
                l = len(w)
                for b in indexlist:
                    namelist_B.append(b)
                    E[b] = b+l
            BMEOS(article, ['TIME', 'LOC', 'ORG', 'NAME', ],
                  [timelist_B, loclist_B, orglist_B, namelist_B], E, fout)


original = open('data\\1998.txt', 'w',
                encoding='utf-8', errors='ignore')
trainfile = open('data\\train.char.bmes', 'w',
                 encoding='utf-8', errors='ignore')
testfile = open('data\\test.char.bmes', 'w',
                encoding='utf-8', errors='ignore')
PKU98 = '../../data/pku98'
PKU199801_TRAIN = os.path.join(PKU98, '199801-train.txt')
PKU199801_TEST = os.path.join(PKU98, '199801-test.txt')
pre(PKU199801_TRAIN, trainfile)
pre(PKU199801_TEST, testfile)
#origin(PKU199801_TEST, original)
trainfile.close()
testfile.close()
# original.close()
