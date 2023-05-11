import requests
import os
import time
import re
from urllib import parse
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import difflib
import urllib
from threading import Timer
capa = DesiredCapabilities.CHROME
capa["pageLoadStrategy"] = "eager"
option=ChromeOptions()
# option.set_headless()
option.add_argument('--no-sandbox')
option.add_experimental_option('excludeSwitches',['enable-automation'])
browser=webdriver.Chrome(options=option,desired_capabilities=capa)
# browser.implicitly_wait(6)

headers={
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
        }
baseurl="https://search.macaulaylibrary.org/catalog?taxonCode="
def compare(str1, str2):
   return difflib.SequenceMatcher(None, str1, str2).quick_ratio()

def searchaudio(target):
    global picnumber
    tar=parse.quote(target)
    aaa=requests.get('https://ebird.org/ws2.0/ref/taxon/find?key=jfekjedvescr&q='+tar+'&locale=zh_CN',headers=headers)
    bbb=re.split('"',aaa.text)[7]
    # print(bbb)
    ccc=parse.quote(bbb)
    eee=re.split('"',aaa.text)[3]
    audiourl=baseurl+eee+"&mediaType=a&q="+ccc
    browser.get(audiourl)
    try:
        wait = WebDriverWait(browser, 10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"button#show_more")))
    except:pass
    pages=(int(picnumber))//30
    while(pages>0):
        try:
            pages=pages-1
            browser.find_element_by_css_selector('button#show_more').send_keys(Keys.ENTER)
            sleep(3)
        except:pass
    js="var q=document.documentElement.scrollTop=100000"
    browser.execute_script(js)
    sleep(2)
    audioitem=browser.find_elements_by_css_selector('a.ResultsGallery-link')
    # print(len(audioitem))
    i=1
    f=open(target+'\\'+target+'.txt','a')
    f.write('\n'+target+'\t'+'sourceaudio_url')
    f.close()
    for item in audioitem:
        try:
            audioinfo=item.get_attribute('href')
            oneaudiourl="https://test.cdn.download.ams.birds.cornell.edu/api/v1/asset/"+audioinfo.split('/')[-1]
            f=open(target+'\\'+target+'_'+str(i)+'.mp3','wb')
            r=requests.get(oneaudiourl,headers=headers)#,verify=False)
            
            r.raise_for_status()
            f.write(r.content)
            f.close()
            f=open(target+'\\'+target+'.txt','a')
            f.write('\n'+target+'_'+str(i)+'.mp3'+'\t'+'https://macaulaylibrary.org/asset/'+audioinfo.split('/')[-1])
            f.close()
            print(target+'  audio  '+str(i))
            i=i+1
            if i>int(picnumber):
                break
        except:pass

def searchvideo(target):
    global picnumber
    # global picnumber
    # print(eee)
    tar=parse.quote(target)
    aaa=requests.get('https://ebird.org/ws2.0/ref/taxon/find?key=jfekjedvescr&q='+tar+'&locale=zh_CN',headers=headers)
    bbb=re.split('"',aaa.text)[7]
    # print(bbb)
    ccc=parse.quote(bbb)
    eee=re.split('"',aaa.text)[3]
    videourl=baseurl+eee+"&mediaType=v&q="+ccc
    browser.get(videourl)
    try:
        wait = WebDriverWait(browser, 10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"button#show_more")))
    except:pass
    pages=(int(picnumber))//30
    while(pages>0):
        try:
            pages=pages-1
            browser.find_element_by_css_selector('button#show_more').send_keys(Keys.ENTER)
            sleep(3)
        except:pass
    js="var q=document.documentElement.scrollTop=100000"
    browser.execute_script(js)
    sleep(2)
    videoitem=browser.find_elements_by_css_selector('a.ResultsGallery-link')
    # print(len(videoitem))
    i=1
    f=open(target+'\\'+target+'.txt','a')
    f.write('\n'+target+'\t'+'sourcevidio_url')
    f.close()
    for item in videoitem:
        try:
            videoinfo=item.get_attribute('data-asset-id')
            onevideourl="https://test.cdn.download.ams.birds.cornell.edu/api/v1/asset/"+videoinfo+'/mp4'
            f=open(target+'\\'+target+'_'+str(i)+'.mp4','wb')
            r=requests.get(onevideourl,headers=headers,verify=False)
            r.raise_for_status()
            f.write(r.content)
            f.close()
            f=open(target+'\\'+target+'.txt','a')
            f.write('\n'+target+'_'+str(i)+'.mp4'+'\t'+'https://macaulaylibrary.org/asset/'+videoinfo)
            f.close()
            print(target+'  video  '+str(i))
            i=i+1
            if i>int(picnumber):
                break
        except:pass

