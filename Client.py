# -*- coding UTF -8 -*-
import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from Main_UI import Ui_MainWindow
from UI2 import Ui_Form
import time,threading
from PyQt5 import QtWidgets,QtCore,QtGui
import socket
import os
import hashlib
import sys
import pymysql
import struct
import time,threading
from PyQt5.QtCore import *
from PyQt5.QtGui import QMovie
from Edit import Table

global lens,fileName1,mark_num,f_url,f_name,data_num,data_1,data_2
lens = 0
mark_num=1
f_url = ''
f_name =''
data_1=''
data_2=''



class Client5(QThread):
    #ip_port =("10.100.127.253", 8000)#指定要发送的服务器地址和端口

    makeprogress = pyqtSignal(int)

    def __init__(self,filename):
        super(Client5,self).__init__()
        self.filename =filename
        self.lens =0


    def run(self):

        ip_port = ("192.168.69.68", 8000)  # 指定要发送的服务器地址和端口
        #ip_port = ("127.0.0.1", 8000)  # 指定要发送的服务器地址和端口
        try:
            print("socket connect!!")
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 生成socket连接对象
            s.connect(ip_port)  # 连接
            print("socket")
        except socket.error as msg:
            print(msg)  # 输出错误信息
            sys.exit(1)
        print("服务器已连接...\n")
        LEN = 0
        while 1:
            #filepath = input("please input the file path:")  # 输入要发送的文件的路径
            filepath = self.filename
            if os.path.isfile(filepath):  # 如果文件存在
                # 定义文件信息，128sq（其中sq是在不同机器上的衡量单位）表示文件命长128byte
                fileinfo_size = struct.calcsize('128sq')
                # 定义文件名和文件大小
                fhead = struct.pack('128sq', os.path.basename(filepath).encode('utf-8'),
                                    os.stat(filepath).st_size)
                s.send(fhead)  # 发送文件名、文件大小等信息
                print('即将发送的文件的路径为：{0}\n'.format(filepath))
                LENS = os.stat(filepath).st_size  # 获取文件的大小
                m = hashlib.md5()
                fp = open(filepath, 'rb')  # 读取文件
                while 1:
                    #print("qq")
                    data = fp.read(1024)
                    m.update(data)
                    data_len = len(data)
                    LEN += data_len
                    if not data:
                        print('{0} 文件发送完毕...'.format(filepath))
                        break
                    s.send(data)  # 发送文件
                    global lens
                    lens = int(LEN / LENS * 100)
                    #self.makeprogress.emit(lens)
                    #time.sleep(0.0000001)
                    print('已发送：', lens, '%')
                fp.close()  # 关闭
                md5 = m.hexdigest()  # 获取MD５
                s.send(md5.encode('utf-8'))  # 发送ｍｄ５
                print('MD5:', md5)
            #s.close()
            break
        fileinfo_size_2 = struct.calcsize('2048sq')
        global mark_num,f_url,f_name
        f_name = s.recv(fileinfo_size)
        f_name = str(f_name,encoding='utf-8')
        f_url = s.recv(fileinfo_size)
        f_url = str(f_url,encoding='utf-8')
        mark_num=s.recv(fileinfo_size)
        mark_num=int.from_bytes(mark_num,byteorder='big',signed=False)
        print(f_name)
        print(mark_num)
        print(f_url)

        s.close()

