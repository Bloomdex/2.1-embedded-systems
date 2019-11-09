import serial.tools.list_ports
from PyQt5 import QtWidgets, QtCore
import os
import serialcontrol.debugmenu as debugmenu
import serialcontrol.datareader as datareader


class ModuleDetector:
    def __init__(self):
        self.operating_system = os.name
        self.arduinos = {}
        self.update_connected_arduinos()

    def get_arduino_module_type(self, port_id):
        if port_id in self.arduinos.keys():
            return self.arduinos[port_id].type

    def update_connected_arduinos(self):
        previous_connected_ports = self.arduinos.keys()
        current_connected_ports = [value.device for value in serial.tools.list_ports.comports()]

        new_connected_ports = current_connected_ports - previous_connected_ports

        new_ports = [value for value in serial.tools.list_ports.comports() if value.device in new_connected_ports]

        for port in new_ports:
            try:
                if self.operating_system is 'nt':
                    print("Found a COM-device at:", port.device)

                    module = Module(port, port.device)
                    self.arduinos.setdefault(port.device, module)
                elif self.operating_system is 'posix':
                    if port.manufacturer.split()[0] == 'Arduino':
                        print("Found an Arduino at:", port.device)

                        module = Module(port, port.device)
                        self.arduinos.setdefault(port.device, module)
            except:
                print("Could not connect to possible Arduino:", port.device)


class Module:
    def __init__(self, device, name):
        self.name = name
        self.is_connected = False
        self.had_connection = False
        self.ser = None
        self.type = 'None'
        self.com_device = device
        self.data = []
        self.data_is_updated = False
        self.reader = Module.ReadThread(self)

    def open_connection(self):
        try:
            self.ser = serial.Serial(port=self.com_device.device, baudrate=19200, bytesize=8,
                                     parity='N', stopbits=1, timeout=None)
            self.is_connected = True
            self.had_connection = True
            self.reader.start()
            print("Connected with Arduino:", self.com_device.device)
        except Exception:
            pass

    def close_connection(self):
        self.ser.close()
        self.ser = None
        self.is_connected = False

    def send_data(self, hex_byte):
        if self.is_connected:
            self.ser.write(bytearray([hex_byte]))

    def decode_retrieved_data(self):
        decoded_signal = datareader.DataReader.decode_and_return_data(self.data)
        decoded_signal = dict((datareader.data_types[key], value) for (key, value) in decoded_signal.items())

        if 'Status' in decoded_signal.keys():
            status_signal = decoded_signal['Status']
            roller_shutter_states = ['closed', 'closing', 'opening', 'open', 'none']
            sensor_states = ["Not Available", "Good"]

            decoded_signal['Status'] = {}
            decoded_signal['Status'].setdefault('SunBlindForced', bool(status_signal[0]))
            decoded_signal['Status'].setdefault('SunBlind', roller_shutter_states[status_signal[1]])
            decoded_signal['Status'].setdefault('Temperature', sensor_states[status_signal[2]])
            decoded_signal['Status'].setdefault('Light', sensor_states[status_signal[3]])

        self.data.clear()
        return decoded_signal

    class ReadThread(QtCore.QThread):
        def __init__(self, module):
            QtCore.QThread.__init__(self)
            self.module = module
            self.running = False

        def run(self):
            self.running = True
            while self.running:
                if self.module.is_connected:
                    try:
                        incoming_byte = self.module.ser.read()
                        self.module.data.append(int(incoming_byte.hex(), 16))
                        self.module.data_is_updated = True
                    except:
                        print("Lost connection with Arduino:", self.module.com_device.device)
                        self.module.close_connection()
                else:
                    self.running = False
                    break

        def stop(self):
            self.running = False


detector = ModuleDetector()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = debugmenu.DebugMenu()
    ui.setup_ui(Form)

    detector = ModuleDetector()

    for arduino in detector.arduinos:
        detector.arduinos[arduino].reader.start()
        ui.add_tab(detector.arduinos[arduino])

    Form.show()
    sys.exit(app.exec_())
