# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(891, 789)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 871, 751))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.grid = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.grid.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setSpacing(10)
        self.grid.setObjectName("grid")
        self.plot_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.plot_button.setObjectName("plot_button")
        self.grid.addWidget(self.plot_button, 7, 1, 1, 1)
        self.com_line = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.com_line.setMaximumSize(QtCore.QSize(300, 16777215))
        self.com_line.setObjectName("com_line")
        self.grid.addWidget(self.com_line, 5, 0, 1, 1)
        self.file_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.file_button.setObjectName("file_button")
        self.grid.addWidget(self.file_button, 7, 0, 1, 1)
        self.start_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.start_button.setObjectName("start_button")
        self.grid.addWidget(self.start_button, 6, 0, 1, 1)
        self.lcdNumber = QtWidgets.QLCDNumber(self.gridLayoutWidget)
        self.lcdNumber.setObjectName("lcdNumber")
        self.grid.addWidget(self.lcdNumber, 5, 1, 1, 1)
        self.stop_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.stop_button.setObjectName("stop_button")
        self.grid.addWidget(self.stop_button, 6, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.grid.addWidget(self.label_2, 5, 2, 1, 1)
        self.save_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.save_button.setObjectName("save_button")
        self.grid.addWidget(self.save_button, 6, 2, 1, 1)
        self.quit_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.quit_button.setObjectName("quit_button")
        self.grid.addWidget(self.quit_button, 7, 2, 1, 1)
        self.textBrowser = QtWidgets.QTextBrowser(self.gridLayoutWidget)
        self.textBrowser.setObjectName("textBrowser")
        self.grid.addWidget(self.textBrowser, 3, 0, 1, 3)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setObjectName("label")
        self.grid.addWidget(self.label, 2, 0, 1, 3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 891, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.plot_button.setText(_translate("MainWindow", "Построить график"))
        self.com_line.setText(_translate("MainWindow", "COM6-38400"))
        self.file_button.setText(_translate("MainWindow", "Выбрать файл"))
        self.start_button.setText(_translate("MainWindow", "Начать запись"))
        self.stop_button.setText(_translate("MainWindow", "Остановить запись"))
        self.label_2.setText(_translate("MainWindow", "Значений записано"))
        self.save_button.setText(_translate("MainWindow", "Сохранить в файл"))
        self.quit_button.setText(_translate("MainWindow", "Выход"))
        self.label.setText(_translate("MainWindow", "TextLabel"))
