from pyzbar import pyzbar
import cv2
import numpy as np
import os
import re
def image_detect(img):
    QRdetecter = cv2.QRCodeDetector()
    barcodes = pyzbar.decode(img)
    # print(barcodes)
    for barcode in barcodes:# 循环读取检测到的条形码
        # 绘条形码、二维码多边形轮廓
        points =[]
        for point in barcode.polygon:
            points.append([point[0], point[1]])
        points = np.array(points,dtype=np.int32).reshape(-1,1, 2)
        cv2.polylines(img, [points], isClosed=True, color=(0,0,255),thickness=2)

        # 条形码数据为字节对象，所以如果我们想把它画出来
        # 需要先把它转换成字符串
        barcodeData = barcode.data.decode("UTF-8") #先解码成字符串
        barcodeType = barcode.type
        # 绘出图像上的条形码数据和类型
        text = "({}): {} ".format(barcodeType, barcodeData )
        print(text)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return text
        #cv2.putText(img, text, (x, y - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    # cv2.imshow("QR", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
if __name__ == "__main__":
    # a=os.walk(os.getcwd())
    # for filepath,dirnames,filenames in os.walk(r'C:\Users\18800\Desktop\PROJECT-AT32415\Code\function\inc'):
    #     for filename in filenames:
    #         if ".h" in filename:
    #             print('#include "'+filename+'"')
    a=os.listdir()
    for item in a:
        # print(item)

        if (".jpg" in item) or ('.JPG' in item) :
            print(item)
            img0 = cv2.imread(item)
            id=image_detect(img0)

            if id:
                # if "CODE128" or "CODABAR" in id:
                    # print(id)
                id=re.findall(': (.*)',id)[0]
                id=id.replace(' ','')
                name=re.findall('(.*)\.',item)[0]
                # print(name)
                try:
                    os.rename(item,id+'_'+name+'.jpg')
                    print(item+'   >>>   '+id+'_'+name+'.jpg')
                except:
                    print(id+".jpg exists, pass")
            else:
                print(item+' no result')
    os.system("pause")