# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\gui.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

import cv2 as cv
from PyQt5 import QtCore, QtGui, QtWidgets

import imutils 
class Ui_MainWindow(object):
	def __init__(self):
		self.running = None
		#self.enable_md_obj = None

	def setupUi(self, MainWindow):
		MainWindow.setObjectName("MainWindow")
		MainWindow.resize(397, 415)
		self.centralwidget = QtWidgets.QWidget(MainWindow)
		self.centralwidget.setObjectName("centralwidget")
		self.start_btn = QtWidgets.QPushButton(self.centralwidget)
		self.start_btn.setGeometry(QtCore.QRect(60, 160, 93, 28))
		self.start_btn.setObjectName("start_btn")
		self.stop_btn = QtWidgets.QPushButton(self.centralwidget)
		self.stop_btn.setGeometry(QtCore.QRect(60, 200, 93, 28))
		self.stop_btn.setObjectName("stop_btn")
		self.enable_md_obj = QtWidgets.QPushButton(self.centralwidget)
		self.enable_md_obj.setGeometry(QtCore.QRect(60, 240, 93, 28))
		self.enable_md_obj.setObjectName("enable_md_obj")
		self.label_obj = QtWidgets.QLabel(self.centralwidget)
		self.label_obj.setGeometry(QtCore.QRect(20, 120, 191, 16))
		self.label_obj.setObjectName("label_obj")
		self.lcd_number_obj = QtWidgets.QLCDNumber(self.centralwidget)
		self.lcd_number_obj.setGeometry(QtCore.QRect(190, 120, 64, 23))
		font = QtGui.QFont()
		font.setPointSize(10)
		font.setBold(True)
		font.setWeight(75)
		self.lcd_number_obj.setFont(font)
		self.lcd_number_obj.setAutoFillBackground(True)
		self.lcd_number_obj.setSmallDecimalPoint(True)
		self.lcd_number_obj.setMode(QtWidgets.QLCDNumber.Dec)
		self.lcd_number_obj.setObjectName("lcd_number_obj")
		MainWindow.setCentralWidget(self.centralwidget)

		self.retranslateUi(MainWindow)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)

		self.start_btn.clicked.connect(self.start_btn_method)
		self.stop_btn.clicked.connect(self.stop_btn_method)
		self.enable_md_obj.clicked.connect(self.start_md)

	def retranslateUi(self, MainWindow):
		_translate = QtCore.QCoreApplication.translate
		MainWindow.setWindowTitle(_translate("MainWindow", "GUI_CoreAI"))
		self.start_btn.setText(_translate("MainWindow", "Start Video"))
		self.stop_btn.setText(_translate("MainWindow", "Stop Video"))
		self.enable_md_obj.setText(_translate("MainWindow", "Enable MD"))
		self.label_obj.setText(_translate("MainWindow", "Number of moving  objects:"))
	
	def start_btn_method(self):
		if self.running is not True:
			self.running = True
			self.get_video()

	def stop_btn_method(self):
		self.running = False

	def get_video(self):
		cap = cv.VideoCapture(0)
		while self.running:
			_, frame = cap.read()
			cv.imshow('frame',frame)
			if cv.waitKey(1) and self.running is False:
				break
		cap.release()
		cv.destroyAllWindows()
	
	def start_md(self):
		if self.running is not True:
			self.running = True
			self.md()
	
	def md(self):
		cap = cv.VideoCapture(0)
		_, frame1 = cap.read()
		_, frame2 = cap.read()

		while cap.isOpened():

			diff = cv.absdiff(frame1, frame2)
			gray = cv.cvtColor(diff, cv.COLOR_BGR2GRAY)
			blur = cv.GaussianBlur(gray, (5, 5), 0)
			_, thresh = cv.threshold(blur, 100, 255, cv.THRESH_BINARY)
			dilated = cv.dilate(thresh, None, iterations=4)
			contours = cv.findContours(dilated, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
			contours = imutils.grab_contours(contours)
			count = 0
			for contour in contours:
					(x, y, w, h) = cv.boundingRect(contour)
					if cv.contourArea(contour) < 700:
							continue
					cv.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
					count+=1
			self.lcd_number_obj.display(count)
			count = 0
			cv.imshow('Motion Detector', frame1)
			frame1 = frame2
			_, frame2 = cap.read()
			if cv.waitKey(1) and self.running is False:
					break
		cap.release()

		cv.destroyAllWindows()


if __name__ == "__main__":
	import sys
	app = QtWidgets.QApplication(sys.argv)
	MainWindow = QtWidgets.QMainWindow()
	ui = Ui_MainWindow()
	ui.setupUi(MainWindow)
	MainWindow.show()
	sys.exit(app.exec_())
