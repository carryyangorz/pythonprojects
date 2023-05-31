import requests
import os
import time
import re
import json
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
# option.add_argument('--headless')
option.add_argument('--no-sandbox')
option.add_argument('log-level=3') #INFO = 0 WARNING = 1 LOG_ERROR = 2 LOG_FATAL = 3 default is 0
option.add_experimental_option('excludeSwitches',['enable-automation'])
# option.add_argument('--blink-settings=imagesEnabled=false')

# option.add_experimental_option("debuggerAddress", "127.0.0.1:9527")
import multiprocessing
from multiprocessing import Process,Lock
# import multiprocessing_win
headers={
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
        }

def download_species(name):
        if os.path.exists(name+'.xlsx'):
                print(name+' already exists, pass')
                return
        url='https://api.inaturalist.org/v1/taxa/autocomplete?q='+name.replace(' ','+')+'&per_page=10&locale=zh-CN&preferred_place_id='
        try:
                r=requests.get(url,headers=headers)
                id=re.findall('"id":(.*?),"default_photo',r.text)[0]
                realname=re.findall('name":"(.*?)","rank',r.text)[0]
                print(realname)
                url2='https://www.inaturalist.org/taxa/'+id+'-'+realname.replace(' ','-')
                print(url2)
                url3='https://www.inaturalist.org/taxon_names.json?per_page=200&taxon_id='+id
                r=requests.get(url3,headers=headers)
                ls=re.findall('"id":(.*?)place_taxon_names',r.text)
        except:
               print(name+' not found')
               return
        if len(ls)==0:
              print(name+' not found')
              return
        else:
                wb=Workbook()
                ws=wb.active
                ws.append(['搜索名','网址','学名','语言','名称'])
        wb.save(name+'.xlsx')
        lll=[]
        for item in ls:
                valid=re.findall('is_valid":(.*?),"lexicon',item)[0]
                if valid=="true":
                        thename=re.findall('name":"(.*?)","is_valid',item)[0]
                        try:
                                lang=re.findall('parameterized_lexicon":"(.*?)","',item)[0]
                        except:
                               lang="NULL"
                        ws.append([name,url2,realname,lang,thename])
                        print(name+' +1')
        wb.save(name+'.xlsx')
        wb.close()
        
if __name__ == "__main__":
    multiprocessing.freeze_support()

    f = open("inaturalist.txt",encoding='utf-8')
    line = f.readline()
    ls=[]
    # errorls=[]
    while line:
        ls.append(line.replace('\n',''))
        line = f.readline()
    f.close()
    
    for item in ls:
           download_species(item)
#     name='Epipremnum aureum'
#     download_species(name)
    os.system ("pause")