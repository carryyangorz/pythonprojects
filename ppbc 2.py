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
capa = DesiredCapabilities.CHROME
capa["pageLoadStrategy"] = "eager"
option=ChromeOptions()
option.add_argument('--headless')
option.add_argument('--no-sandbox')
option.add_argument('log-level=3') #INFO = 0 WARNING = 1 LOG_ERROR = 2 LOG_FATAL = 3 default is 0
option.add_experimental_option('excludeSwitches',['enable-automation'])
browser=webdriver.Chrome(options=option,desired_capabilities=capa)
browser.implicitly_wait(6)

from pyquery import PyQuery as pq
baseurl='http://ppbc.iplant.cn/tu/'
headers={
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36',
        'Referer':'http://ppbc.iplant.cn/'
        }
def getone(num):
    browser.get(baseurl+str(num))
    sleep(1)
    try:
        cc=browser.find_element_by_css_selector('div.divcen')
    except:
        print(str(num)+'图片不存在')
        return
    aa=cc.find_element_by_css_selector('img')
    url=aa.get_attribute('src')
    bb=browser.find_element_by_css_selector('div#txt_classsys')
    name=bb.find_element_by_css_selector('b').text
    cname=name.split(' ')[0]
    lname=name.replace(cname+' ','')
    cc=browser.find_element_by_css_selector('div.fr').text
    id=re.findall('id:(.*)',cc)[0]
    name=lname+'_'+cname+'_'+id
    print(str(num))
    print(name)
    print(url)
    if os.path.exists(name+'.jpg'):
        print('图片已存在')
        print('--------------------------------------')
        return
    r=requests.get(url,headers=headers)
    f=open(name+'.jpg','wb')
    f.write(r.content)
    f.close()
    f=open('url.txt','a')
    f.write('\n'+name+'\t'+baseurl+str(num))
    print('--------------------------------------')

if __name__ == "__main__":
    if not os.path.exists('index.txt'):
        f=open('index.txt','w')
        f.write('1')
        f.close()
    f=open('index.txt','r')
    index=f.readline()
    print(index)
    for i in range(int(index),8000000):
        getone(i)
        f=open('index.txt','w')
        f.write(str(i))
        f.close()
        
    # getone(7676254)