# -*- coding: cp936 -*-
from __future__ import division
from math import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import socket,traceback
import threading
import uuid
import time
host = '127.0.0.1'
port = 12581
toAddr = (host,port-1)
running = True
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.bind((host,port))
class Recv(threading.Thread):
    def Set(self,ch):
        self.t = ch
    def run(self):
        global running
        while running:
            print '222'
            message,address = s.recvfrom(8192)
            print '444'
            text = str(address[0])+"    "+str(time.strftime('%H:%M:%S'))
            self.t.Append(text)
            text = "    "+str(message)
            self.t.Append(text)     
        #print '11'
        return 1
    def Stop(self):
        global running
        running = False
        self.t = 1
        print 'stop1 '
        return 
localIP = socket.gethostbyname(socket.gethostname())
node = uuid.getnode()
mac = uuid.UUID(int = node).hex[-12:]

class Chat(QDialog):
    def __init__(self,parent = None):
        super(Chat,self).__init__(parent)
        font = QFont()
        font.setFamily('Consolas')
        font.setFixedPitch(True)
        font.setPointSize(10)
      
        self.text = ""
        self.input = QTextEdit()
        self.output = QTextEdit()
        self.lab1 = QLabel("                ")
        self.lab2 = QLabel("                ")
        btnSend = QPushButton("Send")
        grid = QGridLayout()
        tgd = QGridLayout()
        grid.addWidget(self.output,0,0)
        grid.addWidget(self.lab1,0,1)
        grid.addWidget(self.input,1,0)
        grid.addWidget(self.lab2,1,1)
        grid.addLayout(tgd,2,0,1,1)
        tgd.addWidget(self.lab1,0,2)
        tgd.addWidget(btnSend,0,3)
        self.setLayout(grid)
        self.input.setFocus()
        self.input.setTextColor(QColor(255,0,0))
        self.input.setFont(font)
        
        btnSend.setToolTip('Send Message')
        QToolTip.setFont(font)
        
        self.output.setReadOnly(True)
        self.output.setFont(font)
        self.output.setTextColor(QColor(0,0,255))
        self.connect(btnSend,SIGNAL("clicked()"),self.clicked)
        self.setGeometry(50, 50, 350, 400)
        self.setToolTip('Client One')
        self.setWindowTitle("IM Client One  "+ str(mac))
        self.setWindowIcon(QIcon('image/ch.png'))
        
       
 

    
    def clicked(self):
        toSendMsg = self.input.toPlainText()
        print 'hhaha'
        if len(toSendMsg)==0:
            msgBox = QMessageBox()
            msgBox.setText("The send message should not be empty")
        else:
            text = str(localIP)+"   "+str(time.strftime('%H:%M:%S'))
            self.output.append(text)
            text = "    "+str(toSendMsg)
            self.output.append(text)
            s.sendto(str(toSendMsg),toAddr)
            self.input.clear()
    def closeEvent(self,event):
        reply = QMessageBox().question(self,'Message',
                                       'Are you sure to quit',
                                       QMessageBox.Yes,QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
        #sys.exit()
    def Append(self,text):
        self.output.append(text)
        self.output.moveCursor(QTextCursor.End)
    def SetFocus(self):
        self.input.setFocus()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    cht = Chat()
    cht.show()
    r = Recv()
    r.Set(cht)
    r.start()
    app.exec_()  
    r.Stop()
    print 'test'
    running = False
