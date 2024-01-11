from matplotlib import pyplot
import os
# print(a)

def printone(name):
    f=open(name)
    line = f.readline()
    ls=[]
    # errorls=[]
    while line:
        ls.append(line.replace('\n',''))
        line = f.readline()
    f.close()
    lenth=len(ls)-1
    print(len(ls))
    ls.remove(ls[0])
    a=int(lenth/3)
    b=int(lenth*2/3)
    data1=ls[0:int(a-1)]
    data2=ls[a:int(b-1)]
    data3=ls[b:int(lenth-1)]
    # data1=ls[0:99]
    # data2=ls[100:199]
    # data3=ls[200:299]
    x=[]
    for i in range(0,a-1):
        x.append(i)
    pyplot.plot(x,data1,'c*-',x,data2, 'bo-',x,data3,'m.-.',)
    pyplot.title(name.replace('.dat',''))
    pyplot.show()

if __name__ == "__main__":
    for item in os.listdir():
        if ".dat" in item:
            printone(item)