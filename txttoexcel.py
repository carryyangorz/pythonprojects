import os
from openpyxl import Workbook
from openpyxl import load_workbook
wb=Workbook()
ws=wb.active
ws.append(['name','Filter by photos','Filter by photo','Filter by video'])
# wb.save(name+'//'+name+'_'+specie_type_ls[typeindex]+'.xlsx')
path=os.getcwd()
ls2=[]
ls1=[]
ls=[]
for f in os.listdir():
    # root 表示当前正在访问的文件夹路径
    # dirs 表示该文件夹下的子目录名list
    # files 表示该文件夹下的文件list
    # 遍历文件
    if '.txt' in f:
        ls=[]
        a=open(f,'r')
        ls.append(f.replace('.txt',''))
        line=a.readlines()
        for b in line:
            if "Filter" in b:
                continue
            ls.append(b)
        ws.append(ls)
wb.save('data.xlsx')
            