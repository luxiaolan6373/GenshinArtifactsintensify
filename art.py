import time,json
#from PIL import Image
from hookkeymose import HookKeyMose
import pyautogui
import ctypes
import cv2
import numpy as np

from lanrenocr.lanrenocr import LanRenOcr
class Artifacts(LanRenOcr):
    def __init__(self):
        self.set_Art_info_pos()
        pyautogui.PAUSE = 0.01
        LanRenOcr.__init__(self)

        self.isshaoyige = False#少1个也算满足
        self.issancitiao = True#3词条 也算多满足一个
        self.isbumanzu= True #是否解锁
        self.Art_on=False
        self.art_list=[]
        self.on_lock_condition = ["暴击率", "暴击伤害"]#副词条
        self.on_lock_condition_main=["暴击率","暴击伤害"] #主词条

    def one_sim(self):
        '''
        "识别一次圣遗物,把信息全部打印出来,并且根据条件进行锁定"
        :return: 圣遗物信息
        '''

        img = pyautogui.screenshot(region=self.art_info_pos)
        img_arr = np.array(img)
        '''
        img_arr[self.art_else_pos[0]: self.art_else_pos[1], self.art_else_pos[2]: self.art_else_pos[3]] = (0, 0, 0)
        #img = Image.fromarray(img_arr)
        #img.show()
        '''
        img = cv2.cvtColor(img_arr, cv2.COLOR_RGB2BGR)
        data=self.get_datas(img)

        d = []
        cound_citiao=0
        for item in data:
            if item["ttxt"].find("+")!=-1:
                cound_citiao+=1
            if item["ttxt"].find("★")!=-1:
                if len(item["ttxt"])<5:
                    self.Art_on = False

                    return []
            d.append(item["ttxt"])
        print(cound_citiao,d)
        self.on_lock(d,cound_citiao)
        return d
    def on_lock(self,d:{},cound_citiao:int):
        ok_condition = 0
        zhucitiao=False
        #主词条条件
        #符合主词条其中一条的就算ok不符合的 也不需要看副词条了 但是要排除 一些部位
        try:
            if len(self.on_lock_condition_main)==0:#如果没有主词条的条件,就直接符合
                zhucitiao = True
            for cond in self.on_lock_condition_main:
                if d[1] in ["生之花", "死之羽"]:
                    zhucitiao = True
                    break
                if d[1] == "时之沙":#部位在2号位
                    # 如果条件中有这几个条件则进行判断,,如果没有则一律放行
                    if cond in ["攻击力", "元素精通", "元素充能", "生命值", "防御力"]:
                        if d[2].find(cond) != -1:#主词条在3号位
                            zhucitiao = True
                            break

                elif d[1] == "空之杯":  # 部位在2号位
                    print("空之杯",cond)
                    # 如果条件中有这几个条件则进行判断,,如果没有则一律放行
                    if cond in ["攻击力", "元素精通", "生命值", "防御力","火元素伤害","水元素伤害",
                                "冰元素伤害","雷元素伤害","草元素伤害","风元素伤害","岩元素伤害","物理伤害"]:
                        if d[2].find(cond) != -1:  # 主词条在3号位
                            zhucitiao = True
                            break
                elif d[1] == "理之冠":  # 部位在2号位
                    # 如果条件中有这几个条件则进行判断,,如果没有则一律放行
                    if cond in ["攻击力", "元素精通", "生命值", "防御力", "暴击率", "暴击伤害", "治疗"]:
                        if d[2].find(cond) != -1:  # 主词条在3号位
                            zhucitiao = True
                            break
                    else:
                        zhucitiao = True
                        break



            if zhucitiao==True:
                for cond in self.on_lock_condition:
                    for f in d:
                        if f.find(cond) != -1:
                            if f.find("件套")==-1:
                                if cond[-1]==("%"):
                                    if f[-1]==("%"):
                                        ok_condition += 1
                                        continue
                                else:
                                    if f[-1]!=("%"):
                                        ok_condition += 1
                                        continue


                                ok_condition += 1

                if self.isshaoyige == False:
                    if ok_condition>=len(self.on_lock_condition) or  (ok_condition>=len(self.on_lock_condition)-1 and cound_citiao==4 and self.issancitiao == True):
                        '2280,540,2388,640,宽高(109,101)'
                        if pyautogui.locateCenterOnScreen(self.imgKey, region=self.key_pos, confidence=self.confidence)==None:
                            pyautogui.moveTo(self.key_pos[0]+self.key_pos[2]//2, self.key_pos[1]+self.key_pos[3]//2)
                            pyautogui.mouseDown()
                            pyautogui.mouseUp()
                            time.sleep(0.2)
                    elif self.isbumanzu==True:#解锁
                        if pyautogui.locateCenterOnScreen(self.imgKey, region=self.key_pos, confidence=self.confidence)!=None:
                            pyautogui.moveTo(self.key_pos[0]+self.key_pos[2]//2, self.key_pos[1]+self.key_pos[3]//2)
                            pyautogui.mouseDown()
                            pyautogui.mouseUp()
                            time.sleep(0.2)

                else:
                    # 少1个也算满足 但是必须大于0个条件
                    if ok_condition>=len(self.on_lock_condition)-1  and ok_condition>0 :
                        '2280,540,2388,640,宽高(109,101)'
                        if pyautogui.locateCenterOnScreen(self.imgKey, region=self.key_pos, confidence=self.confidence)==None:
                            pyautogui.moveTo(self.key_pos[0]+self.key_pos[2]//2, self.key_pos[1]+self.key_pos[3]//2)
                            pyautogui.mouseDown()
                            pyautogui.mouseUp()
                            time.sleep(0.2)
                    elif self.isbumanzu==True:#解锁
                        if pyautogui.locateCenterOnScreen(self.imgKey, region=self.key_pos, confidence=self.confidence)!=None:
                            pyautogui.moveTo(self.key_pos[0]+self.key_pos[2]//2, self.key_pos[1]+self.key_pos[3]//2)
                            pyautogui.mouseDown()
                            pyautogui.mouseUp()
                            time.sleep(0.2)
            else:
                if self.isbumanzu == True:  # 解锁
                    if pyautogui.locateCenterOnScreen(self.imgKey, region=self.key_pos, confidence=self.confidence) != None:
                        pyautogui.moveTo(self.key_pos[0] + self.key_pos[2] // 2, self.key_pos[1] + self.key_pos[3] // 2)
                        pyautogui.mouseDown()
                        pyautogui.mouseUp()
                        time.sleep(0.2)
        except Exception as err:
            print(err)

    def set_Art_info_pos(self):
        with open("img\\package.json")as f:
            text=f.read()
        js=json.loads(text)

        size = pyautogui.size()
        #根据分辨率选择配置
        data={}
        for s in js:
            if s['dpi'][0]==size.width and s['dpi'][1]==size.height:
                data=s
                break
        if data=={}:
            input("暂时不支持您的分辨率!")
            exit()
        #然后开始解析分辨率数据
        #1770,129宽高(388,722)圣遗物资料
        self.art_info_pos = data["art_info_pos"]#识别词条的区域 x,y,w,h
        self.art_start_pos= data["art_start_pos"]#滑动开始的位置
        self.art_stop_pos = data["art_stop_pos"]#滑动结束的位置
        self.art_fist_post=data["art_fist_post"]#首个圣遗物的位置
        #圣遗物物品 每个格子的大小
        self.x_step=data["art_step_pos"][0]
        self.y_step = data["art_step_pos"][1]
        #2280,540,2388,640,宽高(109,101)锁搜索区域
        self.key_pos=data["lock_pos"]#锁的区域 x,y,w,h
        self.imgKey=data["img_lock"]#锁图片
        self.confidence=data["confidence"]#相似度

    def run(self):
        while True:
            if self.Art_on==False:
                time.sleep(0.5)
                continue

            for i in range(5):
                if self.Art_on == False:
                    break
                for y in range(8):
                    if self.Art_on == False:
                        break
                    pyautogui.moveTo(self.art_fist_post[0]+(y*self.x_step),self.art_fist_post[1]+(i*self.y_step))
                    pyautogui.mouseDown()
                    pyautogui.mouseUp()
                    time.sleep(0.05)
                    d=self.one_sim()

                    if d==False:
                        self.Art_on = False
                        self.art_list = []
                        continue
                    else:
                        if len(self.art_list)>0:
                            if self.art_list[-1]==d:

                                self.Art_on=False
                                self.art_list = []
                                continue
                        self.art_list.append(d)
            if self.Art_on==False:
                self.art_list = []
                continue

            pyautogui.moveTo(self.art_start_pos [0], self.art_start_pos[1])
            pyautogui.dragTo(self.art_stop_pos[0], self.art_stop_pos[1], duration=2,tween=pyautogui.easeOutSine   )
            time.sleep(1)
class UpAdd():
    def __init__(self):
        self.click_on = False


    def run_upadd(self):

        with open("img\\package.json") as f:
            text = f.read()
        js = json.loads(text)

        size = pyautogui.size()
        # 根据分辨率选择配置
        data = {}
        for s in js:
            if s['dpi'][0] == size.width and s['dpi'][1] == size.height:
                data = s
                break
        if data == {}:
            input("暂时不支持您的分辨率!")
            exit()
        pyautogui.PAUSE = 0.01
        while True:
            if self.click_on == False:
                time.sleep(0.5)
                continue
            pyautogui.moveTo(data["quick_drop"][0], data["quick_drop"][1])
            pyautogui.mouseDown()
            pyautogui.mouseUp()
            time.sleep(0.1)
            if self.click_on == False:
                time.sleep(0.5)
                continue
            pyautogui.moveTo(data["upadd_bt"][0], data["upadd_bt"][1])
            pyautogui.mouseDown()
            pyautogui.mouseUp()
            time.sleep(0.1)
            if self.click_on == False:
                time.sleep(0.5)
                continue
            pyautogui.moveTo(data["info"][0], data["info"][1])
            pyautogui.mouseDown()
            pyautogui.mouseUp()
            if self.click_on == False:
                time.sleep(0.5)
                continue
            time.sleep(0.1)
            pyautogui.moveTo(data["upadd"][0], data["upadd"][1])
            pyautogui.mouseDown()
            pyautogui.mouseUp()
            time.sleep(0.1)