class MainForm(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(MainForm,self).__init__()
        self.setupUi(self)



        #菜单的点击事件，当点击关闭菜单时连接槽函数close()
        self.actionClose.triggered.connect(self.close)
        self.actionClose.setStatusTip("退出系统")
        #菜单的点击事件，当点击打开菜单时连接槽函数 openMsg()
        self.actionOpen.triggered.connect(self.openFile)
        self.actionOpen.setStatusTip('导入视频')
        #开发者信息
        self.action.setStatusTip("北京工商大学 明少锋 2019.4.8")
        #子窗口
        #self.addwinaction.triggered.connect(self.childShow)
        #菜单点击事件，当点击打开管理的时候连接槽函数
        self.actionEdit.triggered.connect(self.EditShow)
        self.actionEdit.setStatusTip("视频文件后台管理")
        #self.pushButton.clicked.connect(self.find_num)
        self.pushButton.clicked.connect(self.socket_recognition)
        QApplication.processEvents()
        self.pushButton_2.clicked.connect(self.save_mysql)
        self.action_pink.triggered.connect(self.qss_1)
        self.action_blue.triggered.connect(self.qss_2)
        self.action_green.triggered.connect(self.qss_3)
        self.action_black.triggered.connect(self.qss_4)

        #单选按钮默认选择flow
        self.radioButton.setChecked(True)


        #qss进行布局优化
        font = QtGui.QFont()
        font_max = QtGui.QFont()
        #字体
        font.setFamily('楷体')
        font_max.setFamily('Calibri')
        font_max.setBold(True)
        font.setBold(True)
        #设置字体大小
        font.setPointSize(10)
        font.setWeight(75)
        font_max.setPointSize(15)
        font_max.setWeight(80)
        self.label_5.setFont(font_max)
        self.label.setFont(font)
        self.label_4.setFont(font)
        self.label_2.setFont(font)
        self.label_3.setFont(font)
        self.label_6.setFont(font)
        self.label_3.setAlignment(Qt.AlignCenter)
        self.centralwidget.setStyleSheet("#centralwidget{background-color: white}")
        self.setWindowOpacity(0.9)
        self.pushButton.setStyleSheet('''QPushButton{background:#F76677;border-radius:15px;}
QPushButton:hover{background:red;}''')
        self.pushButton_2.setStyleSheet('''QPushButton{background:#F7D674;border-radius:15px;}
QPushButton:hover{background:yellow;}''')
        self.widget.setStyleSheet('''
        Qwidget#widget{
        color:#232C51;
        background:white;
        border-top:1px solid darkGray;
        border-bottom:1px solid darkGray;
        border-right:1px solid darkGray;
        border-top-right-radius:10px;
        border-bottom-right-radius:10px;
        border-top-left-radius:10px;
        border-bottom-left-radius:10px;
        }
        ''')
        self.qss_2()
        self.gif1 = QMovie('images/happy.gif')
        self.label_3.setMovie(self.gif1)
        self.gif1.start()








    def find_num(self):
        db = pymysql.connect(host='127.0.0.1', port=3306, user='MSF', password='1024161X', db='videos',
                             charset='utf8', )
        cursor = db.cursor()
        num = []
        num.append(mark_num)
        cursor.execute('select action_name from ucf101 where id = %s',num)
        global data_num
        data_num = cursor.fetchone()

        data_num = ' '.join(data_num)
        print(data_num)
        imagName = 'ucf101/'+str(mark_num)+'.jpg'
        self.label_5.setText(data_num)
        jpg = QtGui.QPixmap(imagName)
        self.label_3.setPixmap(jpg)
        self.label_3.setScaledContents(True)


    def save_mysql(self):
        db = pymysql.connect(host='127.0.0.1', port=3306, user='MSF', password='1024161X', db='videos',
                             charset='utf8', )
        cursor = db.cursor()
        list_d = []
        list_d.append(f_name)
        list_d.append(f_url)
        list_d.append(mark_num)
        list_d.append(data_num)
        print(list_d)
        cursor.execute('insert into video(name,url,mark,action) values(%s,%s,%s,%s)', list_d)
        db.commit()
        db.close()



    def SEND(self):
        # 创建 socket 对象
        ip_port = ("192.168.69.68", 8001)
        fileinfo_size = struct.calcsize('128sq')
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(ip_port)  # 连接
        if self.radioButton.isChecked() == True:
            global data_1
            data_1 = '1'
        else:

            data_1 = '2'

        data_1 = bytes(data_1, 'utf-8')

        s.send(data_1)
        global data_2
        data_2 = s.recv(fileinfo_size)
        data_2 = str(data_2, encoding='utf-8')
        data_2 = int(data_2)
        print(data_2)
        print('*******************')

        db = pymysql.connect(host='127.0.0.1', port=3306, user='MSF', password='1024161X', db='videos',
                             charset='utf8', )
        cursor = db.cursor()
        num = []
        print(data_2)
        num.append(data_2)
        cursor.execute('select action_name from ucf101 where id = %s', num)
        global data_num
        global mark_num
        mark_num = data_2
        data_num = cursor.fetchone()

        data_num = ' '.join(data_num)
        print(data_num)
        imagName = 'ucf101/' + str(data_2) + '.jpg'
        self.label_5.setText(data_num)
        jpg = QtGui.QPixmap(imagName)
        self.label_3.setPixmap(jpg)
        self.label_3.setScaledContents(True)


    def socket_recognition(self):

        self.gif2 = QMovie('images/bike.gif')
        self.label_3.setMovie(self.gif2)
        self.gif2.start()

        T = threading.Thread(target=self.SEND, )
        T.start()
        QtWidgets.qApp.processEvents()  # 处理主进程事件
        '''
        # 创建 socket 对象
        ip_port = ("192.168.69.68", 8001)
        fileinfo_size = struct.calcsize('128sq')
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(ip_port)  # 连接
        if self.radioButton.isChecked()==True:
            global data_1
            data_1 = '1'
        else:

            data_1='2'

        data_1=bytes(data_1,'utf-8')
        #T = threading.Thread(target=self.SEND,args=(s))
        #T.start()
        QtWidgets.qApp.processEvents()  # 允许主进程处理事件

        s.send(data_1)
        QtWidgets.qApp.processEvents()  # 允许主进程处理事件
        data_2=s.recv(fileinfo_size)
        QtWidgets.qApp.processEvents()  # 允许主进程处理事件
        data_2=str(data_2,encoding='utf-8')
        data_2=int(data_2)
        print(data_2)
        print('*******************')
        
        

        db = pymysql.connect(host='127.0.0.1', port=3306, user='MSF', password='1024161X', db='videos',
                             charset='utf8', )
        cursor = db.cursor()
        num = []
        print(data_2)
        num.append(data_2)
        cursor.execute('select action_name from ucf101 where id = %s', num)
        global data_num
        global mark_num
        mark_num = data_2
        print('++++++')
        print(data_2)
        print('--------')
        data_num = cursor.fetchone()

        data_num = ' '.join(data_num)
        print(data_num)
        imagName = 'ucf101/' + str(data_2) + '.jpg'
        self.label_5.setText(data_num)
        jpg = QtGui.QPixmap(imagName)
        self.label_3.setPixmap(jpg)
        self.label_3.setScaledContents(True)
        
        '''





    def openimage(self):
        imgName, imgType = QFileDialog.getOpenFileName(self, "打开图片", "", "*.jpg;;*.png;;All Files(*)")
        jpg = QtGui.QPixmap(imgName)
        self.label_3.setPixmap(jpg)
        self.label_3.setScaledContents(True)

        self.label_5.setText(f_name)


    def openFile(self):
        global fileName1
        fileName1, filetype = QFileDialog.getOpenFileName(self, "选取文件", "/Users/MING/Desktop",
                                                          "AVI video (*.avi)")
        print(fileName1, filetype)
        self.statusBar.showMessage(fileName1)
        self.label_2.setText(fileName1)
        self.work = Client5(fileName1)
        QApplication.processEvents()
        if(fileName1):
            self.childShow()
            QApplication.processEvents()
            self.work.start()
            print( "work start")




    def EditShow(self):
        #文件后台管理
        self.Edit = Table()
        self.Edit.show()


    def childShow(self):
        #添加子窗口
        self.child = ChildForm()
        self.child.show()

    def load_data(self, sp):
        for i in range(1, 11):  # 模拟主程序加载过程
            time.sleep(0.3)  # 加载数据
            sp.showMessage("加载... {0}%".format(i * 10), QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom, QtCore.Qt.black)
            QtWidgets.qApp.processEvents()  # 允许主进程处理事件

    def qss_1(self):
        self.centralwidget.setStyleSheet('''#centralwidget{
            background-color: LightPink;
        
            }''')
        self.pushButton.setStyleSheet('''QPushButton{background:#FF6347;border-radius:15px;}
        QPushButton:hover{background:red;}''')
        self.pushButton_2.setStyleSheet('''QPushButton{background:#3CB371;border-radius:15px;}
        QPushButton:hover{background:ForestGreen;}''')

    def qss_2(self):
        self.centralwidget.setStyleSheet('''#centralwidget{
                background-color: LightBLue;

                }''')
        self.pushButton.setStyleSheet('''QPushButton{background:#FF69B4;border-radius:15px;}
        QPushButton:hover{background:red;}''')
        self.pushButton_2.setStyleSheet('''QPushButton{background:#6495ED;border-radius:15px;}
        QPushButton:hover{background:RoyalBlue;}''')

    def qss_3(self):
        self.centralwidget.setStyleSheet('''#centralwidget{
                        background-color: LightSeaGreen;

                        }''')
        self.pushButton.setStyleSheet('''QPushButton{background:#F4A460;border-radius:15px;}
        QPushButton:hover{background:DarkOrange;}''')
        self.pushButton_2.setStyleSheet('''QPushButton{background:#DDA0DD;border-radius:15px;}
        QPushButton:hover{background:Orchid;}''')


    def qss_4(self):
        self.centralwidget.setStyleSheet('''#centralwidget{
                        background-color: LightSlateGray;
                        }''')
        self.pushButton.setStyleSheet('''QPushButton{background:#F0F8FF;border-radius:15px;}
        QPushButton:hover{background:DarkOrange;}''')
        self.pushButton_2.setStyleSheet('''QPushButton{background:#9370DB;border-radius:15px;}
        QPushButton:hover{background:Orchid;}''')

class ChildForm(QWidget,Ui_Form):
    def __init__(self):
        super(QWidget,self).__init__()
        self.setupUi(self)

        #self.pushButton.clicked.connect(self.doAction)
        self.timer = QBasicTimer()
        self.step = 0
        self.timer.start(100,self)
        self.label.setStyleSheet("font:10pt '楷体';")
        self.label.setText('发送文件：\n'+fileName1)
        self.label.setGeometry(QRect(328, 240, 329, 27*4))
        self.label.setWordWrap(True)
        self.label.setAlignment(Qt.AlignTop)
        #self.label_2.setAlignment(Qt.AlignCenter)
        #self.label_2.setScaledContents (True)
        self.gif = QMovie('images/aa.gif')
        self.label_2.setMovie(self.gif)
        self.gif.start()

    def doAction(self):

        if self.timer.isActive():
            self.timer.stop()
            self.pushButton.setText('开始')
        else:
            self.timer.start(100, self)
            self.pushButton.setText('停止')

    def timerEvent(self, e):
        if self.timer.isActive():
            pass
        else:
            self.timer.start(100,self)
        if self.step >= 100:
            self.timer.stop()
            #self.pushButton.setText('完成')
            return
        self.step=lens
        self.progressBar.setValue(self.step)
        self.progressBar.setStyleSheet('''
        QProgressBar::chunk {
            background-color: pink;
            }
        ''')
        




if __name__=="__main__":
    app=QApplication(sys.argv)
    splash = QtWidgets.QSplashScreen(QtGui.QPixmap("images/time.jpg"))
    splash.showMessage("加载... 0%", QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom, QtCore.Qt.black)
    splash.show()  # 显示启动界面
    QtWidgets.qApp.processEvents()  # 处理主进程事件
    win =MainForm()
    win.load_data(splash)  # 加载数据
    win.show()
    #win.qss_4()
    splash.finish(win)  # 隐藏启动界面
    sys.exit(app.exec_())