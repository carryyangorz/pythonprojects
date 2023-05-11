import requests
import random
import re
from pyquery import PyQuery as pq 
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from time import sleep
from selenium.webdriver.common.keys import Keys
import os


headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'
}

def choose():
    baseurl='http://www.cfh.ac.cn/album/UserList.aspx'
    r=requests.get(baseurl,headers=headers)
    doc=pq(r.content)
    ls=[]
    pagenum=doc('a.userlist_a').items()
    for item in pagenum:
        ls.append(item.text())
    print('相册一共'+ls[-1]+'页 '+'请输入要爬取的页码，按回车结束：')
    page=input()
    url=baseurl+'?page='+page
    r=requests.get(url,headers=headers)
    doc=pq(r.content)
    userlslist=[]
    userls=doc('tr')('a').items()
    for item in userls:
        print(item.text())
        userlslist.append(item)
        # print(item.attr('href'))
    print('请输入要爬取的用户编号，按回车结束：')
    user=input()
    # numbeer=int(user[-2]+user[-1])
    try:
        userurl='http://www.cfh.ac.cn'+userlslist[int(user[-2]+user[-1])-1].attr('href')
    except:
        userurl='http://www.cfh.ac.cn'+userlslist[int(user[-1])-1].attr('href')
    print(userurl)
    option=ChromeOptions()
    option.set_headless()
    option.add_argument('--no-sandbox')
    option.add_experimental_option('excludeSwitches',['enable-automation'])
    browser=webdriver.Chrome(options=option)
    browser.implicitly_wait(6)
    browser.get(userurl)
    temp=browser.find_element_by_css_selector('span#ctl00_ContentPlaceHolder_body_labPageMsg').text
    # print(temp)
    temp=re.sub(r'.*(个相册，当前是第)[0-9](/)','',temp)
    albumnumber=int(re.sub(r'页','',temp))

    
    while albumnumber>0:
        # print(albumnumber)
        albumnumbernum=0
        albumurllist=[]
        tempalbumls=browser.find_elements_by_css_selector('div.albumItem')
        for item in tempalbumls:
            albumls=item.find_element_by_css_selector('div.photoName2')
            albumurl=albumls.find_element_by_css_selector('a')#.get_attribute('href')
            print(str(albumnumbernum)+'.'+albumurl.text)
            albumnumbernum=albumnumbernum+1
            albumurllist.append(albumurl.get_attribute('href'))
        print(temp)
        print('第'+str(albumnumber)+'相册页,请输入要爬取的相册编号,按回车确认,按00获取此页全部相册,输入000进入下一页')
        nnn=input()
        if nnn=='00':
            for item in albumurllist:
                getonealbum(item)
                sleep(random.randint(1,2))
        else:
            if nnn=='000':
                browser.find_element_by_css_selector('input#ctl00_ContentPlaceHolder_body_ImgBtnNext').send_keys(Keys.ENTER)

                albumnumber=albumnumber-1
                continue
            else:
                getonealbum(albumurllist[int(nnn)])
        print('是否进入下一页相册列表，请输入 1或0:')
        myflag=input()
        if myflag=='1':
            browser.find_element_by_css_selector('input#ctl00_ContentPlaceHolder_body_ImgBtnNext').send_keys(Keys.ENTER)
            # print('下一页')
            # sleep(random.randint(1,3))
            albumnumber=albumnumber-1
    print('结束')
    browser.quit()

