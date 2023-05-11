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
capa = DesiredCapabilities.CHROME
capa["pageLoadStrategy"] = "eager"
option=ChromeOptions()
option.add_argument('--headless')
option.add_argument('--no-sandbox')
option.add_argument('log-level=3') #INFO = 0 WARNING = 1 LOG_ERROR = 2 LOG_FATAL = 3 default is 0
option.add_experimental_option('excludeSwitches',['enable-automation'])
browser1=webdriver.Chrome(options=option,desired_capabilities=capa)
browser2=webdriver.Chrome(options=option,desired_capabilities=capa)
browser3=webdriver.Chrome(options=option,desired_capabilities=capa)
browser4=webdriver.Chrome(options=option,desired_capabilities=capa)
browser5=webdriver.Chrome(options=option,desired_capabilities=capa)
browser6=webdriver.Chrome(options=option,desired_capabilities=capa)
browser7=webdriver.Chrome(options=option,desired_capabilities=capa)
bls=[browser1,browser2,browser3,browser4,browser5,browser6,browser7]
# browser.implicitly_wait(6)

from pyquery import PyQuery as pq
baseurl='http://ppbc.iplant.cn/tu/'
headers={
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36',
        'Referer':'http://ppbc.iplant.cn/'
        }
def getone(a):
    ids=[]
    f=open('id.txt','r')
    ids=f.readlines()
    f.close()
    browser=bls[a]
    while True:
        f=open('index.txt','r')
        index=int(f.readline())
        f.close()

        va=str(index+1)
        # print(va)
        f=open('index.txt','w')
        f.write(va)
        f.close()
        num=ids[index]
    # print(str(index))
        folder=str(index//1000)
        if not os.path.exists(folder+'\\'):
            os.mkdir(folder+'\\')
        # browser=webdriver.Chrome(options=option,desired_capabilities=capa)

        

        browser.get(baseurl+str(num))
        print('sssssssssssssssssss'+str(num))
        sleep(1)
        try:
            cc=browser.find_element_by_css_selector('div.divcen')

            aa=cc.find_element_by_css_selector('img')
            
            url=aa.get_attribute('src')
            bb=browser.find_element_by_css_selector('div#txt_classsys')
            name=bb.find_element_by_css_selector('b').text
            cname=name.split(' ')[0]
            lname=name.replace(cname+' ','')
            cc=browser.find_element_by_css_selector('div.fr').text
        except:
            print(str(num)+'图片不存在')
            continue
        id=re.findall('id:(.*)',cc)[0]
        name=lname+'_'+cname+'_'+id
        print('--------------------------------------')
        print(str(num))
        print(name)
        print(url)
        print('--------------------------------------')
        if os.path.exists(folder+'\\'+name+'.jpg'):
            print('图片已存在')
            continue
        r=requests.get(url,headers=headers)
        f=open(folder+'\\'+name+'.jpg','wb')
        f.write(r.content)
        f.close()
        index=index+1
        f=open('url.txt','a')
        f.write('\n'+name+'\t'+baseurl+str(num))
        f.close()

    # print('--------------------------------------')
if __name__ == "__main__":
    
    # multiprocessing.freeze_support()
    if not os.path.exists('index.txt'):
        f=open('index.txt','w')
        f.write('1')
        f.close()
        index=0
    else:
        f=open('index.txt','r')
        index=int(f.readline())
        f.close()

    # ids=[]
    # f=open('id.txt','r')
    # ids=f.readlines()
    # f.close()
    # print(len(ids))
    for i in range(0,7):
        t1=threading.Thread(target=getone,args=(i,))
    # t2=threading.Thread(target=getone,args=(1,))
    # t3=threading.Thread(target=getone,args=(2,))
    # t4=threading.Thread(target=getone,args=(3,))
    # t5=threading.Thread(target=getone,args=(4,))
    # t1.start()
    # t2.start()
    # t3.start()
    # t4.start()
        t1.start()

