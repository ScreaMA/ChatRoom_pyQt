import sys
import os
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
from PyQt5.QtWidgets import QApplication,QMainWindow,QMessageBox,QFileDialog
from PyQt5.QtCore import *
from Pyform import Ui_MainWindow
from client import Client
import cmd
import time
import threading
import socket

class MyMainWindow(QMainWindow,Ui_MainWindow):
    global client_case
    address = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
    port = 12346
    client_case = Client((address, port))
    update = pyqtSignal(str)
    fileRecv_quest = pyqtSignal()
    userlist = pyqtSignal()
    userlist_global =None
    def __init__(self,parent = None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.action()

    def action(self):
        self.button_login.clicked.connect(self.loginButton)
        self.button_send.clicked.connect(self.sendButton)
        self.message_clear.clicked.connect(self.messageClear)
        self.select_filepath.clicked.connect(self.fileSelect)
        self.button_sendfile.clicked.connect(self.fileSend)
        self.button_connect.clicked.connect(self.socketUpdate)
        self.update.connect(self.message_update)
        self.fileRecv_quest.connect(self.fileRecv_process)
        self.userlist.connect(self.userlist_update)
        #self.server_address.setText(self.address)
        #self.server_port.setText(str(self.port))
    def socketUpdate(self):
        print(client_case.currentHost)
        try:
            address = self.server_address.text()
            port = int(self.server_port.text())
            client_case.currentHost = (address, port)
            self.message_update("已改变服务器参数，请尝试登陆")
        except:
            self.message_update("correct IP and port needed")
        #self.NetStart()

    def loginButton(self):
        name = self.username.text()
        try:
            client_case.do_login(name)
        except:
            self.message_update("未能连接到服务器，请检查IP和端口设置")
        '''
        if (client_case.flag):
            self.message_display.appendPlainText(client_case.status)
            client_case.flag=0
        else:
            None
        '''
    def sendButton(self):
        text = self.message_send.toPlainText()
        name = self.username_list.currentText()
        message = name + ' ' + text 
        if (self.selected_user.isChecked()):
            client_case.do_sendto(message)
        else:
            client_case.do_send(text)
        time.sleep(0.001)
    def messageClear(self):
        self.message_send.clear()
    def fileSelect(self):
        filepath,filetype = QFileDialog.getOpenFileName(self,"选文件",".","*.*")
        self.path_sendfile.setText(filepath)
    def fileSend(self):
        path = self.path_sendfile.text()
        name = self.username_list.currentText()
        message = name + ' ' + path
        client_case.do_sendfile(message)
    def message_update(self,text):
        self.message_display.appendPlainText(text)
    '''
    def fileRecv_messageBox(self):
        result = QMessageBox.question(self,"有文件来了！","接收不？",QMessageBox.Yes|QMessageBox.No,QMessageBox.NoButton)
        if (result == QMessageBox.Yes):
            command = client_case.status
            client_case.do_getfile(command)
        elif (result == QMessageBox.No):
            client_case.recvFile = False
    '''
    def fileRecv_process(self):
        QuestInfo = client_case.status
        #self.update.emit(QuestInfo)
        client_case.do_getfile(QuestInfo)
    def userlist_update(self):
        text =client_case.status
        if (self.userlist_global!=text):
            self.userlist_global = text
        else:
            return
        text = text.lstrip("[")
        text = text.rstrip("]")
        text = text.replace("\"",'')
        text = text.replace(" ",'')
        userlist_list = text.split(',')
        self.username_list.clear()
        for i in userlist_list:
            self.username_list.addItem(i)
        #self.update.emit(text)
    def update_display(self):
        global timer
        if (client_case.flag==1):
            text = client_case.status
            self.update.emit(text)
            #print("print now")
            client_case.flag=0
        elif (client_case.flag==2):
            self.update.emit("有文件来了，自动接收中")
            self.fileRecv_quest.emit()
            client_case.flag=0
        elif (client_case.flag==3):
            self.userlist.emit()
            client_case.flag=0
        elif (client_case.flag==4):
            self.update.emit("文件接收完成")
            client_case.flag=0
        client_case.do_catusers("")
        timer = threading.Timer(0.3,self.update_display)
        timer.start()
    def NetStart(self):
        client_case.start()


    
        
if __name__ =='__main__':
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    myWin.show()
    myWin.update_display()
    myWin.NetStart()
    sys.exit(app.exec_())

