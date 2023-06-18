import requests
import os
import time
import re
from openpyxl import Workbook
from openpyxl import load_workbook
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
from pyquery import PyQuery as pq

capa = DesiredCapabilities.CHROME
capa["pageLoadStrategy"] = "eager"
option=ChromeOptions()
option.add_argument('--disable-gpu')
option.add_argument('--headless')
option.add_argument('--no-sandbox')
option.add_argument('log-level=3') #INFO = 0 WARNING = 1 LOG_ERROR = 2 LOG_FATAL = 3 default is 0
option.add_experimental_option('excludeSwitches',['enable-automation'])
option.add_experimental_option('excludeSwitches', ['enable-logging'])
# option.add_argument('--blink-settings=imagesEnabled=false')

# option.add_experimental_option("debuggerAddress", "127.0.0.1:9527")
import multiprocessing
from multiprocessing import Process,Lock
# import multiprocessing_win
headers={
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
        }

license_ls=['CC0_1_0','CC_BY_4.0','CC_BY-NC_4_0','UNSPECIFIED','UNSUPPORTED']
record_ls=['OBSERVATION','MACHINE_OBSERVATION','HUMAN_OBSERVATION',
           'MATERIAL_SAMPLE','MATERIAL_CITATION','PRESERVED_SPECIMEN','FOSSIL_SPECIMEN','LIVING_SPECIMEN','OCCURRENCE']
# def download_species(name,num,licenseindex,recordindex):


def download_one(data):
    id=data[0]
    name=data[1]
    
    url1='https://www.gbif.org/occurrence/'+id
    browser=webdriver.Chrome(options=option,desired_capabilities=capa)
    browser.get(url1)
    try:
        WebDriverWait(browser, 20, 0.5).until(EC.presence_of_element_located((By.CSS_SELECTOR,'a.imgContainer')))
    except:
        print(name+' error1 -1')
        browser.close()
        browser.quit()
        return
    try:
        a=browser.find_element(By.CSS_SELECTOR,'a.imgContainer')
        url2=a.get_attribute('href')
    except:
        print(name+' error2 -1')
        browser.close()
        browser.quit()
        return  
    # print(url2)
    a=re.findall('media/(.*)',url2)[0]
    if url2==None:
         print(name+' error3 -1')
         browser.close()
         browser.quit()
         return
    picname=name+'_'+a+'.jpg'
    datals1=[]
    datals2=[]
    # try:
    bbb=browser.find_element(By.CSS_SELECTOR,'figcaption.card__content')
    ccc=bbb.find_elements(By.CSS_SELECTOR,'dd')
    # for item in ccc:
    try:
        datals1.append(ccc[0].text)
        datals1.append(ccc[1].text)
    except:
        datals1.append('NULL')
        datals1.append('NULL')

    try:
        datals1.append(ccc[2].find_element(By.CSS_SELECTOR,'a').get_attribute('href'))
    except:
         datals1.append('NULL')
    try:
        datals1.append(ccc[3].find_element(By.CSS_SELECTOR,'a').get_attribute('href'))
    except:
         datals1.append('NULL')
    try:
        datals1.append(ccc[4].text)
        datals1.append(ccc[5].text)
    except:
        #  print(name+' error -1')
        #  return
        datals1.append('NULL')
        datals1.append('NULL')
    try:
        datals1.append(ccc[6].find_element(By.CSS_SELECTOR,'a').get_attribute('href'))
    except:
         datals1.append('NULL')
    try:
        datals1.append((ccc[7].text).replace('\n',' '))
    except:
         datals1.append('NULL')
    # print(datals1)
    ggg=browser.find_elements(By.CSS_SELECTOR,'section.term-block')
    ddd=ggg[-2].find_element(By.CSS_SELECTOR,'div.term-block__terms')          
    eee=ddd.find_elements(By.CSS_SELECTOR,'tr')
    data2dic={
        'Continent':' ',
        'Coordinate uncertainty in metres':' ',
        'Country or area':' ',
        'Country code':' ',
        'Decimal latitude':' ',
        'Decimal longitude':' ',
        'Geodetic datum':' ',
        'State province':' ',
        'Verbatim locality':' '
    }
    # print(len(eee))
    # for item in eee:
    for i in range(1,len(eee)):
    #      if i==0:
         
         fff=eee[i].find_elements(By.CSS_SELECTOR,'td')
         ind=fff[0].text
         data2dic[ind]=fff[1].text
        #  print(len(fff))
        #  datals2.append(fff[1].text)
    for item in data2dic.values():
         datals2.append(item)
    # print(datals2)
    picurl='https://api.gbif.org/v1/image/cache/occurrence/'+id+'/media/'+a
    # print(picurl)
    if os.path.exists(name+"//"+picname):
        print(name+"//"+picname+'  already exists')
        browser.close()
        browser.quit()
        return
    try:
        r=requests.get(picurl,headers=headers)
    except:
         print(name+' error4 -1')
         browser.close()
         browser.quit()
         return
    
    f=open(name+"//"+picname,'wb')
    f.write(r.content)
    f.close()
    f=open(name+'//'+name+'_'+a+'.txt','a',encoding='UTF-8')
    f.write(id+'\n'+url1+'\n'+a+'\n')
    for item in datals1:
         f.write(item+'\n')
    for item in datals2:
         f.write(item+'\n')
    f.close()
    print(name +'  +1')
    browser.close()
    browser.quit()
