import serial.tools.list_ports
from PyQt5 import QtWidgets, QtCore
from serial import SerialException
import os
import serialcontrol.debugmenu as debugmenu
import serialcontrol.datareader as datareader

class ModuleDetector:
    def __init__(self):
        self.operating_system = os.name
        self.arduinos = self.get_connected_arduino_ports()

    def get_arduino_module_type(self, port_id):
        if port_id in self.arduinos.keys():
            print(port_id)

    def update_connected_arduinos(self):
        self.arduinos = self.get_connected_arduino_ports()

    def get_connected_arduino_ports(self):
        ports = serial.tools.list_ports.comports()
        arduino_ports = {}

        for port in ports:
            try:
                if self.operating_system is 'nt':
                    print("Found a COM-device at:", port.device)

                    module = Module(port, port.device)
                    arduino_ports.setdefault(port.device, module)
                elif self.operating_system is 'posix':
                    if port.manufacturer.split()[0] == 'Arduino':
                        print("Found an Arduino at:", port.device)

                        module = Module(port, port.name)
                        arduino_ports.setdefault(port.name, module)
            except:
                print("Could not connect to possible Arduino:", port.device)

        return arduino_ports


class Module:
    def __init__(self, device, name):
        self.name = name
        self.is_connected = False
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
            self.reader.start()
        except SerialException:
            print("Could not open connection with Arduino:", self.com_device.device)

    def close_connection(self):
        self.ser.close()
        self.ser = None
        self.is_connected = False

    def send_data(self, hex_byte):
        if self.is_connected:
            self.ser.write(bytearray([hex_byte]))

    def decode_retrieved_data(self):
        print(self.data)
        decoded_signal = datareader.DataReader.decode_and_return_data(self.data)
        decoded_signal = dict((datareader.data_types[key], value) for (key, value) in decoded_signal.items())

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
                        self.module.close_connection()
                else:
                    self.running = False
                    break

        def stop(self):
            self.running = False


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
