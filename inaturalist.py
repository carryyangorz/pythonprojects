# Source Generated with Decompyle++
# File: inaturalist.pyc (Python 3.8)

import requests
import os
import time
import re
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from threading import Timer
import threading
from threading import Timer
import multiprocessing
from multiprocessing import Process
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36' }

delay=2
num=100
def get(baseurl):
    browser.get(baseurl)
    sleep(1)
    tab = browser.find_element_by_css_selector('div.TaxonPageTabs')
    a = tab.find_element_by_css_selector('div.col-xs-12')
    a.find_elements_by_css_selector('li')[3].click()
    sleep(1)
    b = browser.find_element_by_css_selector('div.TaxonomicBranch')
    c = b.find_elements_by_css_selector('li.all-shown.tabular')
    i = 0
    ls = []
    for item in c:
        count = item.text.split(' ')[-1]
        if count != '0':
            print(str(i) + '---' + item.text)
            ls.append(item)
            i = i + 1
    print('请选择： 输入数字并回车')
    num = int(input())
    url = ls[num].find_elements_by_css_selector('a')[0].get_attribute('href')
    print(url)
    getsub(url)


def getsub(url):
    browser.get(url)
    sleep(1)
    tab = browser.find_element_by_css_selector('div.TaxonPageTabs')
    d = tab.find_element_by_css_selector('div.col-xs-12')
    d.find_elements_by_css_selector('li')[3].click()
    sleep(1)
    e = browser.find_element_by_css_selector('div.TaxonomicBranch')
    f = e.find_elements_by_css_selector('li.all-shown.tabular')
    i = 0
    ls = []
    for item in f:
        count = item.text.split(' ')[-1]
        if count != '0':
            print(str(i) + '---' + item.text)
            ls.append(item)
            i = i + 1
    print('请选择： 输入数字并回车')
    num = int(input())
    url = ls[num].find_elements_by_css_selector('a')[0].get_attribute('href')
    print(url)
    getfinal(url)


def getfinal(url):
    browser.get(url)
    sleep(1)
    tab = browser.find_element_by_css_selector('div.TaxonPageTabs')
    d = tab.find_element_by_css_selector('div.col-xs-12')
    d.find_elements_by_css_selector('li')[3].click()
    sleep(1)
    e = browser.find_element_by_css_selector('ul.plain.taxonomy')
    f = e.find_elements_by_css_selector('li.all-shown.tabular')
    i = 0
    uls = []
    nls = []
    for item in f:
        count = item.text.split(' ')[-1]
        if count != '0':
            print(str(i) + '---' + item.text)
            url = item.find_elements_by_css_selector('a')[-1].get_attribute('href')
            name = re.findall('[a-zA-Z]{2,100}', item.text)[0]
            uls.append(url)
            nls.append(name)
            i = i + 1
    for i in range(0, len(uls)):
        download(uls[i], nls[i])


def download(aurl, name):
    id = re.findall('taxon_id=(.*)&place', aurl)[0]
    url = 'https://api.inaturalist.org/v1/observations?verifiable=any&order_by=observations.id&order=desc&page=1&spam=false&taxon_id=' + id + '&locale=zh-CN&per_page=200'
    browser.get(url)
    ls = []
    aaa = browser.find_element_by_css_selector('pre').text
    total = re.findall('total_results":(.*),"page', aaa)[0]
    pages = int(total) // 200 + 2
    for i in range(1, pages):
        print(i)
        url = 'https://api.inaturalist.org/v1/observations?verifiable=any&order_by=observations.id&order=desc&page=' + str(i) + '&spam=false&taxon_id=' + id + '&locale=zh-CN&per_page=200'
        browser.get(url)
        aaa = browser.find_element_by_css_selector('pre').text
        b = re.findall('square_url":"(.*?)","attribution', aaa)
        print(len(b))
        for item in b:
            if 'inaturalist' in item:
                ls.append(item)
                i = i + 1
    lss = list(set(ls))
    print(len(lss))
    print(name + '   total:   ' + str(len(lss)))
    i = 1
    if not os.path.exists(name + '\\'):
        os.mkdir(name + '\\')
    for item in lss:
        picurl = item.replace('square', 'large')
        r = requests.get(picurl, headers, **('headers',))
        f = open(name + '\\' + name + '_' + str(i) + '.jpg', 'wb')
        f.write(r.content)
        f.close()
        f = open('url.txt', 'a')
        f.write('\n' + name + '_' + str(i) + '\t' + aurl)
        f.close()
        print(name + '   ' + str(i))
        i = i + 1


