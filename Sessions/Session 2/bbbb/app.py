# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\gui.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

import cv2
from PyQt5 import QtCore, QtGui, QtWidgets



class Ui_MainWindow(object):
    def __init__(self):
        self.flag = None
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.start_video_btn = QtWidgets.QPushButton(self.centralwidget)
        self.start_video_btn.setGeometry(QtCore.QRect(110, 150, 93, 28))
        self.start_video_btn.setObjectName("start_video_btn")

        self.stop_video_btn = QtWidgets.QPushButton(self.centralwidget)
        self.stop_video_btn.setGeometry(QtCore.QRect(110, 200, 93, 28))
        self.stop_video_btn.setObjectName("stop_video_btn")

        self.enable_btn = QtWidgets.QPushButton(self.centralwidget)
        self.enable_btn.setGeometry(QtCore.QRect(110, 250, 93, 28))
        self.enable_btn.setObjectName("enable_btn")

        self.label_obj = QtWidgets.QLabel(self.centralwidget)
        self.label_obj.setGeometry(QtCore.QRect(100, 110, 161, 16))
        self.label_obj.setObjectName("label_obj")

        self.lcd_obj = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcd_obj.setGeometry(QtCore.QRect(280, 110, 64, 23))
        self.lcd_obj.setObjectName("lcd_obj")

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.start_video_btn.clicked.connect(self.start_video_mthd)
        self.stop_video_btn.clicked.connect(self.stop_video)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.start_video_btn.setText(_translate("MainWindow", "Start Video"))
        self.stop_video_btn.setText(_translate("MainWindow", "STop Video"))
        self.enable_btn.setText(_translate("MainWindow", "Enable M D"))
        self.label_obj.setText(_translate("MainWindow", "Number of moving objs"))
    
    def stop_video(self):
        self.flag = False

    def start_video_mthd(self):
        self.flag = True
        cap = cv2.VideoCapture(0)
        while self.flag:
            # Capture frame-by-frame
            ret, frame = cap.read()
            # Our operations on the frame come here
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # Display the resulting frame
            cv2.imshow('frame',gray)
            if cv2.waitKey(1) and self.flag is False:
                break
        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
