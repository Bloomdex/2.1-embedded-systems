from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg
import controlpanel.model.units as units
import os


class Ui_SubWindow(object):
    def setupUi(self, SubWindow, unit):
        self.subwindow = SubWindow
        self.unit = unit
        SubWindow.setObjectName("SubWindow")
        SubWindow.setMinimumHeight(280)
        SubWindow.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMaximizeButtonHint)

        self.centralwidget = QtWidgets.QWidget(SubWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.sunblindName = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.sunblindName.setFont(font)
        self.sunblindName.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignHCenter)
        self.sunblindName.setObjectName("sunblindName")
        self.gridLayout.addWidget(self.sunblindName, 0, 1, 1, 1)

        # roll out
        # label_roll_out
        self.label_roll_out = QtWidgets.QLabel(self.centralwidget)
        self.label_roll_out.setAlignment(QtCore.Qt.AlignCenter)
        self.label_roll_out.setObjectName("label_roll_out")
        self.gridLayout.addWidget(self.label_roll_out, 2, 0, 1, 2)
        # min_roll_out_input
        self.min_roll_out_input = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.min_roll_out_input.setObjectName("min_roll_out_input")
        self.min_roll_out_input.setSingleStep(0.1)
        self.min_roll_out_input.setMinimum(0.0)
        self.min_roll_out_input.setMaximum(2.5)
        self.min_roll_out_input.setValue(units.Units.get_unit_min(self.unit))
        self.min_roll_out_input.valueChanged.connect(lambda x: self.set_min_input_value())
        self.gridLayout.addWidget(self.min_roll_out_input, 3, 0, 1, 1)
        # max_roll_out_input
        self.max_roll_out_input = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.max_roll_out_input.setObjectName("max_roll_out_input")
        self.max_roll_out_input.setSingleStep(0.1)
        self.max_roll_out_input.setMinimum(0.0)
        self.max_roll_out_input.setMaximum(2.5)
        self.max_roll_out_input.setValue(units.Units.get_unit_max(self.unit))
        self.max_roll_out_input.valueChanged.connect(lambda x: self.set_max_input_value())
        self.gridLayout.addWidget(self.max_roll_out_input, 4, 0, 1, 1)
        # set_min_roll_out_button
        self.set_min_roll_out_button = QtWidgets.QPushButton(self.centralwidget)
        self.set_min_roll_out_button.setObjectName("set_min_roll_out_Button")
        self.min_input_value = self.min_roll_out_input.value()
        self.set_min_roll_out_button.clicked.connect(lambda x: units.Units.set_unit_min(self.unit, self.min_input_value))
        self.gridLayout.addWidget(self.set_min_roll_out_button, 3, 1, 1, 1)
        # set set_max_roll_out_button
        self.set_max_roll_out_button = QtWidgets.QPushButton(self.centralwidget)
        self.set_max_roll_out_button.setObjectName("set_max_roll_out_button")
        self.max_input_value = self.max_roll_out_input.value()
        self.set_max_roll_out_button.clicked.connect(lambda x: units.Units.set_unit_max(self.unit, self.max_input_value))
        self.gridLayout.addWidget(self.set_max_roll_out_button, 4, 1, 1, 1)

        # light intensity
        # labels
        self.label_light_intensity = QtWidgets.QLabel(self.centralwidget)
        self.label_light_intensity.setAlignment(QtCore.Qt.AlignCenter)
        self.label_light_intensity.setObjectName("label_light_intensity")
        self.gridLayout.addWidget(self.label_light_intensity, 2, 3, 1, 2)
        # light_intensity_input
        self.light_intensity_input = QtWidgets.QSpinBox(self.centralwidget)
        self.light_intensity_input.setObjectName("light_intensity_input")
        self.light_intensity_input.setMinimum(0)
        self.light_intensity_input.setMaximum(100)
        self.light_intensity_input.setValue(units.Units.get_unit_light_intensity(self.unit))
        self.light_intensity_input.valueChanged.connect(lambda x: self.set_light_intensity_value())
        self.gridLayout.addWidget(self.light_intensity_input, 3, 3, 1, 1)
        # set_light_intensity_button
        self.set_light_intensity_button = QtWidgets.QPushButton(self.centralwidget)
        self.set_light_intensity_button.setObjectName("set_light_intensity_button")
        self.light_intensity_value = self.light_intensity_input.value()
        self.set_light_intensity_button.clicked.connect(lambda x: units.Units.set_unit_light_intensity(self.unit, self.light_intensity_value))
        self.gridLayout.addWidget(self.set_light_intensity_button, 3, 4, 1, 1)

        # temperature
        # label_temperature
        self.label_temperature = QtWidgets.QLabel(self.centralwidget)
        self.label_temperature.setAlignment(QtCore.Qt.AlignCenter)
        self.label_temperature.setObjectName("label_temperature")
        self.gridLayout.addWidget(self.label_temperature, 2, 6, 1, 2)
        # temperature_input
        self.temperature_input = QtWidgets.QSpinBox(self.centralwidget)
        self.temperature_input.setObjectName("temperature_input")
        self.temperature_input.setMinimum(-20.0)
        self.temperature_input.setMaximum(70)
        self.temperature_input.setValue(units.Units.get_unit_temp(self.unit))
        self.temperature_input.valueChanged.connect(lambda x: self.set_temperature_value())
        self.gridLayout.addWidget(self.temperature_input, 3, 6, 1, 1)
        # set_temperature_button
        self.set_temperature_button = QtWidgets.QPushButton(self.centralwidget)
        self.set_temperature_button.setObjectName("set_temperature_button")
        self.temperature_value = self.temperature_input.value()
        self.set_temperature_button.clicked.connect(lambda x: units.Units.set_unit_temp(self.unit, self.temperature_value))
        self.gridLayout.addWidget(self.set_temperature_button, 3, 7, 1, 1)

        # function
        # label_functions
        self.label_functions = QtWidgets.QLabel(self.centralwidget)
        self.label_functions.setAlignment(QtCore.Qt.AlignCenter)
        self.label_functions.setObjectName("label_functions")
        self.gridLayout.addWidget(self.label_functions, 2, 11, 1, 2)
        # free_button
        self.free_button = QtWidgets.QPushButton(self.centralwidget)
        self.free_button.setObjectName("free_button")
        self.free_button.clicked.connect(lambda x: units.Units.set_free_unit(self.unit))
        self.gridLayout.addWidget(self.free_button, 3, 11, 2, 1)
        # up_button
        self.up_button = QtWidgets.QPushButton(self.centralwidget)
        self.up_button.setObjectName("up_button")
        self.up_button.clicked.connect(lambda x: units.Units.roll_in_unit(self.unit))
        self.gridLayout.addWidget(self.up_button, 3, 12, 1, 1)
        # down_button
        self.down_button = QtWidgets.QPushButton(self.centralwidget)
        self.down_button.setObjectName("down_button")
        self.down_button.clicked.connect(lambda x: units.Units.roll_out_unit(self.unit))
        self.gridLayout.addWidget(self.down_button, 4, 12, 1, 1)

        # lines
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 2, 2, 4, 1)
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout.addWidget(self.line_2, 2, 5, 4, 1)
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.gridLayout.addWidget(self.line_3, 2, 8, 4, 1)
        self.line_4 = QtWidgets.QFrame(self.centralwidget)
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.gridLayout.addWidget(self.line_4, 2, 10, 4, 1)

        # spacer
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 9, 4, 1)

        # the tabwidget
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setMinimumSize(QtCore.QSize(0, 0))
        self.tabWidget.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.tabWidget.setFocusPolicy(QtCore.Qt.TabFocus)
        self.tabWidget.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.tabWidget.setElideMode(QtCore.Qt.ElideNone)
        self.tabWidget.setTabBarAutoHide(False)
        self.tabWidget.setObjectName("tabWidget")
        # the data tab and gridLayout 3
        self.Data = QtWidgets.QWidget()
        self.Data.setObjectName("Data")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.Data)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tabWidget.addTab(self.Data, "")
        # the stauts tab and gridLayout 4
        self.Status = QtWidgets.QWidget()
        self.Status.setObjectName("Status")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.Status)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.tabWidget.addTab(self.Status, "")
        self.gridLayout.addWidget(self.tabWidget, 1, 0, 1, 13)

        # the graph op Data tab
        self.pen = QtGui.QPen()
        self.pen.setColor(QtGui.QColor(125, 175, 25))
        self.pen.setWidth(.7)
        self.pen.setStyle(QtCore.Qt.SolidLine)
        self.pen2 = QtGui.QPen()
        self.pen2.setColor(QtGui.QColor(125, 25, 25))
        self.pen2.setWidth(.7)
        self.pen2.setStyle(QtCore.Qt.SolidLine)

        self.graph = pg.PlotWidget(self.Data, title="Data")
        self.graph.setWindowTitle("Sunblind data")
        self.graph.addLegend()

        temperature_data = units.Units.get_data_temp(self.unit)
        light_data = units.Units.get_data_light(self.unit)

        # TODO: Replace x with something useful.
        self.graph_temp = self.graph.plotItem.plot([*range(len(temperature_data))],
                                                   temperature_data,
                                                   pen=self.pen, name="_Temperature")
        self.graph_light = self.graph.plotItem.plot([*range(len(light_data))],
                                                    light_data,
                                                    pen=self.pen2, name="_Light")

        #self.update_graph()
        labelStyle = {'color': '#FFF', 'font-size': '10pt'}
        self.graph.setLabel('left', 'Temperature/Light intensity', **labelStyle)
        self.graph.setLabel('bottom', 'Datapoint', **labelStyle)
        self.gridLayout_2.addWidget(self.graph, 0, 0, 1, 1)

        # statusText on status tab
        self.statusText = QtWidgets.QLabel(self.Status)
        font2 = QtGui.QFont()
        font2.setPointSize(15)
        font2.setBold(False)
        font2.setItalic(False)
        font2.setWeight(50)
        font2.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.statusText.setFont(font2)
        self.statusText.setAlignment(QtCore.Qt.AlignHCenter)
        self.statusText.setText("Status")
        self.gridLayout_3.addWidget(self.statusText, 0, 0, 1, 1)
        # status table
        self.tableWidget = QtWidgets.QTableWidget(self.Status)
        if os.name is 'nt':
            self.tableWidget.setStyleSheet("background: rgb(255, 255, 255)")
        self.tableWidget.setFocusPolicy(QtCore.Qt.NoFocus)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)
        self.tableWidget.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.tableWidget.setFrameShape(QtWidgets.QFrame.Box)
        self.tableWidget.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.tableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.tableWidget.setAutoScrollMargin(15)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.CurrentChanged)
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.tableWidget.setTextElideMode(QtCore.Qt.ElideMiddle)
        self.tableWidget.setShowGrid(True)
        self.tableWidget.setGridStyle(QtCore.Qt.NoPen)
        self.tableWidget.setWordWrap(True)
        self.tableWidget.setCornerButtonEnabled(True)
        self.tableWidget.setRowCount(4)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(3)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(0, 2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(1, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(1, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(1, 2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(2, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(2, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(2, 2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(3, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(3, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(3, 2, item)
        self.tableWidget.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setVisible(True)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(True)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(109)
        self.tableWidget.horizontalHeader().setHighlightSections(True)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(109)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(False)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setDefaultSectionSize(18)
        self.tableWidget.verticalHeader().setHighlightSections(True)
        self.tableWidget.verticalHeader().setMinimumSectionSize(18)
        self.tableWidget.verticalHeader().setStretchLastSection(False)
        self.gridLayout_3.addWidget(self.tableWidget, 0, 0, 1, 1)

        # text on in the top from the window
        self.sunBlindName = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.sunBlindName.setFont(font)
        self.sunBlindName.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignHCenter)
        self.sunBlindName.setObjectName("sunblindName")
        self.gridLayout.addWidget(self.sunBlindName, 0, 1, 1, 13)

        SubWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(SubWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(SubWindow)

    def retranslateUi(self, SubWindow):
        _translate = QtCore.QCoreApplication.translate
        SubWindow.setWindowTitle(_translate("SubWindow", "unit" + str(self.unit)))
        self.label_functions.setText(_translate("SubWindow", "Functions"))
        self.label_roll_out.setText(_translate("SubWindow", "Set sun blind roll out "))
        self.free_button.setText(_translate("SubWindow", "FREE"))
        self.up_button.setText(_translate("SubWindow", "UP"))
        self.down_button.setText(_translate("SubWindow", "DOWN"))
        self.set_max_roll_out_button.setText(_translate("SubWindow", "Set max"))
        self.set_min_roll_out_button.setText(_translate("SubWindow", "Set min"))
        self.label_light_intensity.setText(_translate("SubWindow", "Set light intensity"))
        self.set_light_intensity_button.setText(_translate("SubWindow", "Set light intensity"))
        self.label_temperature.setText(_translate("SubWindow", "Set temperature"))
        self.set_temperature_button.setText(_translate("SubWindow", "Set Temperature"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Data), _translate("SubWindow", "Data"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Status), _translate("SubWindow", "Status"))
        self.sunBlindName.setText(_translate("SubWindow", "Unit " + str(self.unit)))
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("SubWindow", "light sensor"))
        item = self.tableWidget.verticalHeaderItem(1)
        item.setText(_translate("SubWindow", "temperature sensor"))
        item = self.tableWidget.verticalHeaderItem(2)
        item.setText(_translate("SubWindow", "ultrasoon sensor"))
        item = self.tableWidget.verticalHeaderItem(3)
        item.setText(_translate("SubWindow", "sun blind"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("SubWindow", "Sensor"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("SubWindow", "Status"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("SubWindow", "Sensor value"))
        self.update_status()

    def set_status(self):
        if units.Units.get_status(self.unit) == "open":
            self.statusText.setText("This sun blind is open.")
        else:
            self.statusText.setText("This sun blind is closed.")

    def set_min_input_value(self):
        self.min_input_value = self.min_roll_out_input.value()

    def set_max_input_value(self):
        self.max_input_value = self.max_roll_out_input.value()

    def set_light_intensity_value(self):
        self.light_intensity_value = self.light_intensity_input.value()

    def set_temperature_value(self):
        self.temperature_value = self.temperature_input.value()

    def update_graph(self):
        temperature_data = units.Units.get_data_temp(self.unit)
        light_data = units.Units.get_data_light(self.unit)

        self.graph_temp.setData(x=[*range(len(temperature_data))], y=temperature_data)
        self.graph_light.setData(x=[*range(len(light_data))], y=light_data)

    def update_status(self):
        status = units.Units.get_status(self.unit)
        data_light = units.Units.get_last_data_light(self.unit)
        data_temp = units.Units.get_last_data_temp(self.unit)
        data_ultrasoon = units.Units.get_last_data_ultrasoon(self.unit)

        item = self.tableWidget.item(0, 0)
        _translate = QtCore.QCoreApplication.translate
        item.setText(_translate("SubWindow", "light sensor"))
        item = self.tableWidget.item(0, 1)
        item.setText(_translate("SubWindow", status[0]))
        item = self.tableWidget.item(0, 2)
        item.setText(_translate("SubWindow", str(data_light)))
        item = self.tableWidget.item(1, 0)
        item.setText(_translate("SubWindow", "temperature sensor"))
        item = self.tableWidget.item(1, 1)
        item.setText(_translate("SubWindow", status[1]))
        item = self.tableWidget.item(1, 2)
        item.setText(_translate("SubWindow", str(data_temp)))
        item = self.tableWidget.item(2, 0)
        item.setText(_translate("SubWindow", "ultrasoon sensor"))
        item = self.tableWidget.item(2, 1)
        item.setText(_translate("SubWindow", status[2]))
        item = self.tableWidget.item(2, 2)
        item.setText(_translate("SubWindow", str(data_ultrasoon)))
        item = self.tableWidget.item(3, 0)
        item.setText(_translate("SubWindow", "sun blind"))
        item = self.tableWidget.item(3, 1)
        item.setText(_translate("SubWindow", status[3]))
        item = self.tableWidget.item(3, 2)
        item.setText(_translate("SubWindow", "NA"))
        self.tableWidget.update()

    def update(self):
        self.update_graph()
        self.update_status()

    def check_if_module_is_connected(self):
        return units.Units.check_if_module_is_connected(self.unit)
