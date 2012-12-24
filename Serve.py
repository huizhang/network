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
port = 12580
toAddr = (host,port+1) #send to
running = True
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.bind((host,port))
class Recv(threading.Thread):
    def Set(self,cht):
        self.t = cht
    def run(self):
        global running
        while running:
            message,address = s.recvfrom(8192)
            text = str(address[0])+"    "+str(time.strftime('%H:%M:%S'))
            self.t.Append(text)
            text = "    "+str(message)
            self.t.Append(text)
    def Stop(self):
        global running
        running = False
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
        self.input.setTextColor(QColor(0,0,255))
        self.input.setFont(font)
        btnSend.setToolTip('Send Message')
        QToolTip.setFont(font)
        
        self.output.setTextColor(QColor(255,0,0))
        self.output.setReadOnly(True)
        self.output.setFont(font)
        self.connect(btnSend,SIGNAL("clicked()"),self.clicked)
        self.setGeometry(500, 50, 350, 400)
        self.setToolTip('Client Two')
        self.setWindowTitle("IM Client Two  "+str(mac))
        self.setWindowIcon(QIcon('image/ch.png'))
    def clicked(self):
        toSendMsg = self.input.toPlainText()
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

app = QApplication(sys.argv)
cht = Chat()
cht.show()
r = Recv()
r.Set(cht)
r.start()
app.exec_()
r.Stop()
r = 1
