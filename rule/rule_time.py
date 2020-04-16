# -*- coding: utf-8 -*-
#!/usr/bin/python

import re
import os

# time
date_pattern = re.compile(
    '\d+年?\d+月\d+日|[0-9]{4}年起?初?末?|\d+月份?|\d+[号日]起?|\d+[~-]\d+[年月天日]|\d+-\d+-\d+|\d+.\d+')
time_pattern = re.compile(
    '20\d\d|[12]+[0-9][:：][0-9]{1,2}|[一二两三四五六七八九十\d]+点半?|0?[1-9][:：][0-9]{1,2}|\d+\S\d+[月天日]内?|yy'
    '\d+时|\d+分+\d+秒?|\d+点半|\d+点\d+分|\d+日?\d+点?\d+分?\d+秒?|T\d+:\d+:\d+|[一二两三四五六七八九十百千万\d]+个?月起?|[一二两三四五六七八九十百千万\d]+年')
N_pattern = re.compile(
    '国庆节前?后?|[父母]亲节|中秋节?前?后?|重阳节?前?后?|圣诞节前?后?|情人节前?后?|元旦前?后?|植树节前?后?|清明前?后?|劳动节前?后?|儿童节前?后?|建军节前?后?|教师节前?后?|'
    '[春夏秋冬][日天季]?|[鼠牛虎兔龙蛇马羊猴鸡狗猪]年|第\S季度|[上中下]+旬|[寒暑][假期]|第\S[年月天]|\S{2,5}时期')
D_pattern = re.compile(
    '[12][0-9]世纪|[12][09][0-9]{2}年度?|[一二两三四五六七八九十\d]+个?半?多?小时|[一二两三四五六七八九十\d]+个?半?钟头'
    '|[一二两三四五六七八九十\d]+个?半?[hH]|'
    '[一二两三四五六七八九十\d]+分多?钟|\d+秒|\d+s|\d+min|[一二两三四五六七八九十\d]+个星期|'
    '[零一二两三四五六七八九十百千万\d]+天|[零一二两三四五六七八九十百千万\d]+半年')
Rel_pattern = re.compile(
    '过去\S{1,3}[年月期]|未来\S{1,3}[年月期]|[前去今明后上下]+半?年|本月|这个月|下个?月|月底|月初|'
    '[当前昨今明后][一两]?[月日天][上中下]?午?|当晚|昨晚|昨夜|这个星期|[上这本下]周|大+前|后天|今|今后')
mix_pattern = re.compile(
    '昨天深夜|[上这本下]+周[一二两三四五六七天日1-7]|[上这本下]+星期[一二两三四五六七天日1-7]|[早晚]?[0-2]?[0-9][点时]半?|[上下]午\d+时'
    '去年\d+月\d+号|\d+/\d+/\d+:\d+:\d+.\d+|\d+月\d+日凌晨|\d+年\d+月|[一二两三四五六七八九十\d]+月[一二两三四五六七八九十\d]+[号日][早晚上下]?午?|[一二两三四五六七八九十\d]+月[上中下]+旬'
    '|\d+时\d+分|\d+日[零一二两三四五六七八九十百千万\d]+时\d+分|今年\d+月\d+日|\d+/\d+/\d+\d+:\d+:\d+.\d+|\d+日[上中下]午')
W_pattern = re.compile(
    '周[一二两三四五六七天日|1-7]|星期[一二两三四五六七天日|1-7]|礼拜[一二两三四五六七天日|1-7]')
F_pattern = re.compile(
    '每[年月日天小时分秒钟]+')
POD_pattern = re.compile(
    '凌晨|清晨|[下上中]午|午后|午间|傍晚|晚间|晚上|深夜|夜间|早上|年[初末]|年中')
shift_pattern = re.compile(
    '([前后]?[一二两三四五六七八九十百千万\d]+个?[年\S{1,2}|月|日|天|(小时)|(分钟)|周|(星期)|(礼拜)][以之]?[前后]?)')
pattern = re.compile('time:(\S+?)}')
mytimelist = []
timelist = []
with open('../data/BosonNLP_NER_6C.txt', 'r', encoding='UTF-8') as f:
    file = f.readlines()
    for line in file:
        T = pattern.findall(line)
        if T != []:
            for each in T:
                timelist.append(each)
        mytime = mix_pattern.findall(line)
        mytimelist.extend(mytime)

        mixlist = []

        mytime = D_pattern.findall(line)
        itlist = D_pattern.finditer(line)
        for it in itlist:
            mixlist.append(it.span())
        mytimelist.extend(mytime)

        mytime = N_pattern.findall(line)
        mytimelist.extend(mytime)
        itlist = N_pattern.finditer(line)
        for it in itlist:
            mixlist.append(it.span())

        mytime = date_pattern.findall(line)
        mytimelist.extend(mytime)
        itlist = date_pattern.finditer(line)
        for it in itlist:
            mixlist.append(it.span())

        mytime = time_pattern.findall(line)
        mytimelist.extend(mytime)
        itlist = time_pattern.finditer(line)
        for it in itlist:
            mixlist.append(it.span())

        mytime = F_pattern.findall(line)
        mytimelist.extend(mytime)
        itlist = F_pattern.finditer(line)
        for it in itlist:
            mixlist.append(it.span())

        mytime = W_pattern.findall(line)
        mytimelist.extend(mytime)
        itlist = W_pattern.finditer(line)
        for it in itlist:
            mixlist.append(it.span())

        mytime = shift_pattern.findall(line)
        mytimelist.extend(mytime)
        itlist = shift_pattern.finditer(line)
        for it in itlist:
            mixlist.append(it.span())

        mytime = POD_pattern.findall(line)
        mytimelist.extend(mytime)
        itlist = POD_pattern.finditer(line)
        for it in itlist:
            mixlist.append(it.span())

        mytime = Rel_pattern.findall(line)
        mytimelist.extend(mytime)
        itlist = Rel_pattern.finditer(line)
        for it in itlist:
            mixlist.append(it.span())

        mixlist = list(set(mixlist))
        mixlist.sort()
        length = len(mixlist)-1
        i = 0
        while i < length:
            if (mixlist[i][1] == mixlist[i+1][0]) or (mixlist[i][1]+1 == mixlist[i+1][0]):
                mixtime = line[mixlist[i][0]:mixlist[i+1][1]]
                mytimelist.append(mixtime)
                mixlist[i+1] = (mixlist[i][0], mixlist[i+1][1])
            i += 1


mytimelist = list(filter(None, mytimelist))
mytimeset = set(mytimelist)
timeset = set(timelist)
TP_set = mytimeset & timeset
FN_set = timeset - mytimeset
FP_set = mytimeset-timeset
# print(FN_set)
TP = len(TP_set)
FN = len(FN_set)
FP = len(FP_set)
precision = TP/(TP+FP)
recall = TP/(TP+FN)
print("recall: ", recall)
print("precision: ", precision)
print("F1: ", 2*precision*recall/(precision+recall))
