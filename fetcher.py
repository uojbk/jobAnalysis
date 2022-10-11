from dataclasses import replace
from tracemalloc import start
import requests
import json
import time

sess = requests.Session()
sess.headers.update({
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-language": "en,zh-CN;q=0.9,zh;q=0.8",
    "cache-control": "max-age=0",
    "sec-ch-ua": "\"Google Chrome\";v=\"105\", \"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"105\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1"
})

JobListFileName = 'jobListData.json'
JobListFilePath = f'D:\dataAna\jobAnalysis\{JobListFileName}'
starter = '__INITIAL_STATE__='
ender = '</script><script src="'
def get_joblist(url)->dict:
    html = sess.get(url).text
    startIndex = html.index(starter)
    endIndex = html.index(ender)
    data = html[startIndex: endIndex]
    data = data.replace('__INITIAL_STATE__=', '')
    return json.loads(data)

def fetch_all_city_list():



    initData = get_joblist('https://sou.zhaopin.com/?jl=530&kw=%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90&p=1')
    # print(data['baseData']['hotCity'])
    
    jobListData = []

    for city in initData['baseData']['hotCity']:
        url = f'https://sou.zhaopin.com/?jl={city["code"]}&kw=%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90&p=1'
        print(url)
        jobListData.append(get_joblist(url))

    with open(JobListFilePath, 'w', encoding='utf8') as f:
        f.write(json.dumps(jobListData))


def get_detail(url)->dict:
    print(url)
    time.sleep(1)
    starter = '__INITIAL_STATE__='
    ender = '</script><script src="'
    # with open('D:\dataAna\jobAnalysis\headers.json', 'r') as f:
    #     hds = json.load(f)
    #     hds['user-agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'

    html = sess.get(url).text
    with open(f'D:\dataAna\jobAnalysis\errorPath.html', 'w', encoding='utf8') as f:
        f.write(html)
    startIndex = html.index(starter)
    endIndex = html.index(ender)
    data = html[startIndex: endIndex]
    data = data.replace('__INITIAL_STATE__=', '')
    data = json.loads(data)
    print(data)
    stop




if __name__ == '__main__':
    # joblist = None
    # with open(JobListFilePath, 'r', encoding='utf8') as f:
    #     joblist = json.load(f)
    #     print(len(joblist))

    # for city in joblist:
    #     sbd = city['statBaseData']
    #     for pos in city['positionList']:
    #         url = f"{pos['positionURL']}?refcode={sbd['pagecode']}&srccode={sbd['funczone']}&preactionid={sbd['actionid']}"
    #         detail = get_detail(url)
    #         time.sleep(0.1)
    cityurl = 'https://sou.zhaopin.com/?jl=530&kw=%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90&p=1'
    city = get_joblist(cityurl)
    sbd = city['statBaseData']
    for pos in city['positionList']:
        url = f"{pos['positionURL']}?refcode={sbd['pagecode']}&srccode={sbd['funczone']}&preactionid={sbd['actionid']}"
        sess.headers.update({'Referer': cityurl})
        print(sess.headers)
        detail = get_detail(url)
        time.sleep(0.1)

