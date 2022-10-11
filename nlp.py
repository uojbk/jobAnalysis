from importlib.resources import path
import json
import re
import jieba
import jieba.posseg as pseg
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
from imageio import imread


with open(r'D:\dataAna\jobAnalysis\allJobDetailData.json', 'r') as f:
    data = json.load(f)

listData = []
TAG = re.compile('<.*?>')

def clean(des: str)->str:
    des = re.sub(TAG, '', des)
    cis = pseg.cut(des)
    rtn = []
    for ci, tag in  cis:
        if tag not in ('m', 'x'):
            rtn.append(ci)
    return rtn


def count(words: list):
    counts = {}
    for w in words:
        counts[w] = counts.get(w, 0) + 1
    rtn = list(counts.items())
    rtn.sort(key=lambda x: x[1], reverse=True)
    return rtn



words = []
for jobid in data:
    job = data[jobid]
    # listData.append([job['detailedPosition']['workCity'], clean(job['detailedPosition']['jobDesc']), job['detailedPosition']['positionStatus']])
    words += clean(job['detailedPosition']['jobDesc'])


back_coloring = imread(r'D:\dataAna\jobAnalysis\mask.png')
stopwords = '的，和，等，与，分析，数据，数据分析，及，并，相关，进行，对，业务，负责，工作，要求，项目，任职，有，或，岗位职责，以上'.split('，')
wc = WordCloud(
    font_path=r'C:\Windows\Fonts\STCAIYUN.TTF', 
    background_color="white", 
    max_words=2000, 
    mask=back_coloring,
    max_font_size=100, 
    random_state=42, 
    width=1000, 
    height=860, 
    margin=2,
    stopwords=stopwords,
)


wc.generate(' '.join(words))
wc.to_file(r'D:\dataAna\jobAnalysis\wordcloud1.png')

# plt.figure()
# # recolor wordcloud and show
# plt.imshow(wc, interpolation="bilinear")
# plt.axis("off")
# plt.show()
# cnts = count(words)
# print(cnts)
# wc.recolor(color_func=ImageColorGenerator(back_coloring))
# wc.to_file(r'D:\dataAna\jobAnalysis\wordcloud2.png')



if __name__ == '__main__':
    pass