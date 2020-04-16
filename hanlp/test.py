from pyhanlp import *
"""
HanLP开启命名实体识别

"""

# 音译人名示例
CRFnewSegment = HanLP.newSegment("crf")
term_list = CRFnewSegment.seg("译智社的田丰要说的是这只是一个hanlp命名实体识别的例子")
print(term_list)


print("\n========== 命名实体开启与关闭对比试验 ==========\n")
sentences = [
    "北川景子参演了林诣彬导演的《速度与激情3》",

]
# 通过HanLP 进行全局设置,但是部分分词器本身可能不支持某项功能
# 部分分词器本身对某些命名实体识别效果较好

viterbiNewSegment = HanLP.newSegment("viterbi")
CRFnewSegment_new = HanLP.newSegment("crf")
# segSentence
# CRFnewSegment_2.seg2sentence(sentences)
for sentence in sentences:
    print("crf : ", CRFnewSegment.seg(sentence))
    print("crf_new : ", CRFnewSegment_new.seg(sentence))
    print("viterbi : ", viterbiNewSegment.seg(sentence))
