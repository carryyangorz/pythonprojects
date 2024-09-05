import requests
import os
import time
import json
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
capa['pageLoadStrategy'] = 'eager'
option = ChromeOptions()
option.add_argument('--no-sandbox')
# option.add_argument('--headless')
option.add_argument('log-level=3')
option.add_experimental_option('excludeSwitches', [
    'enable-automation'])
# browser=webdriver.Chrome(options=option,desired_capabilities=capa)
from threading import Timer
import multiprocessing
from multiprocessing import Process
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36' }

def get(name):
    if not os.path.exists(name + '\\'):
        os.mkdir(name + '\\')
    # else:
        # print(name + 'already exists')
        # return 
    tar = name.replace(' ', '+')
    url = 'https://api.inaturalist.org/v1/taxa/autocomplete?q=' + tar + '&per_page=10&locale=zh-CN&preferred_place_id='
    r = requests.get(url, headers=headers)
    try:
        id = re.findall('"id":([0-9]{0,10}),"', r.text)[0]
        # print('id: '+id)
    except:
        # pass
        print(name + ' no result, over')
        return
    ls = []
    pagenum=1
    finalurl = 'https://api.inaturalist.org/v1/observations/species_counts?verifiable=any&spam=false&taxon_id=' + id + '&locale=zh-CN&page=' + str(pagenum) + '&per_page=100'
    r=requests.get(finalurl,headers=headers)
    r=json.loads(r.text)
    totalcount=r['total_results']
    # print(type(totalcount))
    print(name+' '+str(totalcount) + ' 条结果')
    if totalcount == 0:
        print('no result')
        return
    r=0

    addedcount=0
    while True:
        # print(str(pagenum))
        # if pagenum*100>totalcount:
        #     break
        print('addedcount '+str(addedcount))
        if addedcount>=totalcount:
            print(name+' over')
            return
        finalurl = 'https://api.inaturalist.org/v1/observations/species_counts?verifiable=any&spam=false&taxon_id=' + id + '&locale=zh-CN&page=' + str(pagenum) + '&per_page=100'
        # print('1 '+finalurl)
        r=requests.get(finalurl,headers=headers)
        sleep(1)
        cnnamels=[]
        ennamels=[]
        licensels=[]
        countls=[]
        picurlls=[]
        a=json.loads(r.text)
        
        # print(len(a['results']))
        if len(a['results'])==0:
            return
        for item in a['results']:
            # print('...')
            try:
                cnname=item.get('taxon').get('preferred_common_name')
            except:
                cnname='null'
            try:
                enname=item.get('taxon').get('name')
            except:
                enname='null'
            try:
                count=item.get('count')
            except:
                count=0
            try:
                picurl=item.get('taxon').get('default_photo').get('url').replace('square','large')
            except:
                picurl='null'
            try:
                license=item.get('taxon').get('default_photo').get('license_code')
            except:
                license='null'
            # print(cnname)
            # print(enname)
            # print(count)
            # print(picurl)
            # print(license)
            if enname==None:
                enname='null'
            if cnname==None:
                cnname='null'
            
            if license == None:
                license = 'null'
            if count == None:
                count=0
            cnnamels.append(cnname)
            ennamels.append(enname)
            picurlls.append(picurl)
            countls.append(count)
            licensels.append(license)
        ppls=[]
        print('(1')
        flag=True
        i=0
        while flag:
            for k in range(8):
                if i>len(cnnamels)-1:
                    flag=False
                    continue
                # print(cnnamels[i])
                # print(ennamels[i])
                # print(countls[i])
                # print(picurlls[i])
                # print(licensels[i])
                picname=ennamels[i]+'_'+cnnamels[i]
                # print('+1  ps'+str(i)+'  '+str(len(cnnamels)))
                # print(picurlls[i])
                data=[picname,name,picurlls[i]]
                pp=Process(target=download,args=(data,))
                # i=i+1
                # if i>len(bb):
                #         break
                pp.start()
                ppls.append(pp)
                f = open(name + '\\' + name + '.txt', 'a', encoding='utf-8')
                f.write(picname + '\t' + str(countls[i])+'次观察' + '\t' + licensels[i] + '\t' + picname+'.jpg' + '\t' + picurlls[i] + '\n')
                f.close()
                i=i+1
                addedcount=addedcount+1
                print(name+'  '+str(addedcount))
            for thread in ppls:
                thread.join()
        pagenum+=1
    print(len(cnnamels)+'------------')
            # f = open(name + '\\' + picname+'.jpg', 'wb')
            # try:
            #     r = requests.get(picurl, headers=headers)
            #     r.raise_for_status
            #     f.write(r.content)
            #     f.close()
            # except:
            #     pass
            # f = open(name + '\\' + name + '.txt', 'a', encoding='utf-8')
            # f.write(picname + '\t' + str(count)+'次观察' + '\t' + license + '\t' + picname+'.jpg' + '\t' + picurl + '\n')
            # f.close()
            # print('==================================')
        


    return None
def download(data):
    name=data[1]
    picurl=data[2]
    picname=data[0]
    if os.path.exists(name+'\\'+picname+'.jpg'):
        return
    f=open(name+'\\'+picname+'.jpg','wb')
    try:
    #     if useproxy:
        r=requests.get(picurl,headers=headers)#,proxies=random.choice(proxy))#,verify=False)
        # else:
            # r=requests.get(picurl,headers=headers)
    except:
        print('error:'+picurl)

        # continue
        return
    # r.raise_for_status()
    f.write(r.content)
    # i=i+1
    print(name+' +1')
    f.close()


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
    f = open('inaturalist.txt', 'r', encoding='utf-8')
    names = f.readlines()
     
    f.close()
    while index<len(names):
        item = names[index]
        item = item.replace('\n', '')
        try:
            get(item)
        except:
            sleep(1)
            pass
        index = index + 1
        f = open('index.txt', 'w')
        f.write(str(index))
        f.close()
    os.system ("pause")