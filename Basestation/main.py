from controlpanel.view.setupwindows import MakeWindows


if __name__ == "__main__":

    #units.Units.fill_units(serialcontrol.detector.arduinos)
    #for arduino in serialcontrol.detector.arduinos:
        #serialcontrol.detector.arduinos[arduino].open_connection()

    MakeWindows.make_main_window()

    ""'''
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = mainwindow.Ui_MainWindow(MainWindow)
    ui.setupUi(MainWindow)
    MainWindow.showMaximized()

    sys.exit(app.exec_())
    '''