def download_one_v2(data):

    id=data[0]
    name=data[1]
    url='https://www.gbif.org/occurrence/'+id

    url1='https://www.gbif.org/api/template/occurrence/'+id+'?v=1686130320019'
    try:
        r=requests.get(url1,headers=headers)
    except:
         print(name+' -1')
         return
    doc=pq(r.text)
    a=re.findall('a href="(.*?)" class="imgContainer"',r.text)[0]
    a=re.findall('media/(.*)',a)[0]
    # print(a)
    picname=name+'_'+a+'.jpg'
    picurl='https://api.gbif.org/v1/image/cache/occurrence/'+id+'/media/'+a
    data1dic={
        'creator':' ',
        'publisher':' ',
        'license':' ',
        'references':' ',
        'created':' ',
        'rightsHolder':' ',
        'identifier':' ',
        'Suggested citation':' '
        }
    data2dic={
        'Continent':' ',
        'Coordinate uncertainty in metres':' ',
        'Country or area':' ',
        'Country code':' ',
        'Decimal latitude':' ',
        'Decimal longitude':' ',
        'Geodetic datum':' ',
        'State province':' ',
        'Verbatim locality':' '
        }
    datals1=[]
    datals2=[]
    b=doc('figcaption.card__content')
    it=b('div').items()
    for item in it:
        # print(item)
        if item('dt').text()=='creator':
            data1dic[item('dt').text()]=item('span').text()
            continue
        if item('dt').text()=='publisher':
            data1dic[item('dt').text()]=item('span').text()
            continue
        if item('dt').text()=='license':
            data1dic[item('dt').text()]=item('a').attr('href')
            continue
        if item('dt').text()=='references':
            data1dic[item('dt').text()]=item('a').attr('href')
            continue
        if item('dt').text()=='created':
            data1dic[item('dt').text()]=item('span').text()
            continue
        if item('dt').text()=='rightsHolder':
            data1dic[item('dt').text()]=item('span').text()
            continue
        if item('dt').text()=='identifier':
            data1dic[item('dt').text()]=item('a').attr('href')
            continue
        if item('dt').text()=='Suggested citation':
            Suggested=item.text()
            ls=Suggested.split('\n')
            ls.remove(ls[0])
            Suggested=''
            for item in ls:
                Suggested+=item;
            data1dic['Suggested citation']=Suggested
            continue

    # print(data1dic)
    b=doc('div.term-block__terms')
    t=b('tr').items()
    for item in t:
        c=item('td').items()
        for ee in c:
                # print(ee.text())
                if ee.text()=='Continent':
                        data2dic['Continent'] = (list(item('span').items()))[0].text()
                        continue
                if ee.text()=='Coordinate uncertainty in metres':
                        data2dic['Coordinate uncertainty in metres'] = (list(item('span').items()))[0].text()
                        continue
                if ee.text()=='Country or area':
                        data2dic['Country or area'] = (list(item('span').items()))[0].text()
                        continue
                if ee.text()=='Country code':
                        data2dic['Country code'] = (list(item('span').items()))[0].text()
                        continue
                if ee.text()=='Decimal latitude':
                        data2dic['Decimal latitude'] = (list(item('span').items()))[0].text()
                        continue
                if ee.text()=='Decimal longitude':
                        data2dic['Decimal longitude'] = (list(item('span').items()))[0].text()
                        continue
                if ee.text()=='Geodetic datum':
                        data2dic['Geodetic datum'] = (list(item('span').items()))[0].text()
                        continue
                if ee.text()=='State province':
                        data2dic['State province'] = (list(item('span').items()))[0].text()
                        continue
                if ee.text()=='Verbatim locality':
                        data2dic['Verbatim locality'] = (list(item('span').items()))[0].text()
                        continue
    # print(data2dic)
    if os.path.exists(name+"//"+picname):
        print(name+"//"+picname+'  already exists')
        return
    
    for item in data2dic.values():
         datals2.append(item)
    for item in data1dic.values():
         datals1.append(item)
    try:
        r=requests.get(picurl,headers=headers)
    except:
         print(name+' -1')

         return
    f=open(name+"//"+picname,'wb')
    f.write(r.content)
    f.close()
    f=open(name+'//'+name+'_'+a+'.txt','a',encoding='UTF-8')
    f.write(id+'\n'+url+'\n'+a+'\n')
    for item in datals1:
         f.write(item+'\n')
    for item in datals2:
         f.write(item+'\n')
    f.close()
    print(name +'  +1')

