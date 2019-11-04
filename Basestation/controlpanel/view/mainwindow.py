from __future__ import absolute_import

from functools import partial
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMdiSubWindow
import ProjectEmbeddedSystems.Basestation.controlpanel.view.subwindow as subwindow
import ProjectEmbeddedSystems.Basestation.controlpanel.view.setupwindows as setupwindows
import ProjectEmbeddedSystems.Basestation.controlpanel.model.units as units

class Ui_MainWindow(object):
    def __init__(self, MainWindow):
        self.MainWindow = MainWindow
        self.ui_subwindow = subwindow
        self.comportsmenulist = []
        self.tileSubWindowsButton = QtWidgets.QAction(self.MainWindow)
        self.cascadeSubWindowButton = QtWidgets.QAction(self.MainWindow)
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
        self.menuSubwindows.addAction(self.tileSubWindowsButton)
        self.menuSubwindows.addAction(self.cascadeSubWindowButton)

        # add items to menuOpen
        self.add_items_menuOpen()

        # retranslate the ui
        self.retranslateUi(mainwindow)

        # make buttons in directory menuSubwindows active
        self.tileSubWindowsButton.triggered.connect(self.subWindowFrame.tileSubWindows)
        # self.cascadeSubWindowButton.triggered.connect(self.subWindowFrame.cascadeSubWindows)
        self.cascadeSubWindowButton.triggered.connect(self.add_items_menuOpen)
        QtCore.QMetaObject.connectSlotsByName(mainwindow)

    def retranslateUi(self, mainwindow):
        _translate = QtCore.QCoreApplication.translate
        mainwindow.setWindowTitle(_translate("mainwindow", "MainWindow"))
        self.menuOpen.setTitle(_translate("mainwindow", "Open"))
        self.menuSubwindows.setTitle(_translate("mainwindow", "Subwindow"))
        self.tileSubWindowsButton.setText(_translate("mainwindow", "Tile"))
        self.cascadeSubWindowButton.setText(_translate("mainwindow", "Cascade"))

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
            self.comportsmenulist.append(QtWidgets.QAction(self.MainWindow))
            self.comportsmenulist[x].setCheckable(False)
            self.comportsmenulist[x].setPriority(QtWidgets.QAction.LowPriority)
            self.comportsmenulist[x].setObjectName("addSunblindButton")
            self.menuOpen.addAction(self.comportsmenulist[x])
            self.comportsmenulist[x].triggered.connect(partial(self.add_subwindow, x))
            self.comportsmenulist[x].setText(_translate("mainwindow", "unit" + str(x)))
            print("added item")

'''
    def update(self):
        while True:
            time.sleep(1)
            for x in self.subWindowFrame.subWindowList():
                #x.update_graph()
                test = x(subwindow.Ui_SubWindow)
                test.update_graph()

    
    def add_dockable_subwindow(self, mainwindow):
        if setupwindows.MakeWindows.countSubWindows <= 6:
            window = setupwindows.MakeWindows.makeSubWindow()
            subwindow = QDockWidget("name", mainwindow)
            subwindow.setWidget(window)
            subwindow.setFloating(False)
            subwindow.setFixedSize
            mainwindow.setDockNestingEnabled(True)
            if setupwindows.MakeWindows.countSubWindows < 2 or setupwindows.MakeWindows.countSubWindows == 4:
                mainwindow.addDockWidget(Qt.TopDockWidgetArea, subwindow)
            else:
                mainwindow.addDockWidget(Qt.BottomDockWidgetArea, subwindow)

            setupwindows.MakeWindows.countSubWindows += 1
   
    def add_subwindow_dockable(self, comPort):
        print("test")
        window = setupwindows.MakeWindows.makeSubWindow(comPort)
        subwindow = QDockWidget("name", self.subWindowFrame)
        subwindow.setWidget(window)
        subwindow.setFloating(False)
        #subwindow.setFixedSize()
        #self.subWindowFrame.setDockNestingEnabled(True)
        subwindow.show()
    
    def get_len_sub_window_list(self):
        print(len(self.subWindowFrame.subWindowList))

    def check_sub_window_list(self, element):
        if element in self.subWindowFrame.subWindowList():
            return True
        else:
            return False
'''