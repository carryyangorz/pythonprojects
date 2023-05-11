from PIL import Image
from time import sleep
import os
import pyzbar.pyzbar as pyzbar
import os
import threadpool
def decode(folder,imagename):
    try:
        imga=Image.open(folder+'\\'+imagename)
        imgb=imga.convert('L')
        value=120
        table=[]
        for i in range(256):
            if i < value:
                table.append(0)
            else:
                table.append(1)
        img=imgb.point(table,'1')
        codes=pyzbar.decode(img)
        del img
        del imga
        del imgb
        code=codes[0].data.decode('utf-8')
# return code
        print('+1')
        os.rename(folder+'\\'+imagename,folder+'\\'+code+'.jpg')
    except:
        print(imagename+'       fail')
        f=open('errorlog.txt','a')
        f.write('\n'+folder+'\\'+imagename+'    fail')
        f.close()

def fun1():
    path=os.getcwd()
    ls2=[]
    ls1=[]
    ls=[]
    for i in os.walk(path):
        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list
        # 遍历文件
        for f in i[2]:
            if '.JPG' in f:
                # decode(filename)
                ls1.append(i[0])
                ls2.append(f)
            if '.jpg' in f:
                ls1.append(i[0])
                ls2.append(f)
    # threadls=[]
    # for item in ls:
    for i in range(0,len(ls1)):
        bb=[]
        bb.append(ls1[i])
        bb.append(ls2[i])
        cc=(bb,None)
        ls.append(cc)
    pool=threadpool.ThreadPool(8)
    # threadls.append(threadpool.makeRequests(decode,[((item,),{})]))
    req=threadpool.makeRequests(decode,ls)
    [pool.putRequest(req) for req in req] 
    pool.wait() 
def fun2():
    pass

if __name__ == "__main__":
    # print('请输入需要执行的操作，按回车确认。'+'\n'+'【1】图片条码识别和重命名      【2】图片提取')
    # aa=input()
    # if aa=='2':
        # fun2()
    # else:
    fun1()
    os.system('pause')
        