import requests
import os
import time
import re
import json

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
url='https://api.inaturalist.org/v1/observations?verifiable=any&order_by=observations.id&order=desc&page=1&spam=false&taxon_id=208350&locale=zh-CN&per_page=200'

# aaa='s"url":"https://static.inaturalist.org/photos/29220127/square.jpg?1544974714"},"english_common_na'
# aaa='ne","default_photo":{"square_url":"https://static.inaturalist.org/photos/24712881/square.jpg?1536688629","attribution":"(c) John Boback, alguns direitos reservados (CC BY-NC)","flags":[],"medium_url":"https://static.inaturalist.org/photos/24712881/medium.jpg?1536688629","id":24712881,"license_code":"cc-by-nc","original_dimensions":{"width":1536,"height":2048},"url":"https://static.inaturalist.org/photos/24712881/square.jpg?1536688629"},"preferred_common_name":"葛仙米藻","english_common_name":"Star Jelly"}}],"project_observations":[],"photos":[{"id":103797326,"license_code":"cc-by-nc","url":"https://static.inaturalist.org/photos/103797326/square.jpg?1604959657","attribution":"(c) adriannad16, some rights reserved (CC BY-NC)","original_dimensions":{"width":1536,"height":2048},"flags":[]}],"observation_photos":[{"id":96829105,"position":0,"uuid":"9186424e-2d1c-4e17-854e-0a79a65b6c40","photo":{"id":103797326,"license_code":"cc-by-nc","url":"https://static.inaturalist.org/photos/103797326/square.jpg?1604959657","attribution":"(c) adriannad16, some rights reserved (CC BY-NC)","original_dimensions":{"width":1536,"height":2048},"flags":[]}}],"faves":[],"non_owner_ids":[{"id":141805107,"uuid":"8932f18e-b0d0-4c9c-89b6-d5af2752ae7b","user":{"id":771325,"login":"roman_romanov","spam":false,"suspended"'
ls=[]
# for i in range (1,6):
#     url='https://api.inaturalist.org/v1/observations?verifiable=any&order_by=observations.id&order=desc&page='+str(i)+'&spam=false&taxon_id=151842&locale=zh-CN&per_page=24'
browser.get(url)
aaa=browser.find_element_by_css_selector('pre').text
total=re.findall('total_results":(.*),"page',aaa)[0]
print(total)
pages=int(total)//200+2
lss=[]
# print(pages+'rrrrrtotal')
for i in range(1,pages):
    print('number   ')
    ls=[]
    url='https://api.inaturalist.org/v1/observations?verifiable=any&order_by=observations.id&order=desc&page='+str(i)+'&spam=false&taxon_id=208350&locale=zh-CN&per_page=200'
    browser.get(url)
    aaa=browser.find_element_by_css_selector('pre').text
    b=re.findall('square_url":"(.*?)","attribution',aaa)
    # b=re.findall('medium_url":"(.*?)","id',aaa)
    print(len(b))
    for item in b:
        if "inaturalist" in item:
            ls.append(item)
    temp=list(set(ls))
    lss.extend(temp)
    i=i+1
lss=list(set(ls))
print(len(lss))