class Watchdog:
    def __init__(self, timeout, userHandler=None):  # timeout in seconds
        self.timeout = timeout
        self.handler = userHandler if userHandler is not None else self.defaultHandler
        self.timer = Timer(self.timeout, self.handler)
        self.timer.start()

    def reset(self):
        self.timer.cancel()
        self.timer = Timer(self.timeout, self.handler)
        self.timer.start()

    def stop(self):
        self.timer.cancel()

    def defaultHandler(self):
        print('下载超时')
        browser.close()
# 进度条模块
def progressbar(url,path):
    if not os.path.exists(path):   # 看是否有该文件夹，没有则创建文件夹
         os.mkdir(path)
    start = time.time() #下载开始时间
    response = requests.get(url, stream=True,headers=headers)
    size = 0    #初始化已下载大小
    chunk_size = 1024  # 每次下载的数据大小
    content_size = int(response.headers['content-length'])  # 下载文件总大小
    try:
        if response.status_code == 200:   #判断是否响应成功
            print('Start download,[File size]:{size:.2f} MB'.format(size = content_size / chunk_size /1024))   #开始下载，显示下载文件大小
            with open(path,'wb') as file:   #显示进度条
                for data in response.iter_content(chunk_size = chunk_size):
                    file.write(data)
                    size +=len(data)
                    print('\r'+'[下载进度]:%s%.2f%%' % ('>'*int(size*50/ content_size), float(size / content_size * 100)) ,end=' ')
        end = time.time()   #下载结束时间
        print('Download completed!,times: %.2f秒' % (end - start))  #输出下载用时时间
    except:
        print('Error!')
