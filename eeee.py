import requests
import os
import time
import sys
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
import multiprocessing

capa = DesiredCapabilities.CHROME
capa["pageLoadStrategy"] = "eager"
option=ChromeOptions()
#option.add_argument('--headless')
prefs = {"profile.managed_default_content_settings.images": 2}  #设置无图模式
#option.add_experimental_option("prefs", prefs)  
option.add_argument('--no-sandbox')
option.add_argument('log-level=3') #INFO = 0 WARNING = 1 LOG_ERROR = 2 LOG_FATAL = 3 default is 0
option.add_experimental_option('excludeSwitches',['enable-automation'])
# browser=webdriver.Chrome(options=option,desired_capabilities=capa)
url='https://www.cyberdrop.me/a/1c8Eewgu'
headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'
}
browser=webdriver.Chrome(options=option,desired_capabilities=capa)
browser.implicitly_wait(6)
def get(url):
    ls=[]
    browser.get(url)
    a=browser.find_elements(By.CSS_SELECTOR,'div.image-container')
    for items in a:
        #print(items.text)
        b=items.find_element(By.CSS_SELECTOR,'a#file').get_attribute('href')
        ls.append(b)
    for items in ls:
        print(items)
        browser.get(items)
        sleep(5)
        browser.find_element(By.CSS_SELECTOR,'a#downloadBtn').click()
        sleep(5)
    
if __name__ == "__main__":
    get(url)
    sleep(999)
    