if __name__ == "__main__":
    multiprocessing.freeze_support()
    print('请选择授权许可，  0.CC0 1.0   1.CC BY 4.0   2.CC BY-NC 4.0   3.未指定   4.不支持')
    licenseindex=int(input())
    print('''请选择记录许可    0.观察   1.机器观察   2.人类观察   3.材料样本
             4.材料的引用   5.馆藏标本   6.化石标本   7.活体标本   8.出现记录''')
    recordindex=int(input())
    print('请输入每个品种下载个数：')
    num=int(input())
#     num=40
    f = open("gbif.txt",encoding='utf-8')
    line = f.readline()
    ls=[]
    while line:
        ls.append(line.replace('\n',''))
        line = f.readline()
    f.close()
    loopflag=True
    for name in ls:
            try:
                if loopflag==False:
                     loopflag=True
                     continue
                # download_species(item,num,licenseindex,recordindex)
                if not os.path.exists(name+'//'):
                    os.makedirs(name+'//')
                else:
                    print(name+' already exists,pass')
                    loopflag=False
                    continue
                licen=license_ls[licenseindex]
                record=record_ls[recordindex]
                nameurl='https://api.gbif.org/v1/species/suggest?datasetKey=d7dddbf4-2cf0-4f39-9b2a-bb099caae36c&limit=10&q='+name
                try:
                    r=requests.get(nameurl,headers=headers)
                except:
                    print(name+' not found')
                    loopflag=False
                    continue
                try:
                    taxon_key=re.findall('"key":(.*?),"nameKey',r.text)[0]
                except:
                    print(name +' not found')
                page=0
                totalnum=0
                while (page-1)*100<num:
                    flag=True
                    searchurl='https://www.gbif.org/api/occurrence/search?advanced=false&basis_of_record='+record+'&license='+licen+'&limit=100&locale=zh&mediaType=stillImage&offset='+str(100*page)+'&taxon_key='+taxon_key
                    # print(searchurl)
                    if totalnum>=num:
                        # print(name+' over1')
                        loopflag=False
                        break
                    r=requests.get(searchurl,headers=headers)
                    # print(r.text)
                    picid=re.findall('"key":(.*?),"datasetKey',r.text)
                    if len(picid)==0:
                        print(name+'page '+str(page*100)+' not found')
                        break
                    page=page+1
                    i=0
                    print(name+' page '+str(page)+' num '+str(len(picid)))
                    while flag:
                        
                        for j in range(20):
                                ppls=[]
                                if i>=len(picid):
                                    flag=False
                                    # print('sssssssssssssssss')
                                    break
                                if totalnum>=num:
                                    loopflag=False
                                    print(name+'  over')
                                    flag=False
                                    break
                                # sleep(1)
                                data=[picid[i],name]
                                # l=multiprocessing.Lock()
                                pp=Process(target=download_one_v2,args=(data,))
                                i=i+1
                                totalnum += 1
                                pp.start()
                                ppls.append(pp)
                        for item in ppls:
                                item.join()
                sleep(1)
            except:
                print(item+' over3')