def searchpic(target):
    global picnumber
    global ccc
    global eee
    tar=parse.quote(target)
    aaa=requests.get('https://ebird.org/ws2.0/ref/taxon/find?key=jfekjedvescr&q='+tar+'&locale=zh_CN',headers=headers)
    bbb=re.findall('"name":"(.*?)"}',aaa.text)
    if len(bbb)==0:
        print(target+'没有结果')
        return
    eee=re.findall('"code":"(.*?)","name"',aaa.text)
    aa=compare(bbb[0],target)
    num=0
    i=0
    while i < len(bbb)-1:
        if compare(bbb[i],target)>aa:
                aa=compare(bbb[i],target)
                num=i
        i=i+1
    
    bb=bbb[num]
    # print(bb)
    bbb=re.split('"',aaa.text)[7]
    # print(bbb)
    ccc=parse.quote(bb)
    ee=eee[num]
    # print(ee)
    picurl=baseurl+ee+"&mediaType=p&q="+ccc
    browser.get(picurl)
    try:
        a=browser.find_element_by_css_selector('div.SearchToolbar-sort')
        a.find_element_by_css_selector('a.RadioGroup-toggler').click()
        sleep(1)
        aaaa=browser.find_element_by_css_selector('span#RadioGroup-sort.RadioGroup-panel.RadioGroup-panel--alignRight')
        bbbb=aaaa.find_elements_by_css_selector('label')
        bbbb[1].click()
        sleep(1)
    except:
        pass
    try:
        wait = WebDriverWait(browser, 10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"button#show_more")))
    except:
        print(target+'搜索结果少于40')
        pass
    # XPATH, "//li[@id='SalesRank']")))  # 这里可选择多个selector
    pages=int(picnumber)//30
    while(pages>0):
        try:
            pages=pages-1
            browser.find_element_by_css_selector('button#show_more').send_keys(Keys.ENTER)
            sleep(2)
        except:
            print('么有更多了')
            pass
    js="var q=document.documentElement.scrollTop=100000"
    browser.execute_script(js)
    sleep(5)
    pictotal=''
    audtotal=''
    vidtotal=''
    
    temp=browser.find_element_by_css_selector('label[for="RadioGroup-photos"]')
    pictotal=temp.find_element_by_css_selector('span.RadioGroup-secondary').text
    temp=browser.find_element_by_css_selector('label[for="RadioGroup-audio"]')
    audtotal=temp.find_element_by_css_selector('span.RadioGroup-secondary').text
    temp=browser.find_element_by_css_selector('label[for="RadioGroup-videos"]')
    vidtotal=temp.find_element_by_css_selector('span.RadioGroup-secondary').text
    f=open('catalogue.txt','a')
    f.write('\n'+target+'    '+'picture:'+pictotal+'    '+'audio:'+audtotal+'    '+'video:'+vidtotal)
    f.close()
    f=open(target+'\\'+target+'.txt','a')
    f.write('\n'+target+'\t'+'sourcepic_url'+'\t'+picurl)
    f.close()
    picitem=browser.find_elements_by_css_selector('a.ResultsGallery-link')
    print(len(picitem))
    i=1
    for item in picitem:
        # try:
            # mywatchdog=Watchdog(15)
        asset=item.get_attribute('data-asset-id')
        picurl='https://cdn.download.ams.birds.cornell.edu/api/v1/asset/'+asset+'/1200'
        f=open(target+'\\'+target+'_'+str(i)+'.jpg','wb')
        try:
            r=urllib.request.urlopen(picurl).read()
            # r=requests.get(picurl,headers=headers)#,verify=False)

        # r.raise_for_status()
            f.write(r)
            f.close()
            f=open(target+'\\'+target+'.txt','a')
            f.write('\n'+target+'_'+str(i)+'.jpg'+'\t'+item.get_attribute('href'))
            f.close()
        except:
            print('error')
            continue
        print(target+'  picture  '+str(i))
        i=i+1
        if i>int(picnumber):
            break



if __name__ == "__main__":
    f = open("名录.txt",encoding='utf-8')
    line = f.readline()
    ls=[]
    errorls=[]
    while line:
        ls.append(line.replace('\n',''))
        line = f.readline()
    f.close()
    print('请选择下载 【1】图片  【2】音频  【3】视频    按回车确认')
    type=input()
    print('请输入一个物种要爬取数目，按回车确认')
    picnumber=input()
    eee=''
    ccc=''
    for item in ls:
        if not os.path.exists(item+'\\'):
            os.makedirs(item+'\\')
            if type=='2':
                try:
                    searchaudio(item)
                except:
                    print(item+'  下载出现问题,稍后重新下载')
                    errorls.append(item)
                    pass
            else:
                if type=='3':
                    try:
                        # browser=webdriver.Chrome(options=option,desired_capabilities=capa)
                        # browser.implicitly_wait(6)
                        searchvideo(item)
                    except:
                        print(item+'  下载出现问题,稍后重新下载')
                        errorls.append(item)
                        pass
                else:
                    # try:
                    searchpic(item)
                    # except:
                    #     print(item+'  下载出现问题,稍后重新下载')
                    #     errorls.append(item)
                    #     pass
        else:
            print(item+'此名称已经搜索过')
            pass
    for item in errorls:
        print('重试下载失败的文件。。。。。。')
        if type=='2':
            try:
                # browser=webdriver.Chrome(options=option,desired_capabilities=capa)
                # browser.implicitly_wait(6)
                searchaudio(item)
            except:pass
        else:
            if type=='3':
                try:
                    # browser=webdriver.Chrome(options=option,desired_capabilities=capa)
                    # browser.implicitly_wait(6)
                    searchvideo(item)
                except:pass
            else:
                try:
                    # browser=webdriver.Chrome(options=option,desired_capabilities=capa)
                    # browser.implicitly_wait(6)
                    searchpic(item)
                except:pass
    print('结束')

