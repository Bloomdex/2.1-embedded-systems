from PyQt5 import QtWidgets
import controlpanel.model.units as units
import serialcontrol
from controlpanel.view import mainwindow

if __name__ == "__main__":
    detector = serialcontrol.ModuleDetector()

    units.Units.fill_units(detector.arduinos)

    for arduino in detector.arduinos:
        detector.arduinos[arduino].open_connection()
        detector.arduinos[arduino].reader.start()

    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = mainwindow.Ui_MainWindow(MainWindow)
    ui.setupUi(MainWindow)

    MainWindow.show()

    sys.exit(app.exec_())
