import random
import sys
from PyQt5.Qt import *
from qt_material import apply_stylesheet
from qt_material import list_themes
from art import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from ui.main import Ui_MainWindow
from pynput import keyboard
from pynput.keyboard import Key
import threading

class main(QMainWindow, Ui_MainWindow, Artifacts, UpAdd,HookKeyMose):
    def __init__(self):
        # 继承父类
        super().__init__()
        Artifacts.__init__(self)
        UpAdd.__init__(self)
        HookKeyMose.__init__(self, hookKey=True)
        self.set_ui()
        self.setupUi(self)
        self.setWindowTitle('懒人圣遗物强化助手')  # 标题
        self.setWindowFlags(
            Qt.WindowMaximizeButtonHint | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint | Qt.WindowStaysOnTopHint | Qt.Widget)  # 风格
        # self.setAttribute(Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.setWindowOpacity(0.8)  # 设置1-0之间设置窗口透明度
        self.condition_main_cbs = [self.cb_baojilv, self.cb_baojishanghai, self.cb_gongjlibaifenbi,
                             self.cb_shengingzhibaifenbi, self.cb_yuansuchongneng,
                             self.cb_huoyuansu, self.cb_shuiyuansu,
                             self.cb_bingyuansu, self.c_fengyuansu, self.cb_caoyuansu, self.cb_leiyuansu,
                             self.cb_yanyuansu,
                             self.cb_fangyulibaifenbi, self.cb_zhiliao, self.cb_yuansujingtong,self.cb_wulishanghai
                             ]
        self.condition_cbs = [self.cb_baojilv_f, self.cb_baojishanghai_f, self.cb_gongjlibaifenbi_f, self.cb_gongjili_f,
                             self.cb_shengingzhibaifenbi_f, self.cb_shengmingzhi, self.cb_yuansuchongneng_f,
                             self.cb_fangyulibaifenbi_f,  self.cb_fangyuli_f, self.cb_yuansujingtong_f
                             ]
        self.t1 = threading.Thread(target=self.run)
        self.t2 = threading.Thread(target=self.run_upadd)
        self.t1.setDaemon(True)
        self.t2.setDaemon(True)
        self.t1.start()
        self.t2.start()


    def on_release(self, key: keyboard.KeyCode):
        """定义释放时候的响应"""
        try:
            if key == Key.f8:
                if self.rb_filtrate.isChecked() == True:
                    # 更新主词条列表
                    self.on_lock_condition_main =[item.text() for item in self.condition_main_cbs if item.isChecked()==True]
                    print("主词条条件:",self.on_lock_condition)
                    self.on_lock_condition = [item.text() for item in self.condition_cbs if item.isChecked() == True]
                    print("副词条条件:",self.on_lock_condition)
                    self.isshaoyige = self.cb_set_one.isChecked()  # 少1个也算满足
                    self.issancitiao = self.cb_set_four.isChecked()  # 3词条 也算多满足一个
                    self.isbumanzu = self.cb_unlock.isChecked()  # 是否解锁
                    self.Art_on = not self.Art_on
                    self.click_on = False
                    print("筛选运行:", self.Art_on)
                else:
                    self.click_on = not self.click_on
                    self.Art_on = False
        except:
            pass

    def set_ui(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)  # 初始化Qt应用
    window_main = main()
    themes = list_themes()
    apply_stylesheet(app, theme=themes[random.randint(0, len(themes) - 1)])
    window_main.show()
    sys.exit(app.exec_())  # 监听消息不关闭