def getonealbum(url):
    num=0
    currentpath=os.getcwd()
    option=ChromeOptions()
    option.set_headless()
    option.add_argument('--no-sandbox')
    option.add_experimental_option('excludeSwitches',['enable-automation'])
    browser=webdriver.Chrome(options=option)
    browser.implicitly_wait(6)
    browser.get(url)
    try:
        temp=browser.find_element_by_css_selector('span#ctl00_ContentPlaceHolder_body_labPageMsg').text
        print(temp)
        temp=re.sub(r'.*(张照片，当前是第)[0-9](/)','',temp)
        pagenumber=int(re.sub(r'页','',temp))
    except:
        print('此相册已锁定，不能爬取')
        # albumnumber=0
        choose()
    # print(pagenumber)
    title=browser.find_element_by_css_selector('span#AlbumInfoTitle').text
    author=browser.find_element_by_css_selector('span#A_Author').text
    print(title)
    newtitle=re.sub('/','',title)
    # tempnumber=str(random.randint(1,100))
    if not os.path.exists(currentpath+'\\'+author+'\\'+newtitle+'\\'):
        try:
            os.makedirs(currentpath+'\\'+author+'\\'+newtitle+'\\')
        except:
            newtitle="特殊标题"+str(random.randint(200,999))+str(random.randint(200,999))
            os.makedirs(currentpath+'\\'+author+'\\'+newtitle+'\\')

    else:
        print('相册已经存在')
        return
    # aaa=browser.find_element_by_css_selector('tbody')
    # picls=browser.find_elements_by_css_selector('div.photoItem')
    # print(len(picls))
    # times=1
    failpicls=[]
    picnumber=0
    while pagenumber>0:
        print(pagenumber)
        picls=browser.find_elements_by_css_selector('div.photoItem')
        if len(picls) ==0:
            picls=browser.find_elements_by_css_selector('div.protectedPhotoItem')
        for item in picls:
            # sleep(random.randint(1,2))
            try:
                pictitle=item.find_element_by_css_selector('div.photoLName').text+'_'+item.find_element_by_css_selector('div.photoCName').text+'_'+str(num)
            except:
                pictitle="请根据链接手动查询名称"+str(num)
            # print(currentpath+'author/'+'title/'+pictitle)
            if os.path.exists(currentpath+'\\'+author+'\\'+newtitle+'\\'+pictitle+'.jpg'):
            #if os.path.exists(currentpath+'/'+author+'/'+newtitle):
                print('图片已经存在')
                picnumber=picnumber+1
                # continue
            else:
                try:

                    print('保存图片......'+str(picnumber))
                    picnumber=picnumber+1
                    try:
                        f=open(currentpath+'\\'+author+'\\'+newtitle+'\\'+pictitle+'.jpg','wb')
                    except:
                        print('随机生成文件名')
                        pictitle=str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+'_'+str(num)
                        f=open(currentpath+'\\'+author+'\\'+newtitle+'\\'+pictitle+'.jpg','wb')
                    detailurl=item.find_element_by_css_selector('a').get_attribute('href')
                    picurl=item.find_element_by_css_selector('img').get_attribute('src')
                    picurl=picurl.replace('Thumbnail','Normal')
                    # print(picurl)
                    r=requests.get(picurl,headers=headers,timeout=7)
                    f.write(r.content)
                    f.close()
                    f=open(currentpath+'\\'+author+'\\'+newtitle+'\\'+'url.txt','a')
                    f.write('\n'+pictitle+'\t'+detailurl)
                    f.close()
                except:
                    print('保存图片失败')
                    failpicls.append(picurl)
                    picnumber=picnumber+1
                    # pass
            num=num+1
        browser.find_element_by_css_selector('input#ctl00_ContentPlaceHolder_body_ImgBtnNext').send_keys(Keys.ENTER)
        # sleep(random.randint(1,3))
        print('下一页')
        pagenumber=pagenumber-1
    if failpicls is not None:
        print('重试保存之前保存失败的图片：')
        for item in failpicls:
            try:
                f=open(currentpath+'\\'+author+'\\'+newtitle+'\\'+pictitle+'.jpg','wb')
                r=requests.get(item,headers=headers)
                f.write(r.content)
                f.close()
                print('保存成功')
            except:
                pass

    # browser.quit()


if __name__ == "__main__":
    choose()
    # getonealbum('http://www.cfh.ac.cn/Album/ShowAlbum.aspx?albumid=e67b2030-1656-4a68-aa66-fc81dd381184&Username=alsages')
    



