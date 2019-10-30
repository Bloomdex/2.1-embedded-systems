import serial.tools.list_ports
from PyQt5 import QtWidgets, QtCore
from serial import SerialException
import debugmenu


class ModuleDetector:
    def __init__(self):
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
                if port.manufacturer.split()[0] == 'Arduino':
                    print("Found an Arduino at:", port.device)

                    module = Module(port)
                    arduino_ports.setdefault(port.name, module)
            except:
                print("Could not connect to possible Arduino:", port.device)

        return arduino_ports


class Module:
    def __init__(self, device):
        self.is_connected = False
        self.ser = None
        self.type = 'None'
        self.com_device = device
        self.data = []
        self.data_is_updated = False
        self.reader = Module.ReadThread(self)
        self.reader.start()

    def open_connection(self):
        try:
            self.ser = serial.Serial(self.com_device.device, 19200)
            self.is_connected = True
        except SerialException:
            print("Could not open connection with Arduino:", self.com_device.device)

    def close_connection(self):
        self.ser.close()
        self.is_connected = False

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
                        self.module.data.append(incoming_byte)
                        self.module.data_is_updated = True
                    except:
                        pass

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
        ui.add_tab(detector.arduinos[arduino])

    Form.show()
    sys.exit(app.exec_())
