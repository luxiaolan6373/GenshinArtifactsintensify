
import os
import sys
import ctypes
from ctypes import *
import cv2
import base64
import json
import numpy as np
from PIL import Image

class LanRenOcr:
    def __init__(self):

        old=os.getcwd()
        CUR_PATH = os.getcwd() + "\\lanrenocr"
        os.environ['PATH']=CUR_PATH
        # 添加dll的搜索路径为当前目录
        os.chdir(CUR_PATH)
        dllPath = os.path.join(CUR_PATH, "My_PaddleOCR.dll")
        self.pDll = ctypes.WinDLL(dllPath)
        self.pDll.ocr_Start()
        #恢复目录

        os.chdir(old)
    def get_datas(self, images):
        '''
        支持np图片数据或者图片路径
        :param images:
        :return:
        '''
        image = cv2.imencode('.jpg', images)[1]
        image_code = str(base64.b64encode(image))[2:-1]
        #给c++dll 传char* 类型要转成字节集
        data=bytes(image_code,'utf-8')
        #64位dll 必须把返回的地址类型改成uint64位,不然返回的地址不正确
        self.pDll.ocr_img.restype = c_uint64
        #字符串需要取值 dll返回的是地址  int参数要用c_int转
        js=json.loads(string_at(self.pDll.ocr_img(data, c_int(2), c_int(2))).decode('gbk'))
        datas = []
        try:
            data = js['PaddleOCR']
            for i, infomation in enumerate(data):
                datas.append(infomation)
        except Exception as err:
            print("lanren识字发生错误", err)
        return datas




if __name__ == '__main__':


    lr=LanRenOcr()
    image = Image.open('1232.jpg')
    image = np.copy(image)

    print(lr.recognize_text(image))


