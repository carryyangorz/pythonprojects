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
def download_species(name,num,licenseindex,recordindex):
    if not os.path.exists(name+'//'):
       os.makedirs(name+'//')
    else:
          print(name+' already exists,pass')
          return    
    # if not os.path.exists(name+'//'+name+'.xlsx'):
        # wb=Workbook()
        # ws=wb.active
        # ws.append(['图片名','网址1','网址2'])
        # wb.save(name+'//'+name+'.xlsx')
        # wb.close()
    licen=license_ls[licenseindex]
    record=record_ls[recordindex]
    nameurl='https://api.gbif.org/v1/species/suggest?datasetKey=d7dddbf4-2cf0-4f39-9b2a-bb099caae36c&limit=10&q='+name
    try:
        r=requests.get(nameurl,headers=headers)
    except:
         print(name+' not found')
         return
    try:
        taxon_key=re.findall('"key":(.*?),"nameKey',r.text)[0]
    except:
         print(name +' not found')

    #############################################################
    page=0
    totalnum=0
    while (page-1)*100<num:
        flag=True
        searchurl='https://www.gbif.org/api/occurrence/search?advanced=false&basis_of_record='+record+'&license='+licen+'&limit=100&locale=zh&mediaType=stillImage&offset='+str(100*page)+'&taxon_key='+taxon_key
        # print(searchurl)
        if totalnum>=num:
             print(name+' over')
             return
        r=requests.get(searchurl,headers=headers)
        # print(r.text)
        picid=re.findall('"key":(.*?),"datasetKey',r.text)
        if len(picid)==0:
             print(name+'page '+str(page*100)+' not found')
             return

        page=page+1
        i=0
        print(name+' page '+str(page)+' num '+str(len(picid)))

        ################################################################################
        while flag:
            
            for j in range(20):
                    ppls=[]
                    if i>=len(picid):
                        flag=False
                        # print('sssssssssssssssss')
                        break
                    if totalnum>=num:
                         print(name+'  over')
                         return
                    sleep(1)
                    data=[picid[i],name]
                    # l=multiprocessing.Lock()
                    pp=Process(target=download_one,args=(data,))
                    i=i+1
                    totalnum += 1
                    pp.start()
                    ppls.append(pp)
            for item in ppls:
                    item.join()
        ####################################################################################
        # for item in picid:
        #     data=[item,name]
        #     download_one(data)
    sleep(1)

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
    datals1.append(ccc[0].text)
    datals1.append(ccc[1].text)
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
    for item in ls:
            try:
                download_species(item,num,licenseindex,recordindex)
            except:
                print(item+' over')
