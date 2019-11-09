from __future__ import absolute_import
from functools import partial
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMdiSubWindow
import controlpanel.view.subwindow as subwindow
import controlpanel.view.setupwindows as setupwindows
import controlpanel.model.units as units
from serialcontrol import serialcontrol


class Ui_MainWindow(object):
    def __init__(self, MainWindow):
        self.MainWindow = MainWindow
        self.ui_subwindow = subwindow
        self.comportsmenulist = []
        self.tileSubWindowsButton = QtWidgets.QAction(self.MainWindow)
        self.cascadeSubWindowButton = QtWidgets.QAction(self.MainWindow)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menuOpen = QtWidgets.QMenu(self.menubar)
        self.menuOpen.aboutToShow.connect(self.add_items_menuOpen)
        self.menuSubwindows = QtWidgets.QMenu(self.menubar)
        self.mainFrame = QtWidgets.QWidget(MainWindow)
        self.gridLayout = QtWidgets.QGridLayout(self.mainFrame)
        self.subWindowFrame = QtWidgets.QMdiArea(self.mainFrame)

    def setupUi(self, mainwindow):
        mainwindow.setObjectName("MainWindow")
        mainwindow.resize(517, 645)
        self.mainFrame.setObjectName("mainFrame")
        self.gridLayout.setObjectName("gridLayout")
        self.subWindowFrame.setObjectName("subWindowFrame")
        self.subWindowFrame.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.subWindowFrame.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.subWindowFrame.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.gridLayout.addWidget(self.subWindowFrame, 0, 0, 1, 1)
        mainwindow.setCentralWidget(self.mainFrame)

        # making mainframe with directory's
        self.menubar.setGeometry(QtCore.QRect(0, 0, 517, 21))
        self.menubar.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.menubar.setObjectName("menubar")
        self.menuOpen.setObjectName("menuOpen")
        self.menuSubwindows.setObjectName("menuSubwindows")
        self.menubar.addAction(self.menuOpen.menuAction())
        self.menubar.addAction(self.menuSubwindows.menuAction())
        mainwindow.setMenuBar(self.menubar)

        # adding buttons to menuSubwindows
        self.tileSubWindowsButton.setCheckable(False)
        self.tileSubWindowsButton.setPriority(QtWidgets.QAction.LowPriority)
        self.tileSubWindowsButton.setObjectName("tileSubWindowButton")
        self.cascadeSubWindowButton.setCheckable(False)
        self.cascadeSubWindowButton.setPriority(QtWidgets.QAction.LowPriority)
        self.cascadeSubWindowButton.setObjectName("cascadeSubWindowButton")
        self.menuSubwindows.addAction(self.tileSubWindowsButton)
        self.menuSubwindows.addAction(self.cascadeSubWindowButton)

        # add items to menuOpen
        self.add_items_menuOpen()

        # retranslate the ui
        self.retranslateUi(mainwindow)

        # make buttons in directory menuSubwindows active
        self.tileSubWindowsButton.triggered.connect(self.subWindowFrame.tileSubWindows)
        self.cascadeSubWindowButton.triggered.connect(self.subWindowFrame.cascadeSubWindows)
        QtCore.QMetaObject.connectSlotsByName(mainwindow)

    def retranslateUi(self, mainwindow):
        _translate = QtCore.QCoreApplication.translate
        mainwindow.setWindowTitle(_translate("mainwindow", "MainWindow"))
        self.menuOpen.setTitle(_translate("mainwindow", "Open"))
        self.menuSubwindows.setTitle(_translate("mainwindow", "Subwindow"))
        self.tileSubWindowsButton.setText(_translate("mainwindow", "Tile"))
        self.cascadeSubWindowButton.setText(_translate("mainwindow", "Cascade"))

    def add_subwindow(self, unit):
        win = setupwindows.MakeWindows.make_sub_window(unit)
        window = QMdiSubWindow()
        window.setWidget(win)
        window.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMaximizeButtonHint)
        self.subWindowFrame.addSubWindow(window)
        window.show()
        self.subWindowFrame.tileSubWindows()

    def add_items_menuOpen(self):
        # removing te old buttons from menuOpen
        for x in self.comportsmenulist:
            self.menuOpen.removeAction(x)
            x.deleteLater()
        self.comportsmenulist.clear()

        # adding new buttons to menuOpen
        _translate = QtCore.QCoreApplication.translate
        for arduino in serialcontrol.detector.arduinos:
            self.comportsmenulist.append(QtWidgets.QAction(self.MainWindow))
            index = len(self.comportsmenulist) - 1
            self.comportsmenulist[index].setCheckable(False)
            self.comportsmenulist[index].setPriority(QtWidgets.QAction.LowPriority)
            self.comportsmenulist[index].setObjectName("addSunblindButton")
            self.menuOpen.addAction(self.comportsmenulist[index])
            self.comportsmenulist[index].triggered.connect(partial(self.add_subwindow, arduino))
            self.comportsmenulist[index].setText(_translate("mainwindow", arduino))
