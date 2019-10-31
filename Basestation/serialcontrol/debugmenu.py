from PyQt5 import QtCore, QtWidgets


class DebugMenu(object):
    def setup_ui(self, form):
        form.setObjectName("Form")
        form.resize(391, 288)

        self.grid_layout = QtWidgets.QGridLayout(form)
        self.grid_layout.setObjectName("gridLayout")

        self.tab_com_devices = QtWidgets.QTabWidget(form)
        self.tab_com_devices.setObjectName("tab_com_devices")

        self.tabs = []

        self.grid_layout.addWidget(self.tab_com_devices, 0, 1, 1, 1)

        self.retranslate_ui(form)
        self.tab_com_devices.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(form)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_received_data_displays)
        self.timer.start(250)

    def add_tab(self, module):
        tab = DebugMenu.DebugTab(module)
        tab.button_connection.clicked.connect(tab.handle_connection)
        tab.button_send_hex.clicked.connect(tab.send_hex_data)

        self.tabs.append(tab)
        self.tab_com_devices.addTab(tab.tab, "")
        self.retranslate_tab(tab)

    def update_received_data_displays(self):
        for tab in self.tabs:
            tab.update_data_display()

    def retranslate_tab(self, tab):
        _translate = QtCore.QCoreApplication.translate
        tab.text_received.setText("")
        tab.button_connection.setText(_translate("Form", "Connect"))
        tab.button_send_hex.setText(_translate("Form", "Send"))
        self.tab_com_devices.setTabText(self.tab_com_devices.indexOf(tab.tab), _translate("Form", tab.name))

    def retranslate_ui(self, form):
        _translate = QtCore.QCoreApplication.translate
        form.setWindowTitle(_translate("Form", "Debug - COM Devices"))

    class DebugTab:
        def __init__(self, module):
            self.module = module
            self.name = module.com_device.name

            self.tab = QtWidgets.QWidget()
            self.tab.setObjectName("tab_" + self.name)

            grid_layout_2 = QtWidgets.QGridLayout(self.tab)
            grid_layout_2.setObjectName("grid_layout_2")
            vertical_layout = QtWidgets.QVBoxLayout()
            vertical_layout.setObjectName("vertical_layout")

            self.text_received = QtWidgets.QTextBrowser(self.tab)
            self.text_received.setObjectName("text_received")
            vertical_layout.addWidget(self.text_received)

            horizontal_layout = QtWidgets.QHBoxLayout()
            horizontal_layout.setObjectName("horizontal_layout")

            self.button_connection = QtWidgets.QPushButton(self.tab)
            self.button_connection.setObjectName("button_connection")

            horizontal_layout.addWidget(self.button_connection)

            self.spinbox_value = 0x00

            self.spinbox_hex = QtWidgets.QSpinBox(self.tab)
            self.spinbox_hex.setMaximum(255)
            self.spinbox_hex.setDisplayIntegerBase(16)
            self.spinbox_hex.setObjectName("spinbox_hex")
            self.spinbox_hex.valueChanged.connect(lambda x: self.read_hex_spinbox_value())
            horizontal_layout.addWidget(self.spinbox_hex)

            self.button_send_hex = QtWidgets.QPushButton(self.tab)
            self.button_send_hex.setObjectName("button_send_hex")

            horizontal_layout.addWidget(self.button_send_hex)
            vertical_layout.addLayout(horizontal_layout)

            grid_layout_2.addLayout(vertical_layout, 0, 0, 1, 1)

        def read_hex_spinbox_value(self):
            self.spinbox_value = self.spinbox_hex.value()

        def handle_connection(self):
            if self.module.is_connected:
                self.module.close_connection()
            else:
                self.module.open_connection()

            self.set_button_connect_name(self.module.is_connected)

        def send_hex_data(self):
            self.module.send_data(self.spinbox_value)

        def set_button_connect_name(self, is_connected):
            if is_connected:
                self.button_connection.setText("Disconnect")
            else:
                self.button_connection.setText("Connect")

        def update_data_display(self):
            if self.module.data_is_updated:
                self.text_received.setText(' '.join([value.hex() for value in self.module.data]))
