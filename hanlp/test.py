from pyhanlp import *
import re
PKU98 = '../../data/pku98'
PKU199801 = os.path.join(PKU98, '199801.txt')
PKU199801_TRAIN = os.path.join(PKU98, '199801-train.txt')
PKU199801_TEST = os.path.join(PKU98, '199801-test.txt')
testfile = open(PKU199801_TEST, 'r', encoding='utf-8', errors='ignore')


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


a = open('1998.txt', 'r', encoding='utf-8', errors='ignore')
a = a.readline()
viterbiNewSegment = HanLP.newSegment("viterbi")
CRFnewSegment = HanLP.newSegment("crf")

a = CRFnewSegment.seg(a)
#a = viterbiNewSegment.seg(a)
words = ' '
for term in a:
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
