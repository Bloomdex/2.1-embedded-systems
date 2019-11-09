from __future__ import absolute_import
from functools import partial
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QMdiSubWindow
import controlpanel.view.subwindow as subwindow
import controlpanel.view.setupwindows as setupwindows
import controlpanel.model.units as units


class Ui_MainWindow(object):
    def __init__(self, MainWindow):
        self.MainWindow = MainWindow
        self.ui_subwindow = subwindow
        self.comportsmenulist = []
        self.tileSubWindowsButton = QtWidgets.QAction(self.MainWindow)
        self.cascadeSubWindowButton = QtWidgets.QAction(self.MainWindow)
        self.refreshButton = QtWidgets.QAction(self.MainWindow)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menuOpen = QtWidgets.QMenu(self.menubar)
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
        self.refreshButton.setCheckable(False)
        self.refreshButton.setPriority(QtWidgets.QAction.LowPriority)
        self.refreshButton.setObjectName("refreshButton")
        self.menuSubwindows.addAction(self.tileSubWindowsButton)
        self.menuSubwindows.addAction(self.cascadeSubWindowButton)
        self.menuOpen.addAction(self.refreshButton)

        # add items to menuOpen
        self.add_items_menuOpen()

        # retranslate the ui
        self.retranslateUi(mainwindow)

        # make buttons in directory menuSubwindows active
        self.tileSubWindowsButton.triggered.connect(self.subWindowFrame.tileSubWindows)
        self.cascadeSubWindowButton.triggered.connect(self.subWindowFrame.cascadeSubWindows)
        self.refreshButton.triggered.connect(self.add_items_menuOpen)
        QtCore.QMetaObject.connectSlotsByName(mainwindow)

    def retranslateUi(self, mainwindow):
        _translate = QtCore.QCoreApplication.translate
        mainwindow.setWindowTitle(_translate("mainwindow", "MainWindow"))
        self.menuOpen.setTitle(_translate("mainwindow", "Open"))
        self.menuSubwindows.setTitle(_translate("mainwindow", "Subwindow"))
        self.tileSubWindowsButton.setText(_translate("mainwindow", "Tile"))
        self.cascadeSubWindowButton.setText(_translate("mainwindow", "Cascade"))
        self.refreshButton.setText(_translate("mainwindow", "refresh"))

    def closeEvent(self, window):
        #setupwindows.MakeWindows.to_remove.append()
        print('is removed')

    def add_subwindow(self, comPort):
        win = setupwindows.MakeWindows.make_sub_window(comPort)
        window = QMdiSubWindow()
        window.setWidget(win)
        window.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMaximizeButtonHint)
        #window.closeEvent(self.closeEvent(win))
        self.subWindowFrame.addSubWindow(window)
        window.show()
        self.subWindowFrame.tileSubWindows()

    def add_items_menuOpen(self):
        # removing te old buttons from menuOpen
        for x in self.comportsmenulist:
            self.menuOpen.removeAction(x)
            x.deleteLater()
            print("deleted item")
        self.comportsmenulist.clear()
        print("cleared menu")

        # adding new buttons to menuOpen
        _translate = QtCore.QCoreApplication.translate
        for x in range(len(units.Units.units)):
            print(self.menuOpen.actions())
            self.comportsmenulist.append(QtWidgets.QAction(self.MainWindow))
            self.comportsmenulist[x].setCheckable(False)
            self.comportsmenulist[x].setPriority(QtWidgets.QAction.LowPriority)
            self.comportsmenulist[x].setObjectName("addSunblindButton")
            self.menuOpen.addAction(self.comportsmenulist[x])
            self.comportsmenulist[x].triggered.connect(partial(self.add_subwindow, x))
            self.comportsmenulist[x].setText(_translate("mainwindow", "unit" + str(x)))
