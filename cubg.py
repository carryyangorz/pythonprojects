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
# browser=webdriver.Chrome(options=option,desired_capabilities=capa)
# browser.implicitly_wait(6)
import multiprocessing
from multiprocessing import Process,Lock
# import multiprocessing_win
headers={
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
        }
baseurl="https://image.cubg.cn/search?sort=default&text="

def getone(target):
    browser=webdriver.Chrome(options=option,desired_capabilities=capa)

    i=0
    url=baseurl+target+'&taxonId='
    browser.get(url)
    js="var q=document.documentElement.scrollTop=100000"
    finish=True
    browser.execute_script(js)
    sleep(2)
    ttt=len(browser.find_elements_by_css_selector('div.grid__item'))
    # print(ttt)
    while finish:
        browser.execute_script(js)
        print(target+'      searching...')
        sleep(2)

        try:
            if browser.find_element_by_css_selector('div#imloading.loadmore').text=='您已看完所有照片！':
                finish=False
                print(target+'      search over')
        except:
            finish=False
            print(target+'      search over')
            break
        tttttt=len(browser.find_elements_by_css_selector('div.grid__item'))
        # print(tttttt)
        if tttttt==ttt:
            print(target+'      search over')
            break
    browser.execute_script(js)
    sleep(3)
    aa=browser.find_elements_by_css_selector('div.grid__item')
    als=[]
    bls=[]
    cls=[]
    dls=[]
    ppls=[]
    num=len(aa)
    print(target+'  '+str(num) +'   total')
    for item in aa:
        ch=item.find_element_by_css_selector('div.c_title.tdf').text
        lt=item.find_element_by_css_selector('div.tdf.l_title').text
        name=lt+'_'+ch
        als.append(name)
        picurl1=item.find_element_by_css_selector('img.grid__img').get_attribute('src')
        picurl=picurl1.replace('smthumb','midthumb')
        bls.append(picurl)
        picauthurl=item.find_element_by_css_selector('a[target="_blank"]').get_attribute('href')
        dls.append(picauthurl)
        picauth=item.find_element_by_css_selector('a[target="_blank"]').text
        cls.append(picauth)
    # num=len(als)
    browser.quit()
        # print(target+'  '+str(num) +'   total')
        # f=open(target+'\\'+target+'_'+str(i)+'.jpg','wb')
        # try:
        #     r=requests.get(picurl,headers=headers)#,verify=False)
        # except:
        #     print('error')
        #     # continue
        #     return
        # # r.raise_for_status()
        # f.write(r.content)
        # i=i+1
        # print(i)
        # f.close()
        # f=open(target+'\\'+target+'.txt','a')
        # f.write('\n'+target+'_'+str(i)+'.jpg''\t'+picurl+'\t'+picauth+'\t'+picauthurl)
        # f.close()
    while True:
        for _ in range(8):
            if i>len(als)-1:
                    return
            data=[als[i],bls[i],target,i]
            pp=Process(target=download,args=(data,))
            # i=i+1
            # if i>len(bb):
            #         break
            pp.start()
            ppls.append(pp)
            f=open(target+'\\'+target+'.txt','a')
            f.write('\n'+als[i]+'_'+str(i)+'.jpg''\t'+bls[i]+'\t'+bls[i].replace('midthumb','smthumb')+'\t'+cls[i]+'\t'+dls[i])
            f.close()
            i=i+1
        for thread in ppls:
            thread.join()
    
def download(data):
    global i
    name=data[0]
    picurl=data[1]
    target=data[2]
    i=data[3]
    f=open(target+'\\'+name+'_'+str(i)+'.jpg','wb')
    try:
        r=requests.get(picurl,headers=headers)#,verify=False)
    except:
        print('error')
        # continue
        return
    # r.raise_for_status()
    f.write(r.content)
    # i=i+1
    print(i)
    f.close()


if __name__ == "__main__":
    multiprocessing.freeze_support()
    f = open("plant.txt",encoding='utf-8')
    line = f.readline()
    ls=[]
    # errorls=[]
    while line:
        ls.append(line.replace('\n',''))
        line = f.readline()
    f.close()
    for item in ls:
        # num=0
        if not os.path.exists(item+'\\'):
            os.makedirs(item+'\\')
            getone(item)
        else:
            print(item+'  已经存在')
            pass
        # getone(item)
    # getone('Abelia macrotera')
    os.system('pause')