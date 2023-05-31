import os
from time import sleep
import re
from openpyxl import Workbook
from openpyxl import load_workbook

def workbook_save(name):
    if not os.path.exists(name+'\\'):
        print('return1')
        return
    if os.path.exists(name+'\\'+name+'.xlsx'):
        print('return2')
        return
    wb=Workbook()
    ws=wb.active
    ws.append(['图片名','网址1','网址2','Creator','Publisher','Record licence','References','Created','Rights holder',
               'Identifier','Suggested attribution','Continent','Coordinate uncertainty in metres',
               'Country or area','Country code','Decimal latitude','Decimal longitude','Geodetic datum',
               'State province','Verbatim locality'
])
    if not os.listdir(name+'\\'):  # 如果子文件为空
        os.rmdir(name+'\\')  # 删除这个空文件夹
        print('return3')
        return
    for item in os.listdir(name+'\\'):
        if '.txt' in item:
            print(item)
            f=open(name+'\\'+item,'r',encoding='UTF-8')
            line = f.readline()
            ls=[]        
            while line:
                ls.append(line.replace('\n',''))
                line = f.readline()
            f.close()
            # try:
            tmp=ls[0]
            ls[0]=name+'_'+ls[2]+'.jpg'
            ls[2]='https://api.gbif.org/v1/image/cache/occurrence/'+tmp+'/media/'+ls[2]
            
            ws.append(ls)
            # except:pass
            print(item+' deleted')
            os.remove(name+'\\'+item)
    sleep(1)
    wb.save(name+'//'+name+'.xlsx')
    wb.close()
if __name__== "__main__":
    os.system('taskkill /im chromedriver.exe /F')
    os.system('taskkill /im chrome.exe /F')
    f = open("gbif.txt",encoding='utf-8')
    line = f.readline()
    ls=[]
    while line:
        ls.append(line.replace('\n',''))
        line = f.readline()
    f.close()
    for item in ls:
    # item='Prunus spinosa'
        print(item)
        workbook_save(item)
    os.system('pause')