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
option.add_argument('--headless')
option.add_argument('--no-sandbox')
option.add_argument('log-level=3') #INFO = 0 WARNING = 1 LOG_ERROR = 2 LOG_FATAL = 3 default is 0
option.add_experimental_option('excludeSwitches',['enable-automation'])
browser=webdriver.Chrome(options=option,desired_capabilities=capa)
browser.implicitly_wait(6)
import multiprocessing
from multiprocessing import Process,Lock
# import multiprocessing_win
headers={
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
        }
baseurl='https://api.plantnet.org/v1/projects/'
countrycodels=['the-plant-list','useful','weeds','invasion','prota','prosea',
       'weurope','canada','namerica','central-america','antilles','colombia','guyane','brazil','lapaz','martinique',
               'afn','aft','reunion','maurice','comores','medor','malaysia','japan',
           'nepal','endemia','hawai','polynesiefr']
countryls=['WorldFlora','UsefulPlants','Weeds','InvasivePlants','UsefulPlantsTropicalAfrica','UsefulPlantsAsia',
       'WesternEurope','Canada','USA','CentralAmerica','Caribbean','Colombia','Amazonia','Brazil','TropicalAndes','Martinique',
           'NorthAfrica','TropicalAfrica','Reunion','Mauritius','ComoroIslands','EasternMediterranean','Malaysia','Japan',
           'Nepal','NewCaledonia','Hawaii','FrenchPolynesia']
def get(i):
        if not os.path.exists(countryls[i]+'.xls'):
                wb=Workbook()
                ws=wb.active
                ws.append(['Species','common name','photo','observation','Family'])
                wb.save(countryls[i]+'.xlsx')
                # f=open(countryls[i]+'.xls','a',encoding='utf-8')
                # f.write('Species'+'\t')
                # f.write('common name'+'\t')
                # f.write('photo'+'\t')
                # f.write('observation'+'\t')
                # f.write('Family'+'\n')
                # f.close()
        else:
                print('please remove '+countryls[i]+'.xls'+' and then try again')
                return;
        for page in range(100):
                url2=baseurl+countrycodels[i] + '/species?pageSize=400&page='+str(page)+'&lang=en&sortBy=images_count&sortOrder=desc&illustratedOnly=true'
                browser.get(url2)
                a=browser.find_element(By.CSS_SELECTOR,'pre').text
                b=re.findall('name(.*?)searchTerms"',a)
                print('---------------------------')
                print(countryls[i]+'  page NO.' + str(page)+' lenth:'+str(len(b)))
                if (len(b)==0):
                        print(countryls[i]+'    over')
                        return

                for item in b:
                        name=re.findall('":"(.*?)","auth',item)
                        auth=re.findall('author":"(.*?)"',item)
                        commonname=re.findall('commonNames":\["(.*?)"',item)
                        photo=re.findall('imagesCount":(.*?),"',item)
                        observation=re.findall('observationsCount":(.*?),"',item)
                        family=re.findall('family":"(.*?)"',item)
                        
                        if len(name)==0:
                               name='NULL'
                        else:
                               name=name[0]
                        
                        if len(auth) == 0:
                               auth='NULL'
                        else:
                               auth=auth[0]

                        if len(commonname)==0:
                               commonname='NULL'
                        else:
                               commonname=commonname[0]
                        
                        if len(photo)==0:
                               photo='NULL'
                        else:
                               photo=photo[0]
                        
                        if len(observation)==0:
                               observation='NULL'
                        else:
                               observation=observation[0]
                        
                        if len(family)==0:
                               family='NULL'
                        else:
                               family=family[0]
                        wb=load_workbook(countryls[i]+'.xlsx')
                        ws=wb.active
                        ws.append([name+' '+auth,commonname,photo,observation,family])
                        wb.save(countryls[i]+'.xlsx')
                print('---------------------------')

if __name__ == "__main__":
    print('请输入要下载的序号，如0，1，2,输入999下载全部')
    i=0
    for item in countryls:
           print(str(i)+'.'+item+'\t')
           i=i+1
    choice=input()
    if(choice=='999'):
           
        for i in range(len(countrycodels)):
                get(i)
    else:
           get(int(choice))
                