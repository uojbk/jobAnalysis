from playwright.sync_api import sync_playwright, Response
from requests import head
import random
import json


exepath = 'C:\Program Files\Google\Chrome\Application\chrome.exe'

JobListFileName = 'jobListData.json'
JobListFilePath = f'D:\dataAna\jobAnalysis\{JobListFileName}'
JobDettailData = {}

def monitor_response(res: Response):
    if 'position-detail-new?' in res.url:
        data = res.json()['data']
        pn = data['detailedPosition']['positionNumber']
        JobDettailData[pn] = data
        print('>>>>>>>>>>>>>>>>>>>>>', pn)






hotcities = None
with open(r'D:\dataAna\jobAnalysis\testData\joblistdata.json', 'r', encoding='utf8') as f:
    hotcities = json.load(f)['baseData']['hotCity']
    
    print(len(hotcities))


with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        executable_path=exepath, 
        headless=False, 
        user_data_dir=r'D:\temp\playwright'
    )
    page = browser.new_page()
    page.on("response", monitor_response)
    for city in hotcities:
        url = f'https://sou.zhaopin.com/?jl={city["code"]}&kw=%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90&p=1'
        print(url)
        page.goto(url)
        page.wait_for_timeout(1000)
    # /iteminfo__line1__jobname
    # iteminfo__line1__jobname__name
        for ele in page.query_selector_all('.iteminfo__line1__jobname'):
            print(ele)
            try:
                ele.hover()
            except:
                print('EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE')
                pass
            page.wait_for_timeout(500)
    # for i in range(5):
    #     page.hover('.iteminfo__line1__jobname')
    #     page.hover('.iteminfo__line1__jobname__name')
        page.wait_for_timeout(2000)
    page.wait_for_timeout(10000)
    browser.close()

with open(r'D:\dataAna\jobAnalysis\allJobDetailData.json', 'w', encoding='utf8') as f:
    json.dump(JobDettailData, f)