# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\MyStuff\Python_proj\ftp\clientv3.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

import fix_qt_import

from PyQt5 import QtCore, QtGui, QtWidgets

import socket
import time


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(828, 536)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(20, 20, 561, 411))
        self.listWidget.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.listWidget.setObjectName("listWidget")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(20, 450, 561, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.viewfile = QtWidgets.QPushButton(self.centralwidget)
        self.viewfile.setGeometry(QtCore.QRect(620, 120, 181, 41))
        self.viewfile.setObjectName("viewfile")
        self.viewfolder = QtWidgets.QPushButton(self.centralwidget)
        self.viewfolder.setGeometry(QtCore.QRect(620, 180, 181, 41))
        self.viewfolder.setObjectName("viewfolder")
        self.download = QtWidgets.QPushButton(self.centralwidget)
        self.download.setGeometry(QtCore.QRect(620, 240, 181, 41))
        self.download.setObjectName("download")
        self.quit = QtWidgets.QPushButton(self.centralwidget)
        self.quit.setGeometry(QtCore.QRect(660, 60, 141, 31))
        self.quit.setObjectName("quit")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(620, 340, 131, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(620, 370, 191, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(620, 390, 181, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(620, 420, 191, 16))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(620, 440, 191, 16))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(620, 460, 181, 16))
        self.label_6.setObjectName("label_6")
        self.connectb = QtWidgets.QPushButton(self.centralwidget)
        self.connectb.setGeometry(QtCore.QRect(660, 20, 141, 31))
        self.connectb.setObjectName("connectb")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(620, 290, 181, 16))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 828, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.viewfile.clicked.connect(self.liststuff)
        self.viewfolder.clicked.connect(self.listfolder)
        self.download.clicked.connect(self.dlfile)
        self.quit.clicked.connect(self.quitting)
        self.connectb.clicked.connect(self.ccheck)



    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.viewfile.setText(_translate("MainWindow", "View Files"))
        self.viewfolder.setText(_translate("MainWindow", "View Folder"))
        self.download.setText(_translate("MainWindow", "Download File"))
        self.quit.setText(_translate("MainWindow", "Quit"))
        self.label.setText(_translate("MainWindow", "How to use:"))
        self.label_2.setText(_translate("MainWindow", "Click View Files to view files of"))
        self.label_3.setText(_translate("MainWindow", "main directory"))
        self.label_4.setText(_translate("MainWindow", "To download file or view folder"))
        self.label_5.setText(_translate("MainWindow", "type the name/path and press"))
        self.label_6.setText(_translate("MainWindow", "corresponding button"))
        self.connectb.setText(_translate("MainWindow", "Connect"))

    def liststuff(self):
        host = '172.16.57.44'
        port = 12397
        try:
            s = socket.socket()
            s.connect((host,port))
            s.send(b'list content')
            content = s.recv(1024).decode()
            self.listWidget.addItem(content)
            s.close()
        except:
            self.listWidget.addItem("Connection not available")

    def listfolder(self):
        folder = self.lineEdit.text()

        if folder != "" :
            host = '172.16.57.44'
            port = 12397
            try:
                s = socket.socket()
                s.connect((host,port))
                self.lineEdit.clear()
                folder = "folder viewed: "+folder
                s.sendall(folder.encode())
                data = s.recv(1024).decode()
                self.listWidget.addItem(data)
                s.close()
            except:
                self.listWidget.addItem("Connection not available")

    def dlfile(self):
        file = self.lineEdit.text()
        foldercheck = file.split('/')[0]
        if file != "" and foldercheck != "dist":
            host = '172.16.57.44'
            port = 12397
            try:
                s = socket.socket()
                s.connect((host,port))
                self.lineEdit.clear()
                s.sendall(file.encode())
                data = s.recv(1024).decode()
                if data[:6] == 'EXISTS':
                    self.listWidget.addItem(file+ " ; "+data)
                    filesize = int(data[6:])
                    #self.listWidget
                    #self.listWidget.addItem("dl will start in 5 sec")
                    #time.sleep(5)
                    self.listWidget.addItem("dl start")
                    time.sleep(.5)
                    s.send(b'OK')
                    filename = file.split('/')[-1]
                    f = open('new_'+filename, 'wb')
                    data = s.recv(1024)
                    totalRecv = len(data)
                    f.write(data)
                    ctrval = 0.0
                    while totalRecv < filesize:
                        data = s.recv(1024)
                        totalRecv += len(data)
                        f.write(data)
                        curval = float("{0:.2f}".format((totalRecv/float(filesize))*100))
                        if curval.is_integer() and curval > ctrval:
                            #self.listWidget.addItem("{0:.2f}".format((totalRecv/float(filesize))*100)+"%done")
                            self.progressBar.setValue(curval)
                            ctrval = curval
                    self.listWidget.addItem("Download complete")
                else:
                    self.listWidget.addItem("file does not exist")

                s.close()
            except:
                self.listWidget.addItem("Connection not available")

    def ccheck(self):
        host = '172.16.57.44'
        port = 12397
        try:
            s = socket.socket()
            s.connect((host,port))
            s.send(b'connection')
            message = s.recv(1024).decode()
            self.listWidget.addItem(message)
            s.close()
        except:
            self.listWidget.addItem("Connection not available")

    def quitting(self):
        host = '172.16.57.44'
        port = 12397
        try:
            s = socket.socket()
            s.connect((host,port))
            s.send(b'client quit')
            s.close()
            sys.exit()
        except:
            self.listWidget.addItem("Connection not available")
            sys.exit()



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

