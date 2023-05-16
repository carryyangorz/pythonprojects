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
browser=webdriver.Chrome(options=option,desired_capabilities=capa)
browser.implicitly_wait(6)
name='Abutilon theophrasti Medik.'
url='https://identify.plantnet.org/weeds/species/Abutilon%20theophrasti%20Medik./data'
browser.get(url)
num=200
itemnum=0
# try:
#     wait = WebDriverWait(browser, 2)
#     wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div.card-body")))
# except:pass
for i in range(10000):
    js="var q=document.documentElement.scrollTop=100000"
    browser.execute_script(js)
    sleep(2)
    a=browser.find_elements(By.CSS_SELECTOR,"img.img-fluid")
    if itemnum==len(a):
        print('not increasing')
        break
    itemnum=len(a)
    print(str(len))
    if itemnum>num:
        break


for i in range(min(itemnum,num)):
    print(a[i].get_attribute('src'))
    picurl=a[i].get_attribute('src')
    picurl=picurl.replace('/s/','/o/')
    picid=re.findall('/o/(.*)',picurl)
    print(picurl)
    print(picid)


