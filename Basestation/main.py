from PyQt5 import QtWidgets
import controlpanel.model.units as units
from serialcontrol.serialcontrol import ModuleDetector
from controlpanel.view import mainwindow

if __name__ == "__main__":
    detector = ModuleDetector()

    units.Units.fill_units(detector.arduinos)

    for arduino in detector.arduinos:
        detector.arduinos[arduino].open_connection()

    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = mainwindow.Ui_MainWindow(MainWindow)
    ui.setupUi(MainWindow)
    MainWindow.showMaximized()
    #MainWindow.show()

    sys.exit(app.exec_())