def downloadone(data):
    id = data[0]
    i = data[1]
    name = data[2]
    delay = data[3]
    sleep(delay)
    curl = 'https://www.inaturalist.org/observations/' + id
    if os.path.exists(name + '\\' + name + '_' + str(i) + '_' + id + '.jpg'):
        print(name + '\\' + name + '_' + str(i) + '_' + id + '.jpg   exists')
        return
    rr = requests.get(curl, headers=headers)    
    try:
        picurl = re.findall('<meta content="(https://.*[0-9]{0,20})" property="og:image', rr.text)[0]
    except:
        try:
            print(name + '   ' + str(i) + '   ' + id + '  retry')
            sleep(8)
            rr = requests.get(curl, headers=headers)
            picurl = re.findall('<meta content="(https://.*[0-9]{0,20})" property="og:image', rr.text)[0]
            print(name + '   ' + str(i) + '   retry success!!')
        except:
            print(name + '   ' + str(i) + '   retry still fail')
            return None
    
    r = requests.get(picurl, headers=headers)
    f = open(name + '\\' + name + '_' + str(i) + '_' + id + '.jpg', 'wb')
    f.write(r.content)
    f.close()
    f = open(name + '\\' + 'url.txt', 'a')
    f.write('\n' + name + '_' + str(i) + '_' + id + '\t' + curl)
    f.close()
    print(name + ' +1  ' + str(i))

def getid(name):
    tar = name.replace(' ', '+')
    url = 'https://api.inaturalist.org/v1/taxa/autocomplete?q=' + tar + '&per_page=10&locale=zh-CN&preferred_place_id='
    r = requests.get(url, headers=headers)
    
    try:
        id = re.findall('"id":([0-9]{0,10}),"', r.text)[0]
        thatname=re.findall('name":"(.*?)","parent_id', r.text)[0]
        # print(thatname)
        if thatname!=name:
            print(name + ' no result, over')
            return None
    except:
        print(name + ' no result, over')
        return None
    i = 0
    page=1
    picidls=[]
    # print(id)
    if not os.path.exists(name + '\\'):
        os.mkdir(name + '\\')

    while True:
        burl = 'https://api.inaturalist.org/v1/observations?verifiable=true&order_by=observations.id&order=desc&page='+str(page)+'&spam=false&taxon_id=' + id + '&locale=zh-CN&per_page=200'
        r = requests.get(burl, headers=headers)
        sleep(1)
        # print(r.text)
        picid = re.findall('id":([0-9]{0,10}),"cached_votes_total', r.text)
        # picidls.append(picid)
        for item in picid:
            picidls.append(item)
        page+=1
        print(name + '  totally   ' + str(len(picidls)))
        print(len(picid))
        if len(picid) < 1:
            break
        if len(picidls)>=num:
            break

    ppls = []
    flag=True
    while flag:
        for _ in range(8):
            if i > len(picidls) - 1:
                flag=False
                continue
            if i > num-1:
                flag=False
                continue
            data = [picidls[i],i,name,delay]
            pp = Process(target=downloadone,args=(data,))
            i = i + 1
            pp.start()
            ppls.append(pp)
        for thread in ppls:
            thread.join()

if __name__ == '__main__':
    multiprocessing.freeze_support()
    if not os.path.exists('index.txt'):
        f = open('index.txt', 'w')
        f.write('0')
        f.close()
        index = 0
    else:
        f = open('index.txt', 'r')
        index = int(f.readline())
        f.close()
    f = open('名录.txt', 'r')
    names = f.readlines()
    f.close()
    print('请输入图片下载时间间隔，单位秒：')
    delay = int(input())
    print('请输入一个物种图片下载数目：输入all下载全部')

    num = input()
    if num=='all':
        num=9999999
    else:
        num=int(num)
    while True:
        # index=1
        item = names[index]
        item = item.replace('\n', '')
        print(item + '    ----------------------------')
        index = index + 1
        f = open('index.txt', 'w')
        f.write(str(index))
        f.close()
        if os.path.exists(item + '\\'):
            print(item + '  already there')
            continue
        getid(item)

