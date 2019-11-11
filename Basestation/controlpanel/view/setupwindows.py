import time
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox, QApplication
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
            QApplication.processEvents()


class Thread(QThread):
    def run(self):
        while True:

            MakeWindows.check_update()

            for unit in units.Units.units:
                units.Units.units[unit].generate_new_data()
                QApplication.processEvents()

            for subwindow in MakeWindows.subwindows:
                try:
                    if subwindow.check_if_module_is_connected():
                        subwindow.subwindow.setEnabled(True)
                        subwindow.update()
                        subwindow.free_button.setEnabled(units.Units.units[subwindow.unit].force)
                    else:
                        units.Units.units[subwindow.unit].module.open_connection()
                        subwindow.subwindow.setEnabled(False)
                except RuntimeError:
                    MakeWindows.to_remove_from_subwindows.append(subwindow)
                QApplication.processEvents()

            '''if MakeWindows.roll_delay >= MakeWindows.roll_delay:
                results = []
                for unit in units.Units.units:
                    results.append(units.Units.check_weather_unit(unit))
                if "open" in results:
                    MakeWindows.roll_delay = 0
                    for unit in units.Units.units:
                        units.Units.units[unit].roll_out()
                elif "close" in results:
                    MakeWindows.roll_delay = 0
                    for unit in units.Units.units:
                        units.Units.units[unit].roll_in()
            MakeWindows.roll_delay += 1'''

            for x in MakeWindows.to_remove_from_subwindows:
                MakeWindows.subwindows.remove(x)
            MakeWindows.to_remove_from_subwindows.clear()

            remove_from_dict = []
            for arduino in serialcontrol.detector.arduinos:
                close_connection = True
                if serialcontrol.detector.arduinos[arduino].is_connected:
                    close_connection = False
                for subwindow in MakeWindows.subwindows:
                    if subwindow.unit == arduino:
                        close_connection = False
                if close_connection:
                    remove_from_dict.append(arduino)
            for arduino in remove_from_dict:
                print("Removed", arduino, "from Unit list")
                del units.Units.units[arduino]
                del serialcontrol.detector.arduinos[arduino]
            for x in range(0, 10):
                time.sleep(0.1)
                QApplication.processEvents()
