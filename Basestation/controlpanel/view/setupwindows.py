import time
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox
import sys
import controlpanel.view.mainwindow as mainwindow
import controlpanel.view.subwindow as subwindow
import controlpanel.model.units as units
import serialcontrol.serialcontrol as serialcontrol
from controlpanel.model import sunblindmodel


class MakeWindows:
    subwindows = []
    roll_delay = 60
    thread_running = False
    MainWindow = None
    to_remove_from_subwindows = []

    @staticmethod
    def make_main_window():
        app = QtWidgets.QApplication(sys.argv)
        app.setWindowIcon(QIcon("dashboard_icon.png"))
        MainWindow = QtWidgets.QMainWindow()
        ui = mainwindow.Ui_MainWindow(MainWindow)
        ui.setupUi(MainWindow)
        MainWindow.showMaximized()
        thread = Thread()
        thread.finished.connect(app.exit)
        thread.start()
        MakeWindows.MainWindow = ui
        sys.exit(app.exec_())

    @staticmethod
    def make_sub_window(unit):
        SubWindow = QtWidgets.QMainWindow()
        ui = subwindow.Ui_SubWindow()
        ui.setupUi(SubWindow, unit)
        SubWindow.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        MakeWindows.subwindows.append(ui)
        return SubWindow

    @staticmethod
    def make_max_error():
        message = QMessageBox()
        message.setWindowTitle("ERROR")
        message.setText("Maximum must be higher then minimum.")
        message.setIcon(QMessageBox.Critical)
        message.exec_()

    @staticmethod
    def make_min_error():
        message = QMessageBox()
        message.setWindowTitle("ERROR")
        message.setText("Minimum must be lower then maximum.")
        message.setIcon(QMessageBox.Critical)
        message.exec_()

    @staticmethod
    def update_light_intensity_inputs():
        for x in MakeWindows.subwindows:
            x.light_intensity_input.setValue(units.Units.get_unit_light_intensity(x.unit))

    @staticmethod
    def update_temp_inputs():
        for x in MakeWindows.subwindows:
            x.temperature_input.setValue(units.Units.get_unit_temp(x.unit))

    @staticmethod
    def update_min_inputs():
        for x in MakeWindows.subwindows:
            x.min_roll_out_input.setValue(units.Units.get_unit_min(x.unit))

    @staticmethod
    def update_max_inputs():
        for x in MakeWindows.subwindows:
            x.max_roll_out_input.setValue(units.Units.get_unit_max(x.unit))

    @staticmethod
    def check_update():
        serialcontrol.detector.update_connected_arduinos()
        arduinos = serialcontrol.detector.arduinos
        for arduino in serialcontrol.detector.arduinos:
            if not serialcontrol.detector.arduinos[arduino].is_connected and not serialcontrol.detector.arduinos[arduino].had_connection:
                serialcontrol.detector.arduinos[arduino].open_connection()
                units.Units.add_unit_to_units(sunblindmodel.SunBlindModel(arduinos[arduino]))


class Thread(QThread):
    def run(self):
        while True:
            MakeWindows.check_update()

            for unit in units.Units.units:
                unit.generate_new_data()

            for x in MakeWindows.subwindows:
                try:
                    if x.check_if_module_is_connected():
                        x.subwindow.setEnabled(True)
                        x.update()
                    else:
                        units.Units.units[x.unit].module.open_connection()
                        x.subwindow.setEnabled(False)
                except RuntimeError:
                    MakeWindows.to_remove_from_subwindows.append(x)
            if MakeWindows.roll_delay >= 60:
                results = []
                for x in range(len(units.Units.units)):
                    results.append(units.Units.check_weather_unit(x))
                if "open" in results:
                    MakeWindows.roll_delay = 0
                    for x in range(len(units.Units.units)):
                        units.Units.roll_out_unit(x)
                elif "close" in results:
                    MakeWindows.roll_delay = 0
                    for x in range(len(units.Units.units)):
                        units.Units.roll_in_unit(x)
            MakeWindows.roll_delay += 1

            for x in MakeWindows.to_remove_from_subwindows:
                MakeWindows.subwindows.remove(x)
            MakeWindows.to_remove_from_subwindows.clear()
            for x in range(0, 10):
                time.sleep(0.1)
