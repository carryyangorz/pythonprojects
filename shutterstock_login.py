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
path=os.getcwd()
prefs = {"download.default_directory":path}
# option.add_argument('--headless')
option.add_argument('--no-sandbox')
option.add_experimental_option("prefs", prefs)
option.add_argument('log-level=3') #INFO = 0 WARNING = 1 LOG_ERROR = 2 LOG_FATAL = 3 default is 0
option.add_experimental_option('excludeSwitches',['enable-automation'])
browser=webdriver.Chrome(options=option,desired_capabilities=capa)
browser.implicitly_wait(6)

baseurl='https://www.shutterstock.com/zh/home'
url='https://accounts.shutterstock.com/login?next=%2Foauth%2Fauthorize%3Fstate%3D0bc7523e6812ef8fc7578e28d923d0fd%26redirect_uri%3Dhttps%253A%252F%252Fwww.shutterstock.com%252Fsstk-oauth%252Fcallback%253Flanding_page%253Dhttp%25253A%25252F%25252Fwww.shutterstock.com%25252Fzh%25252Fhome%2526realm%253Dcustomer%26scope%3Dlicenses.create%2520licenses.view%2520organization.view%2520purchases.view%2520purchases.create%2520user.edit%2520user.email%2520user.view%2520user.address%2520organization.address%2520collections.view%2520collections.edit%2520media.upload%2520media.submit%2520media.edit%26hl%3Den%26client_id%3D4dee2-8f775-dd4c6-4e561-6e645-1aa0f'

def login():
    # username='coo@isee.sh.cn'

    # passwd='iSee2020'
    f=open('account.txt')
    index=f.readlines()
    f.close()
    username=index[0].replace('\n','')
    passwd=index[1].replace('\n','')
    # browser=webdriver.Chrome(options=option,desired_capabilities=capa)
    browser.get(url)
    # browser.find_element_by_css_selector('button[data-track-label="logIn"]').click()
    # browser.find_element_by_css_selector('input["email"]').send_keys(username)
    browser.find_element_by_css_selector('input#login-username').send_keys(username)
    sleep(1)
    # browser.find_element_by_css_selector('input[name="password"]').send_keys(passwd)
    browser.find_element_by_css_selector('input#login-password').send_keys(passwd)
    sleep(1)
    browser.find_element_by_css_selector('button#login').send_keys(Keys.ENTER)
    # browser.find_element_by_css_selector('button.oc_v_453f4.b_h_9156a.b_h_f4d86.b_h_1a7bb.b_h_97f8c.b_h_ce5e9.b_h_31b1c.b_h_276d2.oc_v_5910e.b_h_51685.oc_v_f5103.b_h_77160').send_keys(Keys.ENTER)
    # aa=browser.find_element_by_css_selector('div.oc_R_3d11b.b_u_28b8f.e_a_cb40d')
    # bb=aa.find_element_by_css_selector('div.e_j_d3f02')
    # print(bb.text)
    sleep(5)
    # browser.execute_script("arguments[0].removeAttribute('type')",bb)
    # bb.send_keys(Keys.ENTER)

def search():
    f=open('id.txt','r')
    index=f.readlines()
    f.close()
    for item in index:
        item=item.replace('\n','')
        print(item)
        try:
            browser.get('https://www.shutterstock.com/zh/search/'+item)
            sleep(3)
            browser.find_element_by_css_selector('button.Q_a_00c08.oc_v_453f4.b_h_9156a.b_h_f4d86.b_h_1a7bb.b_h_97f8c.b_h_ce5e9.b_h_31b1c.b_h_276d2.oc_v_5910e.b_h_51685.oc_v_f5103.b_h_77160').send_keys(Keys.ENTER)
            sleep(3)
            # browser.find_element_by_css_selector('button.Q_r_a6346.oc_v_453f4.b_h_9156a.b_h_f4d86.b_h_1a7bb.b_h_97f8c.b_h_ce5e9.b_h_31b1c.b_h_376d2.oc_v_5910e.b_h_51685.oc_v_f5103.b_h_77160').send_keys(Keys.ENTER)
            # sleep(1)
            browser.find_element_by_css_selector('button.Q_q_a6346.oc_v_453f4.b_h_9156a.b_h_f4d86.b_h_1a7bb.b_h_97f8c.b_h_ce5e9.b_h_31b1c.b_h_276d2.oc_v_5910e.b_h_51685.oc_v_f5103.b_h_77160').send_keys(Keys.ENTER)
            # print(bb)
            sleep(7)
        except:
            print(item+'    error')
            pass
       
    

if __name__ == "__main__":
    
    login()
    search()
    sleep(100)
    
