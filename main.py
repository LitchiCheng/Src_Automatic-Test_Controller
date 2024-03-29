import os,sys,time,socket,struct,barcode
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from barcode.writer import ImageWriter
from pystrich.code128 import Code128Encoder
import json
from ctypes import *

class Test_Items:
    def __init__(self):
        self.rs232 = 0x01
        self.rs485 = 0x02
        self.can = 0x03
        self.doOpen = 0x04
        self.doClose = 0x05
        self.bootLight = 0x06
        self.emcOpen = 0x07
        self.emcClose = 0x08
        self.chargeGround = 0x09
        self.chargeBrake = 0x0A
        self.brakeOpen = 0x0B
        self.brakeClose = 0x0C
        self.diBrake = 0x0D
        self.diGround = 0x0E
        self.delayBrake = 0x0F
        self.delayClose = 0x10
        self.openPC = 0x11
        self.closePC = 0x12
        self.warnLightOpen = 0x13
        self.warnLightClose = 0x14
        self.uidQuery = 0x15
        self.mainVersionQuery = 0x16
        self.gyroVersionQuery = 0x17
        self.noWork = 0xFF

class socketTool:
    def __init__(self, remote_ip ,local_port):
        self.remote_ip = remote_ip
        self.remote_port = 4822
        self.local_port = local_port
        self.local_ip = ''
        self.so = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # self.so.bind((self.local_ip, int(self.local_port)))
    
    def connect(self):
        pass
        # self.so = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # self.so.bind((self.local_ip, int(self.local_port)))

    def setRemoteIp(self, ip):
        self.remote_ip = ip
    
    def setLocalPort(self, port):
        self.local_port = port

    def sendTestCmd(self, index, timeout_t):
        print((self.remote_ip, self.remote_port))
        print("send index is " + str(index))
        self.so.sendto(struct.pack('>HB',0x1234,index),(self.remote_ip, self.remote_port))
        self.so.settimeout(timeout_t)

    def recvTestResult(self, index):
        ret = b''   
        try:
            ret,address= self.so.recvfrom(1024)
            print("接收到的" + str(address[0]))      
        except socket.timeout:
            ret = b''
        try:
            head, item_index, result = struct.unpack('>H2B',ret)
            print("recv is " + str(hex(head)) + " " + str(hex(item_index)))
        except:
            head = 0xFFFF   
        if head == 0x5678:
            if item_index == index and result == 0xFF:
                return True
            else:
                return False
        else:
            return False


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(504, 882)
        MainWindow.setMinimumSize(QtCore.QSize(0, 0))
        MainWindow.setMaximumSize(QtCore.QSize(6666, 6666))
        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setEnabled(True)
        self.tabWidget.setGeometry(QtCore.QRect(10, 230, 491, 631))
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.layoutWidget = QtWidgets.QWidget(self.tab_3)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 0, 461, 591))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout_6.setContentsMargins(5, 5, 5, 5)
        self.gridLayout_6.setSpacing(0)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.horizontalLayout_2.setContentsMargins(2, 2, 2, 2)
        self.horizontalLayout_2.setSpacing(2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.push_reset = QtWidgets.QPushButton(self.layoutWidget)
        self.push_reset.setMinimumSize(QtCore.QSize(0, 21))
        self.push_reset.setMaximumSize(QtCore.QSize(16777215, 21))
        self.push_reset.setObjectName("push_reset")
        self.horizontalLayout_2.addWidget(self.push_reset)
        self.gridLayout_6.addLayout(self.horizontalLayout_2, 1, 1, 1, 1)
        self.line_18 = QtWidgets.QFrame(self.layoutWidget)
        self.line_18.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_18.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_18.setObjectName("line_18")
        self.gridLayout_6.addWidget(self.line_18, 3, 1, 1, 1)
        self.line_20 = QtWidgets.QFrame(self.layoutWidget)
        self.line_20.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_20.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_20.setObjectName("line_20")
        self.gridLayout_6.addWidget(self.line_20, 1, 2, 1, 1)
        self.line_19 = QtWidgets.QFrame(self.layoutWidget)
        self.line_19.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_19.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_19.setObjectName("line_19")
        self.gridLayout_6.addWidget(self.line_19, 1, 0, 1, 1)
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setContentsMargins(2, 2, 2, 2)
        self.gridLayout_5.setSpacing(0)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setContentsMargins(2, 2, 2, 2)
        self.gridLayout_3.setSpacing(5)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.manual_test_push_rs232 = QtWidgets.QPushButton(self.layoutWidget)
        self.manual_test_push_rs232.setMinimumSize(QtCore.QSize(122, 21))
        self.manual_test_push_rs232.setMaximumSize(QtCore.QSize(16777215, 21))
        self.manual_test_push_rs232.setObjectName("manual_test_push_rs232")
        self.gridLayout_3.addWidget(self.manual_test_push_rs232, 0, 0, 1, 1)
        self.manual_test_push_485 = QtWidgets.QPushButton(self.layoutWidget)
        self.manual_test_push_485.setMinimumSize(QtCore.QSize(122, 21))
        self.manual_test_push_485.setMaximumSize(QtCore.QSize(16777215, 21))
        self.manual_test_push_485.setObjectName("manual_test_push_485")
        self.gridLayout_3.addWidget(self.manual_test_push_485, 1, 0, 1, 1)
        self.manual_test_push_can = QtWidgets.QPushButton(self.layoutWidget)
        self.manual_test_push_can.setMinimumSize(QtCore.QSize(122, 21))
        self.manual_test_push_can.setMaximumSize(QtCore.QSize(16777215, 21))
        self.manual_test_push_can.setObjectName("manual_test_push_can")
        self.gridLayout_3.addWidget(self.manual_test_push_can, 2, 0, 1, 1)
        self.manual_test_push_do_on = QtWidgets.QPushButton(self.layoutWidget)
        self.manual_test_push_do_on.setMinimumSize(QtCore.QSize(122, 21))
        self.manual_test_push_do_on.setMaximumSize(QtCore.QSize(16777215, 21))
        self.manual_test_push_do_on.setObjectName("manual_test_push_do_on")
        self.gridLayout_3.addWidget(self.manual_test_push_do_on, 3, 0, 1, 1)
        self.manual_test_push_do_off = QtWidgets.QPushButton(self.layoutWidget)
        self.manual_test_push_do_off.setMinimumSize(QtCore.QSize(122, 21))
        self.manual_test_push_do_off.setMaximumSize(QtCore.QSize(16777215, 21))
        self.manual_test_push_do_off.setObjectName("manual_test_push_do_off")
        self.gridLayout_3.addWidget(self.manual_test_push_do_off, 4, 0, 1, 1)
        self.manual_test_push_bootlight = QtWidgets.QPushButton(self.layoutWidget)
        self.manual_test_push_bootlight.setMinimumSize(QtCore.QSize(122, 21))
        self.manual_test_push_bootlight.setMaximumSize(QtCore.QSize(16777215, 21))
        self.manual_test_push_bootlight.setObjectName("manual_test_push_bootlight")
        self.gridLayout_3.addWidget(self.manual_test_push_bootlight, 5, 0, 1, 1)
        self.manual_test_push_emc_on = QtWidgets.QPushButton(self.layoutWidget)
        self.manual_test_push_emc_on.setMinimumSize(QtCore.QSize(122, 21))
        self.manual_test_push_emc_on.setMaximumSize(QtCore.QSize(16777215, 21))
        self.manual_test_push_emc_on.setObjectName("manual_test_push_emc_on")
        self.gridLayout_3.addWidget(self.manual_test_push_emc_on, 6, 0, 1, 1)
        self.manual_test_push_emc_off = QtWidgets.QPushButton(self.layoutWidget)
        self.manual_test_push_emc_off.setMinimumSize(QtCore.QSize(122, 21))
        self.manual_test_push_emc_off.setMaximumSize(QtCore.QSize(16777215, 21))
        self.manual_test_push_emc_off.setObjectName("manual_test_push_emc_off")
        self.gridLayout_3.addWidget(self.manual_test_push_emc_off, 7, 0, 1, 1)
        self.manual_test_push_charge_groud = QtWidgets.QPushButton(self.layoutWidget)
        self.manual_test_push_charge_groud.setMinimumSize(QtCore.QSize(122, 21))
        self.manual_test_push_charge_groud.setMaximumSize(QtCore.QSize(16777215, 21))
        self.manual_test_push_charge_groud.setObjectName("manual_test_push_charge_groud")
        self.gridLayout_3.addWidget(self.manual_test_push_charge_groud, 8, 0, 1, 1)
        self.manual_test_push_charge_brake = QtWidgets.QPushButton(self.layoutWidget)
        self.manual_test_push_charge_brake.setMinimumSize(QtCore.QSize(122, 21))
        self.manual_test_push_charge_brake.setMaximumSize(QtCore.QSize(16777215, 21))
        self.manual_test_push_charge_brake.setObjectName("manual_test_push_charge_brake")
        self.gridLayout_3.addWidget(self.manual_test_push_charge_brake, 9, 0, 1, 1)
        self.manual_test_push_brake_on = QtWidgets.QPushButton(self.layoutWidget)
        self.manual_test_push_brake_on.setMinimumSize(QtCore.QSize(122, 21))
        self.manual_test_push_brake_on.setMaximumSize(QtCore.QSize(16777215, 21))
        self.manual_test_push_brake_on.setObjectName("manual_test_push_brake_on")
        self.gridLayout_3.addWidget(self.manual_test_push_brake_on, 10, 0, 1, 1)
        self.manual_test_push_brake_off = QtWidgets.QPushButton(self.layoutWidget)
        self.manual_test_push_brake_off.setMinimumSize(QtCore.QSize(122, 21))
        self.manual_test_push_brake_off.setMaximumSize(QtCore.QSize(16777215, 21))
        self.manual_test_push_brake_off.setObjectName("manual_test_push_brake_off")
        self.gridLayout_3.addWidget(self.manual_test_push_brake_off, 11, 0, 1, 1)
        self.manual_test_push_di_brake = QtWidgets.QPushButton(self.layoutWidget)
        self.manual_test_push_di_brake.setMinimumSize(QtCore.QSize(122, 21))
        self.manual_test_push_di_brake.setMaximumSize(QtCore.QSize(16777215, 21))
        self.manual_test_push_di_brake.setObjectName("manual_test_push_di_brake")
        self.gridLayout_3.addWidget(self.manual_test_push_di_brake, 12, 0, 1, 1)
        self.manual_test_push_di_ground = QtWidgets.QPushButton(self.layoutWidget)
        self.manual_test_push_di_ground.setMinimumSize(QtCore.QSize(122, 21))
        self.manual_test_push_di_ground.setMaximumSize(QtCore.QSize(16777215, 21))
        self.manual_test_push_di_ground.setObjectName("manual_test_push_di_ground")
        self.gridLayout_3.addWidget(self.manual_test_push_di_ground, 13, 0, 1, 1)
        self.manual_test_push_delay_brake = QtWidgets.QPushButton(self.layoutWidget)
        self.manual_test_push_delay_brake.setMinimumSize(QtCore.QSize(122, 21))
        self.manual_test_push_delay_brake.setMaximumSize(QtCore.QSize(16777215, 21))
        self.manual_test_push_delay_brake.setObjectName("manual_test_push_delay_brake")
        self.gridLayout_3.addWidget(self.manual_test_push_delay_brake, 14, 0, 1, 1)
        self.manual_test_push_delay_on = QtWidgets.QPushButton(self.layoutWidget)
        self.manual_test_push_delay_on.setMinimumSize(QtCore.QSize(122, 21))
        self.manual_test_push_delay_on.setMaximumSize(QtCore.QSize(16777215, 21))
        self.manual_test_push_delay_on.setObjectName("manual_test_push_delay_on")
        self.gridLayout_3.addWidget(self.manual_test_push_delay_on, 15, 0, 1, 1)
        self.manual_test_push_warn_on = QtWidgets.QPushButton(self.layoutWidget)
        self.manual_test_push_warn_on.setMinimumSize(QtCore.QSize(122, 21))
        self.manual_test_push_warn_on.setMaximumSize(QtCore.QSize(16777215, 21))
        self.manual_test_push_warn_on.setObjectName("manual_test_push_warn_on")
        self.gridLayout_3.addWidget(self.manual_test_push_warn_on, 16, 0, 1, 1)
        self.manual_test_push_warn_off = QtWidgets.QPushButton(self.layoutWidget)
        self.manual_test_push_warn_off.setMinimumSize(QtCore.QSize(122, 21))
        self.manual_test_push_warn_off.setMaximumSize(QtCore.QSize(16777215, 21))
        self.manual_test_push_warn_off.setObjectName("manual_test_push_warn_off")
        self.gridLayout_3.addWidget(self.manual_test_push_warn_off, 17, 0, 1, 1)
        self.gridLayout_5.addLayout(self.gridLayout_3, 1, 0, 1, 1)
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setContentsMargins(2, 2, 2, 2)
        self.gridLayout_4.setSpacing(5)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.manual_label_state_rs232 = QtWidgets.QLabel(self.layoutWidget)
        self.manual_label_state_rs232.setMinimumSize(QtCore.QSize(21, 21))
        self.manual_label_state_rs232.setMaximumSize(QtCore.QSize(21, 21))
        self.manual_label_state_rs232.setText("")
        self.manual_label_state_rs232.setPixmap(QtGui.QPixmap("../x.png"))
        self.manual_label_state_rs232.setObjectName("manual_label_state_rs232")
        # self.manual_label_state_rs232.setVisible(False)
        self.gridLayout_4.addWidget(self.manual_label_state_rs232, 0, 0, 1, 1)
        self.manual_label_state_rs485 = QtWidgets.QLabel(self.layoutWidget)
        self.manual_label_state_rs485.setMinimumSize(QtCore.QSize(21, 21))
        self.manual_label_state_rs485.setMaximumSize(QtCore.QSize(21, 21))
        self.manual_label_state_rs485.setText("")
        self.manual_label_state_rs485.setPixmap(QtGui.QPixmap("../x.png"))
        self.manual_label_state_rs485.setObjectName("manual_label_state_rs485")
        self.gridLayout_4.addWidget(self.manual_label_state_rs485, 1, 0, 1, 1)
        self.manual_label_state_can = QtWidgets.QLabel(self.layoutWidget)
        self.manual_label_state_can.setMinimumSize(QtCore.QSize(21, 21))
        self.manual_label_state_can.setMaximumSize(QtCore.QSize(21, 21))
        self.manual_label_state_can.setText("")
        self.manual_label_state_can.setPixmap(QtGui.QPixmap("../x.png"))
        self.manual_label_state_can.setObjectName("manual_label_state_can")
        self.gridLayout_4.addWidget(self.manual_label_state_can, 2, 0, 1, 1)
        self.manual_label_state_do_on = QtWidgets.QLabel(self.layoutWidget)
        self.manual_label_state_do_on.setMinimumSize(QtCore.QSize(21, 21))
        self.manual_label_state_do_on.setMaximumSize(QtCore.QSize(21, 21))
        self.manual_label_state_do_on.setText("")
        self.manual_label_state_do_on.setPixmap(QtGui.QPixmap("../x.png"))
        self.manual_label_state_do_on.setObjectName("manual_label_state_do_on")
        self.gridLayout_4.addWidget(self.manual_label_state_do_on, 3, 0, 1, 1)
        self.manual_label_state_do_off = QtWidgets.QLabel(self.layoutWidget)
        self.manual_label_state_do_off.setMinimumSize(QtCore.QSize(21, 21))
        self.manual_label_state_do_off.setMaximumSize(QtCore.QSize(21, 21))
        self.manual_label_state_do_off.setText("")
        self.manual_label_state_do_off.setPixmap(QtGui.QPixmap("../x.png"))
        self.manual_label_state_do_off.setObjectName("manual_label_state_do_off")
        self.gridLayout_4.addWidget(self.manual_label_state_do_off, 4, 0, 1, 1)
        self.manual_label_state_bootlight = QtWidgets.QLabel(self.layoutWidget)
        self.manual_label_state_bootlight.setMinimumSize(QtCore.QSize(21, 21))
        self.manual_label_state_bootlight.setMaximumSize(QtCore.QSize(21, 21))
        self.manual_label_state_bootlight.setText("")
        self.manual_label_state_bootlight.setPixmap(QtGui.QPixmap("../x.png"))
        self.manual_label_state_bootlight.setObjectName("manual_label_state_bootlight")
        self.gridLayout_4.addWidget(self.manual_label_state_bootlight, 5, 0, 1, 1)
        self.manual_label_state_emc_on = QtWidgets.QLabel(self.layoutWidget)
        self.manual_label_state_emc_on.setMinimumSize(QtCore.QSize(21, 21))
        self.manual_label_state_emc_on.setMaximumSize(QtCore.QSize(21, 21))
        self.manual_label_state_emc_on.setText("")
        self.manual_label_state_emc_on.setPixmap(QtGui.QPixmap("../x.png"))
        self.manual_label_state_emc_on.setObjectName("manual_label_state_emc_on")
        self.gridLayout_4.addWidget(self.manual_label_state_emc_on, 6, 0, 1, 1)
        self.manual_label_state_emc_off = QtWidgets.QLabel(self.layoutWidget)
        self.manual_label_state_emc_off.setMinimumSize(QtCore.QSize(21, 21))
        self.manual_label_state_emc_off.setMaximumSize(QtCore.QSize(21, 21))
        self.manual_label_state_emc_off.setText("")
        self.manual_label_state_emc_off.setPixmap(QtGui.QPixmap("../x.png"))
        self.manual_label_state_emc_off.setObjectName("manual_label_state_emc_off")
        self.gridLayout_4.addWidget(self.manual_label_state_emc_off, 7, 0, 1, 1)
        self.manual_label_state_charge_ground = QtWidgets.QLabel(self.layoutWidget)
        self.manual_label_state_charge_ground.setMinimumSize(QtCore.QSize(21, 21))
        self.manual_label_state_charge_ground.setMaximumSize(QtCore.QSize(21, 21))
        self.manual_label_state_charge_ground.setText("")
        self.manual_label_state_charge_ground.setPixmap(QtGui.QPixmap("../x.png"))
        self.manual_label_state_charge_ground.setObjectName("manual_label_state_charge_ground")
        self.gridLayout_4.addWidget(self.manual_label_state_charge_ground, 8, 0, 1, 1)
        self.manual_label_state_charge_brake = QtWidgets.QLabel(self.layoutWidget)
        self.manual_label_state_charge_brake.setMinimumSize(QtCore.QSize(21, 21))
        self.manual_label_state_charge_brake.setMaximumSize(QtCore.QSize(21, 21))
        self.manual_label_state_charge_brake.setText("")
        self.manual_label_state_charge_brake.setTextFormat(QtCore.Qt.RichText)
        self.manual_label_state_charge_brake.setPixmap(QtGui.QPixmap("../x.png"))
        self.manual_label_state_charge_brake.setObjectName("manual_label_state_charge_brake")
        self.gridLayout_4.addWidget(self.manual_label_state_charge_brake, 9, 0, 1, 1)
        self.manual_label_state_brake_on = QtWidgets.QLabel(self.layoutWidget)
        self.manual_label_state_brake_on.setMinimumSize(QtCore.QSize(21, 21))
        self.manual_label_state_brake_on.setMaximumSize(QtCore.QSize(21, 21))
        self.manual_label_state_brake_on.setText("")
        self.manual_label_state_brake_on.setPixmap(QtGui.QPixmap("../x.png"))
        self.manual_label_state_brake_on.setObjectName("manual_label_state_brake_on")
        self.gridLayout_4.addWidget(self.manual_label_state_brake_on, 10, 0, 1, 1)
        self.manual_label_state_brake_off = QtWidgets.QLabel(self.layoutWidget)
        self.manual_label_state_brake_off.setMinimumSize(QtCore.QSize(21, 21))
        self.manual_label_state_brake_off.setMaximumSize(QtCore.QSize(21, 21))
        self.manual_label_state_brake_off.setText("")
        self.manual_label_state_brake_off.setPixmap(QtGui.QPixmap("../x.png"))
        self.manual_label_state_brake_off.setObjectName("manual_label_state_brake_off")
        self.gridLayout_4.addWidget(self.manual_label_state_brake_off, 11, 0, 1, 1)
        self.manual_label_state_di_off = QtWidgets.QLabel(self.layoutWidget)
        self.manual_label_state_di_off.setMinimumSize(QtCore.QSize(21, 21))
        self.manual_label_state_di_off.setMaximumSize(QtCore.QSize(21, 21))
        self.manual_label_state_di_off.setText("")
        self.manual_label_state_di_off.setPixmap(QtGui.QPixmap("../x.png"))
        self.manual_label_state_di_off.setObjectName("manual_label_state_di_off")
        self.gridLayout_4.addWidget(self.manual_label_state_di_off, 12, 0, 1, 1)
        self.manual_label_state_di_ground = QtWidgets.QLabel(self.layoutWidget)
        self.manual_label_state_di_ground.setMinimumSize(QtCore.QSize(21, 21))
        self.manual_label_state_di_ground.setMaximumSize(QtCore.QSize(21, 21))
        self.manual_label_state_di_ground.setText("")
        self.manual_label_state_di_ground.setPixmap(QtGui.QPixmap("../x.png"))
        self.manual_label_state_di_ground.setObjectName("manual_label_state_di_ground")
        self.gridLayout_4.addWidget(self.manual_label_state_di_ground, 13, 0, 1, 1)
        self.manual_label_state_delay_brake = QtWidgets.QLabel(self.layoutWidget)
        self.manual_label_state_delay_brake.setMinimumSize(QtCore.QSize(21, 21))
        self.manual_label_state_delay_brake.setMaximumSize(QtCore.QSize(21, 21))
        self.manual_label_state_delay_brake.setText("")
        self.manual_label_state_delay_brake.setPixmap(QtGui.QPixmap("../x.png"))
        self.manual_label_state_delay_brake.setObjectName("manual_label_state_delay_brake")
        self.gridLayout_4.addWidget(self.manual_label_state_delay_brake, 14, 0, 1, 1)
        self.manual_label_state_delay_on = QtWidgets.QLabel(self.layoutWidget)
        self.manual_label_state_delay_on.setMinimumSize(QtCore.QSize(21, 21))
        self.manual_label_state_delay_on.setMaximumSize(QtCore.QSize(21, 21))
        self.manual_label_state_delay_on.setText("")
        self.manual_label_state_delay_on.setPixmap(QtGui.QPixmap("../x.png"))
        self.manual_label_state_delay_on.setObjectName("manual_label_state_delay_on")
        self.gridLayout_4.addWidget(self.manual_label_state_delay_on, 15, 0, 1, 1)
        self.manual_label_state_warn_on = QtWidgets.QLabel(self.layoutWidget)
        self.manual_label_state_warn_on.setMinimumSize(QtCore.QSize(21, 21))
        self.manual_label_state_warn_on.setMaximumSize(QtCore.QSize(21, 21))
        self.manual_label_state_warn_on.setText("")
        self.manual_label_state_warn_on.setPixmap(QtGui.QPixmap("../x.png"))
        self.manual_label_state_warn_on.setObjectName("manual_label_state_warn_on")
        self.gridLayout_4.addWidget(self.manual_label_state_warn_on, 16, 0, 1, 1)
        self.manual_label_state_warn_off = QtWidgets.QLabel(self.layoutWidget)
        self.manual_label_state_warn_off.setMinimumSize(QtCore.QSize(21, 21))
        self.manual_label_state_warn_off.setMaximumSize(QtCore.QSize(21, 21))
        self.manual_label_state_warn_off.setText("")
        self.manual_label_state_warn_off.setPixmap(QtGui.QPixmap("../x.png"))
        self.manual_label_state_warn_off.setObjectName("manual_label_state_warn_off")
        self.gridLayout_4.addWidget(self.manual_label_state_warn_off, 17, 0, 1, 1)
        self.gridLayout_5.addLayout(self.gridLayout_4, 1, 1, 1, 1)
        self.line_17 = QtWidgets.QFrame(self.layoutWidget)
        self.line_17.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_17.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_17.setObjectName("line_17")
        self.gridLayout_5.addWidget(self.line_17, 0, 0, 1, 1)
        self.gridLayout_6.addLayout(self.gridLayout_5, 2, 1, 1, 1)
        self.line_15 = QtWidgets.QFrame(self.layoutWidget)
        self.line_15.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_15.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_15.setObjectName("line_15")
        self.gridLayout_6.addWidget(self.line_15, 2, 0, 1, 1)
        self.line_16 = QtWidgets.QFrame(self.layoutWidget)
        self.line_16.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_16.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_16.setObjectName("line_16")
        self.gridLayout_6.addWidget(self.line_16, 2, 2, 1, 1)
        self.line_21 = QtWidgets.QFrame(self.layoutWidget)
        self.line_21.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_21.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_21.setObjectName("line_21")
        self.gridLayout_6.addWidget(self.line_21, 0, 1, 1, 1)
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.layoutWidget1 = QtWidgets.QWidget(self.tab_4)
        self.layoutWidget1.setGeometry(QtCore.QRect(10, 0, 461, 596))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.gridLayout_11 = QtWidgets.QGridLayout(self.layoutWidget1)
        self.gridLayout_11.setContentsMargins(5, 5, 5, 5)
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.line_32 = QtWidgets.QFrame(self.layoutWidget1)
        self.line_32.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_32.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_32.setObjectName("line_32")
        self.gridLayout_11.addWidget(self.line_32, 9, 0, 1, 1)
        self.line_25 = QtWidgets.QFrame(self.layoutWidget1)
        self.line_25.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_25.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_25.setObjectName("line_25")
        self.gridLayout_11.addWidget(self.line_25, 5, 0, 1, 1)
        self.gridLayout_9 = QtWidgets.QGridLayout()
        self.gridLayout_9.setContentsMargins(5, 5, 5, 5)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_19 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_19.setMinimumSize(QtCore.QSize(0, 21))
        self.label_19.setMaximumSize(QtCore.QSize(16777215, 21))
        self.label_19.setObjectName("label_19")
        self.gridLayout.addWidget(self.label_19, 4, 0, 1, 1)
        self.label_37 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_37.setMinimumSize(QtCore.QSize(0, 21))
        self.label_37.setMaximumSize(QtCore.QSize(16777215, 21))
        self.label_37.setObjectName("label_37")
        self.gridLayout.addWidget(self.label_37, 7, 0, 1, 1)
        self.label_33 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_33.setMinimumSize(QtCore.QSize(0, 21))
        self.label_33.setMaximumSize(QtCore.QSize(16777215, 21))
        self.label_33.setObjectName("label_33")
        self.gridLayout.addWidget(self.label_33, 10, 0, 1, 1)
        self.label_29 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_29.setMinimumSize(QtCore.QSize(0, 21))
        self.label_29.setMaximumSize(QtCore.QSize(16777215, 21))
        self.label_29.setObjectName("label_29")
        # self.label_29.setVisible(False)
        self.gridLayout.addWidget(self.label_29, 12, 0, 1, 1)
        self.label_31 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_31.setMinimumSize(QtCore.QSize(0, 21))
        self.label_31.setMaximumSize(QtCore.QSize(16777215, 21))
        self.label_31.setObjectName("label_31")
        self.gridLayout.addWidget(self.label_31, 13, 0, 1, 1)
        self.label_21 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_21.setMinimumSize(QtCore.QSize(0, 21))
        self.label_21.setMaximumSize(QtCore.QSize(16777215, 21))
        self.label_21.setObjectName("label_21")
        self.gridLayout.addWidget(self.label_21, 5, 0, 1, 1)
        self.label_38 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_38.setMinimumSize(QtCore.QSize(0, 21))
        self.label_38.setMaximumSize(QtCore.QSize(16777215, 21))
        self.label_38.setObjectName("label_38")
        self.gridLayout.addWidget(self.label_38, 8, 0, 1, 1)
        self.label_59 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_59.setObjectName("label_59")
        self.gridLayout.addWidget(self.label_59, 0, 0, 1, 1)
        self.label_22 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_22.setMinimumSize(QtCore.QSize(0, 21))
        self.label_22.setMaximumSize(QtCore.QSize(16777215, 21))
        self.label_22.setObjectName("label_22")
        self.gridLayout.addWidget(self.label_22, 6, 0, 1, 1)
        self.label_23 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_23.setMinimumSize(QtCore.QSize(0, 21))
        self.label_23.setMaximumSize(QtCore.QSize(16777215, 21))
        self.label_23.setObjectName("label_23")
        self.gridLayout.addWidget(self.label_23, 9, 0, 1, 1)
        self.label_36 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_36.setMinimumSize(QtCore.QSize(0, 21))
        self.label_36.setMaximumSize(QtCore.QSize(16777215, 21))
        self.label_36.setObjectName("label_36")
        self.gridLayout.addWidget(self.label_36, 11, 0, 1, 1)
        self.label_32 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_32.setMinimumSize(QtCore.QSize(0, 21))
        self.label_32.setMaximumSize(QtCore.QSize(16777215, 21))
        self.label_32.setObjectName("label_32")
        self.gridLayout.addWidget(self.label_32, 15, 0, 1, 1)
        self.label_20 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_20.setMinimumSize(QtCore.QSize(0, 21))
        self.label_20.setMaximumSize(QtCore.QSize(16777215, 21))
        self.label_20.setObjectName("label_20")
        self.label_20.setVisible(False)
        self.gridLayout.addWidget(self.label_20, 3, 0, 1, 1)
        self.line_3 = QtWidgets.QFrame(self.layoutWidget1)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.gridLayout.addWidget(self.line_3, 1, 0, 1, 1)
        self.label_30 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_30.setMinimumSize(QtCore.QSize(0, 21))
        self.label_30.setMaximumSize(QtCore.QSize(16777215, 21))
        self.label_30.setObjectName("label_30")
        self.gridLayout.addWidget(self.label_30, 2, 0, 1, 1)
        self.gridLayout_9.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.line_4 = QtWidgets.QFrame(self.layoutWidget1)
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.gridLayout_9.addWidget(self.line_4, 0, 1, 1, 1)
        self.gridLayout_7 = QtWidgets.QGridLayout()
        self.gridLayout_7.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout_7.setHorizontalSpacing(0)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.auto_line_text_brake = QtWidgets.QLineEdit(self.layoutWidget1)
        self.auto_line_text_brake.setMinimumSize(QtCore.QSize(0, 21))
        self.auto_line_text_brake.setMaximumSize(QtCore.QSize(16777215, 21))
        self.auto_line_text_brake.setAlignment(QtCore.Qt.AlignCenter)
        self.auto_line_text_brake.setObjectName("auto_line_text_brake")
        self.gridLayout_7.addWidget(self.auto_line_text_brake, 10, 0, 1, 1)
        self.auto_line_text_bootlight = QtWidgets.QLineEdit(self.layoutWidget1)
        self.auto_line_text_bootlight.setMinimumSize(QtCore.QSize(0, 21))
        self.auto_line_text_bootlight.setMaximumSize(QtCore.QSize(16777215, 21))
        self.auto_line_text_bootlight.setAlignment(QtCore.Qt.AlignCenter)
        self.auto_line_text_bootlight.setObjectName("auto_line_text_bootlight")
        self.gridLayout_7.addWidget(self.auto_line_text_bootlight, 7, 0, 1, 1)
        self.auto_line_text_charge = QtWidgets.QLineEdit(self.layoutWidget1)
        self.auto_line_text_charge.setMinimumSize(QtCore.QSize(0, 21))
        self.auto_line_text_charge.setMaximumSize(QtCore.QSize(16777215, 21))
        self.auto_line_text_charge.setAlignment(QtCore.Qt.AlignCenter)
        self.auto_line_text_charge.setObjectName("auto_line_text_charge")
        self.gridLayout_7.addWidget(self.auto_line_text_charge, 9, 0, 1, 1)
        self.label_60 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_60.setObjectName("label_60")
        self.gridLayout_7.addWidget(self.label_60, 0, 0, 1, 1)
        self.auto_line_text_can = QtWidgets.QLineEdit(self.layoutWidget1)
        self.auto_line_text_can.setMinimumSize(QtCore.QSize(0, 21))
        self.auto_line_text_can.setMaximumSize(QtCore.QSize(16777215, 21))
        self.auto_line_text_can.setAlignment(QtCore.Qt.AlignCenter)
        self.auto_line_text_can.setObjectName("auto_line_text_can")
        self.gridLayout_7.addWidget(self.auto_line_text_can, 5, 0, 1, 1)
        self.auto_line_text_do = QtWidgets.QLineEdit(self.layoutWidget1)
        self.auto_line_text_do.setMinimumSize(QtCore.QSize(0, 21))
        self.auto_line_text_do.setMaximumSize(QtCore.QSize(16777215, 21))
        self.auto_line_text_do.setAlignment(QtCore.Qt.AlignCenter)
        self.auto_line_text_do.setObjectName("auto_line_text_do")
        self.gridLayout_7.addWidget(self.auto_line_text_do, 6, 0, 1, 1)
        self.auto_line_text_di = QtWidgets.QLineEdit(self.layoutWidget1)
        self.auto_line_text_di.setMinimumSize(QtCore.QSize(0, 21))
        self.auto_line_text_di.setMaximumSize(QtCore.QSize(16777215, 21))
        self.auto_line_text_di.setAlignment(QtCore.Qt.AlignCenter)
        self.auto_line_text_di.setObjectName("auto_line_text_di")
        self.gridLayout_7.addWidget(self.auto_line_text_di, 11, 0, 1, 1)
        self.auto_line_text_poweron = QtWidgets.QLineEdit(self.layoutWidget1)
        self.auto_line_text_poweron.setEnabled(True)
        self.auto_line_text_poweron.setMinimumSize(QtCore.QSize(0, 21))
        self.auto_line_text_poweron.setMaximumSize(QtCore.QSize(16777215, 21))
        self.auto_line_text_poweron.setAlignment(QtCore.Qt.AlignCenter)
        self.auto_line_text_poweron.setObjectName("auto_line_text_poweron")
        self.gridLayout_7.addWidget(self.auto_line_text_poweron, 2, 0, 1, 1)
        self.auto_line_text_rs485 = QtWidgets.QLineEdit(self.layoutWidget1)
        self.auto_line_text_rs485.setMinimumSize(QtCore.QSize(0, 21))
        self.auto_line_text_rs485.setMaximumSize(QtCore.QSize(16777215, 21))
        self.auto_line_text_rs485.setAlignment(QtCore.Qt.AlignCenter)
        self.auto_line_text_rs485.setObjectName("auto_line_text_rs485")
        self.gridLayout_7.addWidget(self.auto_line_text_rs485, 4, 0, 1, 1)
        self.line_2 = QtWidgets.QFrame(self.layoutWidget1)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout_7.addWidget(self.line_2, 1, 0, 1, 1)
        self.auto_line_text_poweroff = QtWidgets.QLineEdit(self.layoutWidget1)
        self.auto_line_text_poweroff.setEnabled(True)
        self.auto_line_text_poweroff.setMinimumSize(QtCore.QSize(0, 21))
        self.auto_line_text_poweroff.setMaximumSize(QtCore.QSize(16777215, 21))
        self.auto_line_text_poweroff.setAlignment(QtCore.Qt.AlignCenter)
        self.auto_line_text_poweroff.setObjectName("auto_line_text_poweroff")
        self.gridLayout_7.addWidget(self.auto_line_text_poweroff, 15, 0, 1, 1)
        self.auto_line_text_rs232 = QtWidgets.QLineEdit(self.layoutWidget1)
        self.auto_line_text_rs232.setEnabled(True)
        self.auto_line_text_rs232.setMinimumSize(QtCore.QSize(0, 21))
        self.auto_line_text_rs232.setMaximumSize(QtCore.QSize(16777215, 21))
        self.auto_line_text_rs232.setAlignment(QtCore.Qt.AlignCenter)
        self.auto_line_text_rs232.setReadOnly(False)
        self.auto_line_text_rs232.setObjectName("auto_line_text_rs232")
        self.auto_line_text_rs232.setVisible(False)
        self.gridLayout_7.addWidget(self.auto_line_text_rs232, 3, 0, 1, 1)
        self.auto_line_text_delay = QtWidgets.QLineEdit(self.layoutWidget1)
        self.auto_line_text_delay.setMinimumSize(QtCore.QSize(0, 21))
        self.auto_line_text_delay.setMaximumSize(QtCore.QSize(16777215, 21))
        self.auto_line_text_delay.setAlignment(QtCore.Qt.AlignCenter)
        self.auto_line_text_delay.setObjectName("auto_line_text_delay")
        # self.auto_line_text_delay.setVisible(False)
        self.gridLayout_7.addWidget(self.auto_line_text_delay, 12, 0, 1, 1)
        self.auto_line_text_warninglight = QtWidgets.QLineEdit(self.layoutWidget1)
        self.auto_line_text_warninglight.setMinimumSize(QtCore.QSize(0, 21))
        self.auto_line_text_warninglight.setMaximumSize(QtCore.QSize(16777215, 21))
        self.auto_line_text_warninglight.setAlignment(QtCore.Qt.AlignCenter)
        self.auto_line_text_warninglight.setObjectName("auto_line_text_warninglight")
        self.gridLayout_7.addWidget(self.auto_line_text_warninglight, 13, 0, 1, 1)
        self.auto_line_text_emc = QtWidgets.QLineEdit(self.layoutWidget1)
        self.auto_line_text_emc.setMinimumSize(QtCore.QSize(0, 21))
        self.auto_line_text_emc.setMaximumSize(QtCore.QSize(16777215, 21))
        self.auto_line_text_emc.setAlignment(QtCore.Qt.AlignCenter)
        self.auto_line_text_emc.setObjectName("auto_line_text_emc")
        self.gridLayout_7.addWidget(self.auto_line_text_emc, 8, 0, 1, 1)
        self.gridLayout_9.addLayout(self.gridLayout_7, 0, 2, 1, 1)
        self.line_5 = QtWidgets.QFrame(self.layoutWidget1)
        self.line_5.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.gridLayout_9.addWidget(self.line_5, 0, 3, 1, 1)
        self.gridLayout_8 = QtWidgets.QGridLayout()
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.line = QtWidgets.QFrame(self.layoutWidget1)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout_8.addWidget(self.line, 1, 0, 1, 1)
        self.auto_label_brake_state = QtWidgets.QLabel(self.layoutWidget1)
        self.auto_label_brake_state.setMinimumSize(QtCore.QSize(21, 21))
        self.auto_label_brake_state.setMaximumSize(QtCore.QSize(21, 21))
        self.auto_label_brake_state.setText("")
        self.auto_label_brake_state.setPixmap(QtGui.QPixmap("../x.png"))
        self.auto_label_brake_state.setObjectName("auto_label_brake_state")
        self.gridLayout_8.addWidget(self.auto_label_brake_state, 10, 0, 1, 1)
        self.auto_label_do_state = QtWidgets.QLabel(self.layoutWidget1)
        self.auto_label_do_state.setMinimumSize(QtCore.QSize(21, 21))
        self.auto_label_do_state.setMaximumSize(QtCore.QSize(21, 21))
        self.auto_label_do_state.setText("")
        self.auto_label_do_state.setPixmap(QtGui.QPixmap("../x.png"))
        self.auto_label_do_state.setObjectName("auto_label_do_state")
        self.gridLayout_8.addWidget(self.auto_label_do_state, 6, 0, 1, 1)
        self.auto_label_bootlight_state = QtWidgets.QLabel(self.layoutWidget1)
        self.auto_label_bootlight_state.setMinimumSize(QtCore.QSize(21, 21))
        self.auto_label_bootlight_state.setMaximumSize(QtCore.QSize(21, 21))
        self.auto_label_bootlight_state.setText("")
        self.auto_label_bootlight_state.setPixmap(QtGui.QPixmap("../x.png"))
        self.auto_label_bootlight_state.setObjectName("auto_label_bootlight_state")
        self.gridLayout_8.addWidget(self.auto_label_bootlight_state, 7, 0, 1, 1)
        self.auto_label_delay_state = QtWidgets.QLabel(self.layoutWidget1)
        self.auto_label_delay_state.setMinimumSize(QtCore.QSize(21, 21))
        self.auto_label_delay_state.setMaximumSize(QtCore.QSize(21, 21))
        self.auto_label_delay_state.setText("")
        self.auto_label_delay_state.setPixmap(QtGui.QPixmap("../x.png"))
        self.auto_label_delay_state.setObjectName("auto_label_delay_state")
        # self.auto_label_delay_state.setVisible(False)
        self.gridLayout_8.addWidget(self.auto_label_delay_state, 12, 0, 1, 1)
        self.auto_label_can_state = QtWidgets.QLabel(self.layoutWidget1)
        self.auto_label_can_state.setMinimumSize(QtCore.QSize(21, 21))
        self.auto_label_can_state.setMaximumSize(QtCore.QSize(21, 21))
        self.auto_label_can_state.setText("")
        self.auto_label_can_state.setPixmap(QtGui.QPixmap("../x.png"))
        self.auto_label_can_state.setObjectName("auto_label_can_state")
        self.gridLayout_8.addWidget(self.auto_label_can_state, 5, 0, 1, 1)
        self.auto_label_rs232_state = QtWidgets.QLabel(self.layoutWidget1)
        self.auto_label_rs232_state.setMinimumSize(QtCore.QSize(21, 21))
        self.auto_label_rs232_state.setMaximumSize(QtCore.QSize(21, 21))
        self.auto_label_rs232_state.setText("")
        self.auto_label_rs232_state.setPixmap(QtGui.QPixmap("../x.png"))
        self.auto_label_rs232_state.setObjectName("auto_label_rs232_state")
        self.auto_label_rs232_state.setVisible(False)
        self.gridLayout_8.addWidget(self.auto_label_rs232_state, 3, 0, 1, 1)
        self.auto_label_poweroff_state = QtWidgets.QLabel(self.layoutWidget1)
        self.auto_label_poweroff_state.setMinimumSize(QtCore.QSize(21, 21))
        self.auto_label_poweroff_state.setMaximumSize(QtCore.QSize(21, 21))
        self.auto_label_poweroff_state.setText("")
        self.auto_label_poweroff_state.setObjectName("auto_label_poweroff_state")
        self.gridLayout_8.addWidget(self.auto_label_poweroff_state, 15, 0, 1, 1)
        self.auto_label_rs485_state = QtWidgets.QLabel(self.layoutWidget1)
        self.auto_label_rs485_state.setMinimumSize(QtCore.QSize(21, 21))
        self.auto_label_rs485_state.setMaximumSize(QtCore.QSize(21, 21))
        self.auto_label_rs485_state.setText("")
        self.auto_label_rs485_state.setPixmap(QtGui.QPixmap("../x.png"))
        self.auto_label_rs485_state.setObjectName("auto_label_rs485_state")
        self.gridLayout_8.addWidget(self.auto_label_rs485_state, 4, 0, 1, 1)
        self.auto_label_warninglight_state = QtWidgets.QLabel(self.layoutWidget1)
        self.auto_label_warninglight_state.setMinimumSize(QtCore.QSize(21, 21))
        self.auto_label_warninglight_state.setMaximumSize(QtCore.QSize(21, 21))
        self.auto_label_warninglight_state.setText("")
        self.auto_label_warninglight_state.setPixmap(QtGui.QPixmap("../x.png"))
        self.auto_label_warninglight_state.setObjectName("auto_label_warninglight_state")
        self.gridLayout_8.addWidget(self.auto_label_warninglight_state, 13, 0, 1, 1)
        self.auto_label_di_state = QtWidgets.QLabel(self.layoutWidget1)
        self.auto_label_di_state.setMinimumSize(QtCore.QSize(21, 21))
        self.auto_label_di_state.setMaximumSize(QtCore.QSize(21, 21))
        self.auto_label_di_state.setText("")
        self.auto_label_di_state.setPixmap(QtGui.QPixmap("../x.png"))
        self.auto_label_di_state.setObjectName("auto_label_di_state")
        self.gridLayout_8.addWidget(self.auto_label_di_state, 11, 0, 1, 1)
        self.auto_label_charge_state = QtWidgets.QLabel(self.layoutWidget1)
        self.auto_label_charge_state.setMinimumSize(QtCore.QSize(21, 21))
        self.auto_label_charge_state.setMaximumSize(QtCore.QSize(21, 21))
        self.auto_label_charge_state.setText("")
        self.auto_label_charge_state.setPixmap(QtGui.QPixmap("../x.png"))
        self.auto_label_charge_state.setObjectName("auto_label_charge_state")
        self.gridLayout_8.addWidget(self.auto_label_charge_state, 9, 0, 1, 1)
        self.auto_label_emc_state = QtWidgets.QLabel(self.layoutWidget1)
        self.auto_label_emc_state.setMinimumSize(QtCore.QSize(21, 21))
        self.auto_label_emc_state.setMaximumSize(QtCore.QSize(21, 21))
        self.auto_label_emc_state.setText("")
        self.auto_label_emc_state.setPixmap(QtGui.QPixmap("../x.png"))
        self.auto_label_emc_state.setObjectName("auto_label_emc_state")
        self.gridLayout_8.addWidget(self.auto_label_emc_state, 8, 0, 1, 1)
        self.label_61 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_61.setObjectName("label_61")
        self.gridLayout_8.addWidget(self.label_61, 0, 0, 1, 1)
        self.auto_label_poweron_state = QtWidgets.QLabel(self.layoutWidget1)
        self.auto_label_poweron_state.setMinimumSize(QtCore.QSize(21, 21))
        self.auto_label_poweron_state.setMaximumSize(QtCore.QSize(21, 21))
        self.auto_label_poweron_state.setText("")
        self.auto_label_poweron_state.setObjectName("auto_label_poweron_state")
        self.gridLayout_8.addWidget(self.auto_label_poweron_state, 2, 0, 1, 1)
        self.gridLayout_9.addLayout(self.gridLayout_8, 0, 5, 1, 1)
        self.gridLayout_17 = QtWidgets.QGridLayout()
        self.gridLayout_17.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout_17.setHorizontalSpacing(0)
        self.gridLayout_17.setObjectName("gridLayout_17")
        self.auto_line_text_warninglight_timeout = QtWidgets.QLineEdit(self.layoutWidget1)
        self.auto_line_text_warninglight_timeout.setMinimumSize(QtCore.QSize(0, 21))
        self.auto_line_text_warninglight_timeout.setMaximumSize(QtCore.QSize(16777215, 21))
        self.auto_line_text_warninglight_timeout.setAlignment(QtCore.Qt.AlignCenter)
        self.auto_line_text_warninglight_timeout.setObjectName("auto_line_text_warninglight_timeout")
        self.gridLayout_17.addWidget(self.auto_line_text_warninglight_timeout, 13, 0, 1, 1)
        self.auto_line_text_rs485_timeout = QtWidgets.QLineEdit(self.layoutWidget1)
        self.auto_line_text_rs485_timeout.setMinimumSize(QtCore.QSize(0, 21))
        self.auto_line_text_rs485_timeout.setMaximumSize(QtCore.QSize(16777215, 21))
        self.auto_line_text_rs485_timeout.setAlignment(QtCore.Qt.AlignCenter)
        self.auto_line_text_rs485_timeout.setObjectName("auto_line_text_rs485_timeout")
        self.gridLayout_17.addWidget(self.auto_line_text_rs485_timeout, 4, 0, 1, 1)
        self.auto_line_text_brake_timeout = QtWidgets.QLineEdit(self.layoutWidget1)
        self.auto_line_text_brake_timeout.setMinimumSize(QtCore.QSize(0, 21))
        self.auto_line_text_brake_timeout.setMaximumSize(QtCore.QSize(16777215, 21))
        self.auto_line_text_brake_timeout.setAlignment(QtCore.Qt.AlignCenter)
        self.auto_line_text_brake_timeout.setObjectName("auto_line_text_brake_timeout")
        self.gridLayout_17.addWidget(self.auto_line_text_brake_timeout, 10, 0, 1, 1)
        self.auto_line_text_delay_timeout = QtWidgets.QLineEdit(self.layoutWidget1)
        self.auto_line_text_delay_timeout.setMinimumSize(QtCore.QSize(0, 21))
        self.auto_line_text_delay_timeout.setMaximumSize(QtCore.QSize(16777215, 21))
        self.auto_line_text_delay_timeout.setAlignment(QtCore.Qt.AlignCenter)
        self.auto_line_text_delay_timeout.setObjectName("auto_line_text_delay_timeout")
        # self.auto_line_text_delay_timeout.setVisible(False)
        self.gridLayout_17.addWidget(self.auto_line_text_delay_timeout, 12, 0, 1, 1)
        self.auto_line_text_can_timeout = QtWidgets.QLineEdit(self.layoutWidget1)
        self.auto_line_text_can_timeout.setMinimumSize(QtCore.QSize(0, 21))
        self.auto_line_text_can_timeout.setMaximumSize(QtCore.QSize(16777215, 21))
        self.auto_line_text_can_timeout.setAlignment(QtCore.Qt.AlignCenter)
        self.auto_line_text_can_timeout.setObjectName("auto_line_text_can_timeout")
        self.gridLayout_17.addWidget(self.auto_line_text_can_timeout, 5, 0, 1, 1)
        self.auto_line_text_do_timeout = QtWidgets.QLineEdit(self.layoutWidget1)
        self.auto_line_text_do_timeout.setMinimumSize(QtCore.QSize(0, 21))
        self.auto_line_text_do_timeout.setMaximumSize(QtCore.QSize(16777215, 21))
        self.auto_line_text_do_timeout.setAlignment(QtCore.Qt.AlignCenter)
        self.auto_line_text_do_timeout.setObjectName("auto_line_text_do_timeout")
        self.gridLayout_17.addWidget(self.auto_line_text_do_timeout, 6, 0, 1, 1)
        self.auto_line_text_poweroff_timeout = QtWidgets.QLineEdit(self.layoutWidget1)
        self.auto_line_text_poweroff_timeout.setEnabled(True)
        self.auto_line_text_poweroff_timeout.setMinimumSize(QtCore.QSize(0, 21))
        self.auto_line_text_poweroff_timeout.setMaximumSize(QtCore.QSize(16777215, 21))
        self.auto_line_text_poweroff_timeout.setAlignment(QtCore.Qt.AlignCenter)
        self.auto_line_text_poweroff_timeout.setObjectName("auto_line_text_poweroff_timeout")
        self.gridLayout_17.addWidget(self.auto_line_text_poweroff_timeout, 15, 0, 1, 1)
        self.auto_line_text_charge_timeout = QtWidgets.QLineEdit(self.layoutWidget1)
        self.auto_line_text_charge_timeout.setMinimumSize(QtCore.QSize(0, 21))
        self.auto_line_text_charge_timeout.setMaximumSize(QtCore.QSize(16777215, 21))
        self.auto_line_text_charge_timeout.setAlignment(QtCore.Qt.AlignCenter)
        self.auto_line_text_charge_timeout.setObjectName("auto_line_text_charge_timeout")
        self.gridLayout_17.addWidget(self.auto_line_text_charge_timeout, 9, 0, 1, 1)
        self.auto_line_text_emc_timeout = QtWidgets.QLineEdit(self.layoutWidget1)
        self.auto_line_text_emc_timeout.setMinimumSize(QtCore.QSize(0, 21))
        self.auto_line_text_emc_timeout.setMaximumSize(QtCore.QSize(16777215, 21))
        self.auto_line_text_emc_timeout.setAlignment(QtCore.Qt.AlignCenter)
        self.auto_line_text_emc_timeout.setObjectName("auto_line_text_emc_timeout")
        self.gridLayout_17.addWidget(self.auto_line_text_emc_timeout, 8, 0, 1, 1)
        self.line_6 = QtWidgets.QFrame(self.layoutWidget1)
        self.line_6.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.gridLayout_17.addWidget(self.line_6, 1, 0, 1, 1)
        self.auto_line_text_rs232_timeout = QtWidgets.QLineEdit(self.layoutWidget1)
        self.auto_line_text_rs232_timeout.setEnabled(True)
        self.auto_line_text_rs232_timeout.setMinimumSize(QtCore.QSize(0, 21))
        self.auto_line_text_rs232_timeout.setMaximumSize(QtCore.QSize(16777215, 21))
        self.auto_line_text_rs232_timeout.setAlignment(QtCore.Qt.AlignCenter)
        self.auto_line_text_rs232_timeout.setReadOnly(False)
        self.auto_line_text_rs232_timeout.setObjectName("auto_line_text_rs232_timeout")
        self.auto_line_text_rs232_timeout.setVisible(False)
        self.gridLayout_17.addWidget(self.auto_line_text_rs232_timeout, 3, 0, 1, 1)
        self.auto_line_text_poweron_timeout = QtWidgets.QLineEdit(self.layoutWidget1)
        self.auto_line_text_poweron_timeout.setEnabled(True)
        self.auto_line_text_poweron_timeout.setMinimumSize(QtCore.QSize(0, 21))
        self.auto_line_text_poweron_timeout.setMaximumSize(QtCore.QSize(16777215, 21))
        self.auto_line_text_poweron_timeout.setAlignment(QtCore.Qt.AlignCenter)
        self.auto_line_text_poweron_timeout.setObjectName("auto_line_text_poweron_timeout")
        self.gridLayout_17.addWidget(self.auto_line_text_poweron_timeout, 2, 0, 1, 1)
        self.auto_line_text_bootlight_timeout = QtWidgets.QLineEdit(self.layoutWidget1)
        self.auto_line_text_bootlight_timeout.setMinimumSize(QtCore.QSize(0, 21))
        self.auto_line_text_bootlight_timeout.setMaximumSize(QtCore.QSize(16777215, 21))
        self.auto_line_text_bootlight_timeout.setAlignment(QtCore.Qt.AlignCenter)
        self.auto_line_text_bootlight_timeout.setObjectName("auto_line_text_bootlight_timeout")
        self.gridLayout_17.addWidget(self.auto_line_text_bootlight_timeout, 7, 0, 1, 1)
        self.auto_line_text_di_timeout = QtWidgets.QLineEdit(self.layoutWidget1)
        self.auto_line_text_di_timeout.setMinimumSize(QtCore.QSize(0, 21))
        self.auto_line_text_di_timeout.setMaximumSize(QtCore.QSize(16777215, 21))
        self.auto_line_text_di_timeout.setAlignment(QtCore.Qt.AlignCenter)
        self.auto_line_text_di_timeout.setObjectName("auto_line_text_di_timeout")
        self.gridLayout_17.addWidget(self.auto_line_text_di_timeout, 11, 0, 1, 1)
        self.label_62 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_62.setObjectName("label_62")
        self.gridLayout_17.addWidget(self.label_62, 0, 0, 1, 1)
        self.gridLayout_9.addLayout(self.gridLayout_17, 0, 4, 1, 1)
        self.gridLayout_11.addLayout(self.gridLayout_9, 1, 1, 1, 1)
        self.auto_push_button_report = QtWidgets.QPushButton(self.layoutWidget1)
        self.auto_push_button_report.setMinimumSize(QtCore.QSize(0, 21))
        self.auto_push_button_report.setMaximumSize(QtCore.QSize(16777215, 21))
        self.auto_push_button_report.setObjectName("auto_push_button_report")
        self.gridLayout_11.addWidget(self.auto_push_button_report, 7, 1, 1, 1)
        self.line_23 = QtWidgets.QFrame(self.layoutWidget1)
        self.line_23.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_23.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_23.setObjectName("line_23")
        self.gridLayout_11.addWidget(self.line_23, 3, 0, 1, 1)
        self.line_29 = QtWidgets.QFrame(self.layoutWidget1)
        self.line_29.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_29.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_29.setObjectName("line_29")
        self.gridLayout_11.addWidget(self.line_29, 5, 2, 1, 1)
        self.line_27 = QtWidgets.QFrame(self.layoutWidget1)
        self.line_27.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_27.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_27.setObjectName("line_27")
        self.gridLayout_11.addWidget(self.line_27, 3, 2, 1, 1)
        self.line_13 = QtWidgets.QFrame(self.layoutWidget1)
        self.line_13.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_13.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_13.setObjectName("line_13")
        self.gridLayout_11.addWidget(self.line_13, 2, 1, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(0, 0, 0, -1)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.auto_push_button_test = QtWidgets.QPushButton(self.layoutWidget1)
        self.auto_push_button_test.setMinimumSize(QtCore.QSize(0, 21))
        self.auto_push_button_test.setMaximumSize(QtCore.QSize(16777215, 21))
        self.auto_push_button_test.setObjectName("auto_push_button_test")
        self.horizontalLayout.addWidget(self.auto_push_button_test)
        self.auto_push_button_pause = QtWidgets.QPushButton(self.layoutWidget1)
        self.auto_push_button_pause.setMinimumSize(QtCore.QSize(0, 21))
        self.auto_push_button_pause.setMaximumSize(QtCore.QSize(16777215, 21))
        self.auto_push_button_pause.setObjectName("auto_push_button_pause")
        self.horizontalLayout.addWidget(self.auto_push_button_pause)
        self.gridLayout_11.addLayout(self.horizontalLayout, 5, 1, 1, 1)
        self.line_11 = QtWidgets.QFrame(self.layoutWidget1)
        self.line_11.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_11.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_11.setObjectName("line_11")
        self.gridLayout_11.addWidget(self.line_11, 1, 0, 1, 1)
        self.line_12 = QtWidgets.QFrame(self.layoutWidget1)
        self.line_12.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_12.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_12.setObjectName("line_12")
        self.gridLayout_11.addWidget(self.line_12, 1, 2, 1, 1)
        self.label_69 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_69.setMinimumSize(QtCore.QSize(0, 21))
        self.label_69.setMaximumSize(QtCore.QSize(16777215, 21))
        self.label_69.setObjectName("label_69")
        self.gridLayout_11.addWidget(self.label_69, 3, 1, 1, 1)
        self.line_28 = QtWidgets.QFrame(self.layoutWidget1)
        self.line_28.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_28.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_28.setObjectName("line_28")
        self.gridLayout_11.addWidget(self.line_28, 4, 2, 1, 1)
        self.line_24 = QtWidgets.QFrame(self.layoutWidget1)
        self.line_24.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_24.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_24.setObjectName("line_24")
        self.gridLayout_11.addWidget(self.line_24, 4, 0, 1, 1)
        self.line_30 = QtWidgets.QFrame(self.layoutWidget1)
        self.line_30.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_30.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_30.setObjectName("line_30")
        self.gridLayout_11.addWidget(self.line_30, 7, 2, 1, 1)
        self.line_14 = QtWidgets.QFrame(self.layoutWidget1)
        self.line_14.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_14.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_14.setObjectName("line_14")
        self.gridLayout_11.addWidget(self.line_14, 0, 1, 1, 1)
        self.line_33 = QtWidgets.QFrame(self.layoutWidget1)
        self.line_33.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_33.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_33.setObjectName("line_33")
        self.gridLayout_11.addWidget(self.line_33, 9, 2, 1, 1)
        self.progressBar = QtWidgets.QProgressBar(self.layoutWidget1)
        self.progressBar.setMinimumSize(QtCore.QSize(0, 21))
        self.progressBar.setMaximumSize(QtCore.QSize(16777215, 21))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout_11.addWidget(self.progressBar, 9, 1, 1, 1)
        self.auto_line_text_total = QtWidgets.QLineEdit(self.layoutWidget1)
        self.auto_line_text_total.setMinimumSize(QtCore.QSize(0, 21))
        self.auto_line_text_total.setMaximumSize(QtCore.QSize(16777215, 21))
        self.auto_line_text_total.setAlignment(QtCore.Qt.AlignCenter)
        self.auto_line_text_total.setObjectName("auto_line_text_total")
        self.gridLayout_11.addWidget(self.auto_line_text_total, 4, 1, 1, 1)
        self.line_34 = QtWidgets.QFrame(self.layoutWidget1)
        self.line_34.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_34.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_34.setObjectName("line_34")
        self.gridLayout_11.addWidget(self.line_34, 10, 1, 1, 1)
        self.line_22 = QtWidgets.QFrame(self.layoutWidget1)
        self.line_22.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_22.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_22.setObjectName("line_22")
        self.gridLayout_11.addWidget(self.line_22, 8, 1, 1, 1)
        self.line_26 = QtWidgets.QFrame(self.layoutWidget1)
        self.line_26.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_26.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_26.setObjectName("line_26")
        self.gridLayout_11.addWidget(self.line_26, 7, 0, 1, 1)
        self.line_31 = QtWidgets.QFrame(self.layoutWidget1)
        self.line_31.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_31.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_31.setObjectName("line_31")
        self.gridLayout_11.addWidget(self.line_31, 8, 0, 1, 1)
        self.auto_line_text_pass_percent = QtWidgets.QLineEdit(self.layoutWidget1)
        self.auto_line_text_pass_percent.setMinimumSize(QtCore.QSize(0, 21))
        self.auto_line_text_pass_percent.setMaximumSize(QtCore.QSize(16777215, 21))
        self.auto_line_text_pass_percent.setAlignment(QtCore.Qt.AlignCenter)
        self.auto_line_text_pass_percent.setObjectName("auto_line_text_pass_percent")
        self.gridLayout_11.addWidget(self.auto_line_text_pass_percent, 6, 1, 1, 1)
        self.atuo_label_rs232_state_3 = QtWidgets.QLabel(self.tab_4)
        self.atuo_label_rs232_state_3.setGeometry(QtCore.QRect(220, 230, 21, 21))
        self.atuo_label_rs232_state_3.setMinimumSize(QtCore.QSize(21, 21))
        self.atuo_label_rs232_state_3.setMaximumSize(QtCore.QSize(21, 21))
        self.atuo_label_rs232_state_3.setText("")
        self.atuo_label_rs232_state_3.setPixmap(QtGui.QPixmap("../x.png"))
        self.atuo_label_rs232_state_3.setObjectName("atuo_label_rs232_state_3")
        self.tabWidget.addTab(self.tab_4, "")
        self.tab_7 = QtWidgets.QWidget()
        self.tab_7.setObjectName("tab_7")
        self.textBrowser = QtWidgets.QTextBrowser(self.tab_7)
        self.textBrowser.setGeometry(QtCore.QRect(10, 10, 471, 521))
        self.textBrowser.setObjectName("textBrowser")
        self.tabWidget.addTab(self.tab_7, "")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 231, 211))
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_13 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_13.setObjectName("gridLayout_13")
        self.gridLayout_12 = QtWidgets.QGridLayout()
        self.gridLayout_12.setContentsMargins(5, 5, 5, 5)
        self.gridLayout_12.setSpacing(2)
        self.gridLayout_12.setObjectName("gridLayout_12")
        self.gridLayout_10 = QtWidgets.QGridLayout()
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_70 = QtWidgets.QLabel(self.groupBox)
        self.label_70.setMinimumSize(QtCore.QSize(0, 21))
        self.label_70.setMaximumSize(QtCore.QSize(16777215, 21))
        self.label_70.setObjectName("label_70")
        self.verticalLayout.addWidget(self.label_70)
        self.label_71 = QtWidgets.QLabel(self.groupBox)
        self.label_71.setMinimumSize(QtCore.QSize(0, 21))
        self.label_71.setMaximumSize(QtCore.QSize(16777215, 21))
        self.label_71.setObjectName("label_71")
        self.verticalLayout.addWidget(self.label_71)
        self.gridLayout_10.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.line_ip = QtWidgets.QLineEdit(self.groupBox)
        self.line_ip.setMinimumSize(QtCore.QSize(0, 21))
        self.line_ip.setMaximumSize(QtCore.QSize(16777215, 21))
        self.line_ip.setObjectName("line_ip")
        self.verticalLayout_2.addWidget(self.line_ip)
        self.line_port = QtWidgets.QLineEdit(self.groupBox)
        self.line_port.setMinimumSize(QtCore.QSize(0, 21))
        self.line_port.setMaximumSize(QtCore.QSize(16777215, 21))
        self.line_port.setObjectName("line_port")
        self.verticalLayout_2.addWidget(self.line_port)
        self.gridLayout_10.addLayout(self.verticalLayout_2, 0, 1, 1, 1)
        self.gridLayout_12.addLayout(self.gridLayout_10, 0, 0, 1, 1)
        self.manual_test_push_openpc = QtWidgets.QPushButton(self.groupBox)
        self.manual_test_push_openpc.setObjectName("manual_test_push_openpc")
        self.gridLayout_12.addWidget(self.manual_test_push_openpc, 2, 0, 1, 1)
        self.manual_test_push_closepc = QtWidgets.QPushButton(self.groupBox)
        self.manual_test_push_closepc.setObjectName("manual_test_push_closepc")
        self.gridLayout_12.addWidget(self.manual_test_push_closepc, 3, 0, 1, 1)
        self.manual_print_barcode= QtWidgets.QPushButton(self.groupBox)
        self.manual_print_barcode.setObjectName("manual_print_barcode")
        self.gridLayout_12.addWidget(self.manual_print_barcode, 4, 0, 1, 1)

        self.push_connect = QtWidgets.QPushButton(self.groupBox)
        self.push_connect.setMinimumSize(QtCore.QSize(0, 21))
        self.push_connect.setMaximumSize(QtCore.QSize(16777215, 21))
        self.push_connect.setObjectName("push_connect")
        self.gridLayout_12.addWidget(self.push_connect, 1, 0, 1, 1)
        self.gridLayout_13.addLayout(self.gridLayout_12, 0, 0, 1, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(240, 10, 251, 211))
        self.groupBox_2.setObjectName("groupBox_2")
        self.layoutWidget2 = QtWidgets.QWidget(self.groupBox_2)
        self.layoutWidget2.setGeometry(QtCore.QRect(10, 10, 231, 99))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.gridLayout_16 = QtWidgets.QGridLayout(self.layoutWidget2)
        self.gridLayout_16.setContentsMargins(2, 2, 2, 2)
        self.gridLayout_16.setObjectName("gridLayout_16")
        self.gridLayout_15 = QtWidgets.QGridLayout()
        self.gridLayout_15.setObjectName("gridLayout_15")
        self.label_74 = QtWidgets.QLabel(self.layoutWidget2)
        self.label_74.setMinimumSize(QtCore.QSize(0, 21))
        self.label_74.setMaximumSize(QtCore.QSize(16777215, 21))
        self.label_74.setObjectName("label_74")
        self.gridLayout_15.addWidget(self.label_74, 0, 0, 1, 1)
        self.label_73 = QtWidgets.QLabel(self.layoutWidget2)
        self.label_73.setMinimumSize(QtCore.QSize(0, 21))
        self.label_73.setMaximumSize(QtCore.QSize(16777215, 21))
        self.label_73.setObjectName("label_73")
        self.gridLayout_15.addWidget(self.label_73, 1, 0, 1, 1)
        self.label_75 = QtWidgets.QLabel(self.layoutWidget2)
        self.label_75.setMinimumSize(QtCore.QSize(0, 21))
        self.label_75.setMaximumSize(QtCore.QSize(16777215, 21))
        self.label_75.setObjectName("label_75")
        self.gridLayout_15.addWidget(self.label_75, 2, 0, 1, 1)
        self.gridLayout_16.addLayout(self.gridLayout_15, 1, 1, 1, 1)
        self.gridLayout_14 = QtWidgets.QGridLayout()
        self.gridLayout_14.setObjectName("gridLayout_14")
        self.gyroversion_label = QtWidgets.QLabel(self.layoutWidget2)
        self.gyroversion_label.setMinimumSize(QtCore.QSize(0, 21))
        self.gyroversion_label.setMaximumSize(QtCore.QSize(16777215, 21))
        self.gyroversion_label.setObjectName("gyroversion_label")
        self.gridLayout_14.addWidget(self.gyroversion_label, 1, 0, 1, 1)
        self.uid_label = QtWidgets.QLabel(self.layoutWidget2)
        self.uid_label.setMinimumSize(QtCore.QSize(0, 21))
        self.uid_label.setMaximumSize(QtCore.QSize(16777215, 21))
        self.uid_label.setObjectName("uid_label")
        self.gridLayout_14.addWidget(self.uid_label, 2, 0, 1, 1)
        self.mainversion_label = QtWidgets.QLabel(self.layoutWidget2)
        self.mainversion_label.setMinimumSize(QtCore.QSize(0, 21))
        self.mainversion_label.setMaximumSize(QtCore.QSize(16777215, 21))
        self.mainversion_label.setObjectName("mainversion_label")
        self.gridLayout_14.addWidget(self.mainversion_label, 0, 0, 1, 1)
        self.gridLayout_16.addLayout(self.gridLayout_14, 1, 2, 1, 1)
        self.line_35 = QtWidgets.QFrame(self.layoutWidget2)
        self.line_35.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_35.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_35.setObjectName("line_35")
        self.gridLayout_16.addWidget(self.line_35, 2, 1, 1, 1)
        self.line_36 = QtWidgets.QFrame(self.layoutWidget2)
        self.line_36.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_36.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_36.setObjectName("line_36")
        self.gridLayout_16.addWidget(self.line_36, 0, 2, 1, 1)
        self.line_37 = QtWidgets.QFrame(self.layoutWidget2)
        self.line_37.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_37.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_37.setObjectName("line_37")
        self.gridLayout_16.addWidget(self.line_37, 1, 0, 1, 1)
        self.line_38 = QtWidgets.QFrame(self.layoutWidget2)
        self.line_38.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_38.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_38.setObjectName("line_38")
        self.gridLayout_16.addWidget(self.line_38, 1, 3, 1, 1)
        self.uidcode_bar_label = QtWidgets.QLabel(self.groupBox_2)
        self.uidcode_bar_label.setGeometry(QtCore.QRect(10, 110, 231, 91))
        self.uidcode_bar_label.setObjectName("uidcode_bar_label")
        self.lcdNumber = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdNumber.setGeometry(QtCore.QRect(420, 220, 71, 20))
        self.lcdNumber.setSmallDecimalPoint(False)
        self.lcdNumber.setObjectName("lcdNumber")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.tabWidget.setEnabled(False)

        self.auto_label_brake_state.setScaledContents(True)
        self.auto_label_warninglight_state.setScaledContents(True)
        self.auto_label_poweroff_state.setScaledContents(True)
        self.auto_label_poweron_state.setScaledContents(True)
        self.auto_label_rs232_state.setScaledContents(True)
        self.auto_label_rs485_state.setScaledContents(True)
        self.auto_label_di_state.setScaledContents(True)
        self.auto_label_do_state.setScaledContents(True)
        self.auto_label_delay_state.setScaledContents(True)
        self.auto_label_charge_state.setScaledContents(True)
        self.auto_label_can_state.setScaledContents(True)
        self.auto_label_emc_state.setScaledContents(True)
        self.auto_label_bootlight_state.setScaledContents(True)

        self.manual_label_state_bootlight.setScaledContents(True)
        self.manual_label_state_brake_off.setScaledContents(True)
        self.manual_label_state_brake_on.setScaledContents(True)
        self.manual_label_state_can.setScaledContents(True)
        self.manual_label_state_charge_brake.setScaledContents(True)
        self.manual_label_state_charge_ground.setScaledContents(True)
        self.manual_label_state_delay_brake.setScaledContents(True)
        self.manual_label_state_delay_on.setScaledContents(True)
        self.manual_label_state_di_ground.setScaledContents(True)
        self.manual_label_state_di_off.setScaledContents(True)
        self.manual_label_state_do_off.setScaledContents(True)
        self.manual_label_state_do_on.setScaledContents(True)
        self.manual_label_state_emc_off.setScaledContents(True)
        self.manual_label_state_emc_on.setScaledContents(True)
        self.manual_label_state_rs232.setScaledContents(True)
        self.manual_label_state_rs485.setScaledContents(True)
        self.manual_label_state_warn_off.setScaledContents(True)
        self.manual_label_state_warn_on.setScaledContents(True)

        self.auto_push_button_test.clicked.connect(self.onykeyAutoTest)     #一键自动测试
        self.push_connect.clicked.connect(self.connectFunc)                 #connect
        self.auto_push_button_report.clicked.connect(self.onkeyReport)      #一键生成报告
        self.manual_test_push_openpc.clicked.connect(self.manualOpenPC)     #开机
        self.manual_test_push_closepc.clicked.connect(self.manualClosePC)   #关机
        self.auto_push_button_pause.clicked.connect(self.autoTestPause)     #暂停
        self.manual_print_barcode.clicked.connect(self.printBarcode) #打印条形码

        self.auto_test_sendcmd_thread = autoTestSendCmdThread()         
        self.auto_test_sendcmd_thread.process_bar_signal.connect(self.updateAutoTestProcessBar)     #更新进度条
        self.auto_test_sendcmd_thread.result_signal.connect(self.autoTestSignal)                    #更新测试通过次数
        self.auto_test_sendcmd_thread.abnormal_msg_signal.connect(self.updateStatusBar)             #更新底部状态栏

        self.listen_reply_thread = listenReplyThread()
        self.resetAllAutoTestCounter()

        self.connect_thread = connectThread()
        self.connect_thread.gyro_signal.connect(self.handleGyroVersion)                  #更新陀螺仪版本              
        self.connect_thread.main_signal.connect(self.handleMainVersion)                  #更新主版本
        self.connect_thread.uid_signal.connect(self.handleUID)                           #更新UID

        self.first_in = True
        self.forbidden = False
        self.uid_string = ""
 
        self.item = Test_Items()
        self.manual_test_push_rs232.clicked.connect(self.manual232)
        self.manual_test_push_485.clicked.connect(self.manual485)
        self.manual_test_push_can.clicked.connect(self.manualcan)
        self.manual_test_push_do_on.clicked.connect(self.manualdoOpen)
        self.manual_test_push_do_off.clicked.connect(self.manualdoClose)
        self.manual_test_push_bootlight.clicked.connect(self.manualbootLight)
        self.manual_test_push_emc_on.clicked.connect(self.manualemcOpen)
        self.manual_test_push_emc_off.clicked.connect(self.manualemcClose)
        self.manual_test_push_charge_groud.clicked.connect(self.manualchargeGround)
        self.manual_test_push_charge_brake.clicked.connect(self.manualchargeBrake)
        self.manual_test_push_brake_on.clicked.connect(self.manualbrakeOpen)
        self.manual_test_push_brake_off.clicked.connect(self.manualbrakeClose)
        self.manual_test_push_di_brake.clicked.connect(self.manualdiBrake)
        self.manual_test_push_di_ground.clicked.connect(self.manualdiGround)
        self.manual_test_push_delay_brake.clicked.connect(self.manualdelayBrake)
        self.manual_test_push_delay_on.clicked.connect(self.manualdelayClose)
        self.manual_test_push_warn_on.clicked.connect(self.manualwarnLightOpen)
        self.manual_test_push_warn_off.clicked.connect(self.manualwarnLightClose)

    def printBarcode(self):
        if self.uid_string != "" or self.uid_string != "解析失败":
            pDll = CDLL("./postek_q8/postekq8.dll")
            charPointer = bytes(self.uid_string,"gbk")
            pDll.printBarCode(charPointer)

    def manual232(self):
        self.udp.sendTestCmd(self.item.rs232, 0.5)

    def manual485(self):
        self.udp.sendTestCmd(self.item.rs485, 0.5)

    def manualcan(self):
        self.udp.sendTestCmd(self.item.can, 0.5)

    def manualdoOpen(self):
        self.udp.sendTestCmd(self.item.doOpen, 0.5)

    def manualdoClose(self):
        self.udp.sendTestCmd(self.item.doClose, 0.5)

    def manualbootLight(self):
        self.udp.sendTestCmd(self.item.bootLight, 0.5)

    def manualemcOpen(self):
        self.udp.sendTestCmd(self.item.emcOpen, 0.5)

    def manualemcClose(self):
        self.udp.sendTestCmd(self.item.emcClose, 0.5)

    def manualchargeGround(self):
        self.udp.sendTestCmd(self.item.chargeGround, 0.5)

    def manualchargeBrake(self):
        self.udp.sendTestCmd(self.item.chargeBrake, 0.5)
    
    def manualbrakeOpen(self):
        self.udp.sendTestCmd(self.item.brakeOpen, 0.5)
    
    def manualbrakeClose(self):
        self.udp.sendTestCmd(self.item.brakeClose, 0.5)
    
    def manualdiBrake(self):
        self.udp.sendTestCmd(self.item.diBrake, 0.5)

    def manualdiGround(self):
        self.udp.sendTestCmd(self.item.diGround, 0.5)

    def manualdelayBrake(self):
        self.udp.sendTestCmd(self.item.delayBrake, 0.5)

    def manualdelayClose(self):
        self.udp.sendTestCmd(self.item.delayClose, 0.5)

    def manualwarnLightOpen(self):
        self.udp.sendTestCmd(self.item.warnLightOpen, 0.5)

    def manualwarnLightClose(self):
        self.udp.sendTestCmd(self.item.warnLightClose, 0.5)
    
    def autoTestPause(self):
        self.auto_test_sendcmd_thread.pause_signal = True
        self.statusbar.showMessage("test is stop...", 9999)

    def manualOpenPC(self):
        self.udp.sendTestCmd(0x11,0.5)

    def manualClosePC(self):
        self.udp.sendTestCmd(0x12,0.5)

    def onkeyReport(self):
        try:
            finished_percent = float(int(self.auto_line_text_pass_percent.text()) / 100)
        except:
            finished_percent = 0.8
        text_name = self.uid_string
        rs232_test_times = int(self.auto_line_text_total.text())*int(self.auto_line_text_rs232.text())
        rs485_test_times = int(self.auto_line_text_total.text())*int(self.auto_line_text_rs485.text())
        can_test_times = int(self.auto_line_text_total.text())*int(self.auto_line_text_can.text())
        do_test_times = int(self.auto_line_text_total.text())*int(self.auto_line_text_do.text())
        bootlight_test_times = int(self.auto_line_text_total.text())*int(self.auto_line_text_bootlight.text())
        emc_test_times = int(self.auto_line_text_total.text())*int(self.auto_line_text_emc.text())
        charge_test_times = int(self.auto_line_text_total.text())*int(self.auto_line_text_charge.text())
        brake_test_times = int(self.auto_line_text_total.text())*int(self.auto_line_text_brake.text())
        di_test_times = int(self.auto_line_text_total.text())*int(self.auto_line_text_di.text())
        delay_test_times = int(self.auto_line_text_total.text())*int(self.auto_line_text_delay.text())
        warn_test_times = int(self.auto_line_text_total.text())*int(self.auto_line_text_warninglight.text())
        openpc_test_times = int(self.auto_line_text_total.text())*int(self.auto_line_text_poweron.text())
        closepc_test_times = int(self.auto_line_text_total.text())*int(self.auto_line_text_poweroff.text())
        key_word_file = ".\\report\\" + text_name + ".txt"
        file = open(key_word_file,'w+', encoding='utf-8')
        file.write("******测试报告******\n")
        file.write("时间：" + time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time())) + "\n")
        file.write("UID："+ self.uid_string + "\n")
        file.write("主控版本：" + self.mainversion_string + "\n")
        file.write("陀螺仪版本：" + self.gyroversion_string + "\n")
        file.write("总循环次数：" + self.auto_line_text_total.text() + "\n")
        file.write("开机次数：" + str(openpc_test_times) + "\n")
        file.write("关机次数：" + str(closepc_test_times) + "\n")

        file.write("rs232测试：\n")
        file.write("\t总次数：" + str(rs232_test_times)+"\n")
        file.write("\t成功："+str(self.auto_rs232_yes_counter)+ "\n")
        rs232_result = self.auto_rs232_yes_counter >= finished_percent*rs232_test_times
        if rs232_result:
            file.write("\t结果：" + "pass\n")
        else:
            file.write("\t结果：" + "fail\n")

        file.write("rs485测试：\n")
        file.write("\t总次数：" + str(rs485_test_times)+"\n")
        file.write("\t成功："+str(self.auto_rs485_yes_counter)+ "\n")
        rs485_result = self.auto_rs485_yes_counter >= finished_percent*rs485_test_times
        if rs485_result:
            file.write("\t结果：" + "pass\n")
        else:
            file.write("\t结果：" + "fail\n")

        file.write("can测试：\n")
        file.write("\t总次数：" + str(can_test_times)+"\n")
        file.write("\t成功："+str(self.auto_can_yes_counter)+ "\n")
        can_result = self.auto_can_yes_counter >= finished_percent*can_test_times
        if can_result:
            file.write("\t结果：" + "pass\n")
        else:
            file.write("\t结果：" + "fail\n")

        file.write("DO测试：\n")
        file.write("\t总次数：" + str(do_test_times)+"\n")
        file.write("\t成功："+str(self.auto_do_yes_counter)+ "\n")
        do_result = self.auto_do_yes_counter >= finished_percent*do_test_times
        if do_result:
            file.write("\t结果：" + "pass\n")
        else:
            file.write("\t结果：" + "fail\n")

        file.write("开机灯测试：\n")
        file.write("\t总次数：" + str(bootlight_test_times)+"\n")
        file.write("\t成功："+str(self.auto_bootlight_yes_counter)+ "\n")
        bootlight_result = self.auto_bootlight_yes_counter >= finished_percent*bootlight_test_times
        if bootlight_result:
            file.write("\t结果：" + "pass\n")
        else:
            file.write("\t结果：" + "fail\n")

        file.write("急停测试：\n")
        file.write("\t总次数：" + str(emc_test_times)+"\n")
        file.write("\t成功："+str(self.auto_emc_yes_counter)+ "\n")
        emc_result = self.auto_emc_yes_counter >= finished_percent*emc_test_times
        if emc_result:
            file.write("\t结果：" + "pass\n")
        else:
            file.write("\t结果：" + "fail\n")

        file.write("充电测试：\n")
        file.write("\t总次数：" + str(charge_test_times)+"\n")
        file.write("\t成功："+str(self.auto_charge_yes_counter)+ "\n")
        charge_result = self.auto_charge_yes_counter >= finished_percent*charge_test_times
        if charge_result:
            file.write("\t结果：" + "pass\n")
        else:
            file.write("\t结果：" + "fail\n")

        file.write("抱闸测试：\n")
        file.write("\t总次数：" + str(brake_test_times)+"\n")
        file.write("\t成功："+str(self.auto_brake_yes_counter)+ "\n")
        brake_result = self.auto_brake_yes_counter >= finished_percent*brake_test_times
        if brake_result:
            file.write("\t结果：" + "pass\n")
        else:
            file.write("\t结果：" + "fail\n") 

        file.write("DI测试：\n")
        file.write("\t总次数：" + str(di_test_times)+"\n")
        file.write("\t成功："+str(self.auto_di_yes_counter)+ "\n")
        di_result = self.auto_di_yes_counter >= finished_percent*di_test_times
        if di_result:
            file.write("\t结果：" + "pass\n")
        else:
            file.write("\t结果：" + "fail\n") 

        file.write("继电器测试：\n")
        file.write("\t总次数：" + str(delay_test_times)+"\n")
        file.write("\t成功："+str(self.auto_delay_yes_counter)+ "\n")
        delay_result = self.auto_delay_yes_counter >= finished_percent*delay_test_times
        if delay_result:
            file.write("\t结果：" + "pass\n")
        else:
            file.write("\t结果：" + "fail\n")

        file.write("报警灯测试：\n")
        file.write("\t总次数：" + str(warn_test_times)+"\n")
        file.write("\t成功："+str(self.auto_warn_yes_counter)+ "\n")
        warn_result = self.auto_warn_yes_counter >= finished_percent*warn_test_times
        if warn_result:
            file.write("\t结果：" + "pass\n")
        else:
            file.write("\t结果：" + "fail\n")
        if warn_result and delay_result and di_result and brake_result and charge_result and emc_result and bootlight_result and do_result and can_result and rs485_result and rs232_result:
            file.write("结论：" + "pass\n")
            self.statusbar.showMessage("测试结果全部成功，请查看...", 99999)
        else:
            file.write("结论：" + "fail\n")
            self.statusbar.showMessage("测试结果存在失败，请查看...", 99999)
        file.close()
        document = open(key_word_file,'r',encoding = "utf-8") 
        self.textBrowser.setText("")
        for i in document.readlines():
            self.textBrowser.append(i)
        document.close()
        self.tabWidget.setCurrentIndex(2)

    def resetAllAutoTestCounter(self):
        self.auto_rs232_yes_counter = 0
        self.auto_rs485_yes_counter = 0
        self.auto_can_yes_counter = 0
        self.auto_can_yes_counter = 0
        self.auto_do_yes_counter = 0
        self.auto_bootlight_yes_counter =0
        self.auto_emc_yes_counter =0 
        self.auto_charge_yes_counter =0
        self.auto_brake_yes_counter =0
        self.auto_di_yes_counter =0
        self.auto_delay_yes_counter =0
        self.auto_warn_yes_counter =0

    def handleGyroVersion(self, version):
        self.gyroversion_string = version
        self.gyroversion_label.setText(version)
        if version == "解析失败" or self.forbidden:
            self.tabWidget.setEnabled(False)
        else:
            self.tabWidget.setEnabled(True)   
        
    def handleMainVersion(self, version, is_connected):
        self.mainversion_string = version
        self.mainversion_label.setText(version)
        if version == "解析失败":
            self.forbidden = True

    def handleUID(self, version, code_bar_address):
        self.uid_string = version
        self.uid_label.setText(version)
        if version == "解析失败":
            self.forbidden = True
        if code_bar_address != "NULL":
            self.uidcode_bar_label.setScaledContents(True)
            self.uidcode_bar_label.setPixmap(QtGui.QPixmap(code_bar_address))
        
    def connectFunc(self):
        if not self.first_in: 
            # self.udp.so.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.udp.setLocalPort(self.line_port.text())
            self.udp.setRemoteIp(self.line_ip.text())
            self.udp.connect()
        elif self.first_in == True:
            self.first_in = False
            self.udp = socketTool(self.line_ip.text(), int(self.line_port.text()))
        
        self.connect_thread.setSocket(self.udp.so)
        self.auto_test_sendcmd_thread.setSocketTool(self.udp)
        self.connect_thread.start()
        self.forbidden = False
        
    
    def resetAutoState(self):
        result_show = QtGui.QPixmap(".\\icon\\x.png")
        self.auto_label_rs232_state.setPixmap(result_show)
        self.auto_label_rs485_state.setPixmap(result_show)
        self.auto_label_can_state.setPixmap(result_show)
        self.auto_label_do_state.setPixmap(result_show)
        self.auto_label_bootlight_state.setPixmap(result_show)
        self.auto_label_emc_state.setPixmap(result_show)
        self.auto_label_charge_state.setPixmap(result_show)
        self.auto_label_brake_state.setPixmap(result_show)
        self.auto_label_di_state.setPixmap(result_show)
        self.auto_label_delay_state.setPixmap(result_show)
        self.auto_label_warninglight_state.setPixmap(result_show)

    def onykeyAutoTest(self):
        self.resetAllAutoTestCounter()
        self.resetAutoState()
        self.auto_test_sendcmd_thread.resetTotalTimesCounter()
        self.auto_test_sendcmd_thread.start()
        self.auto_test_sendcmd_thread.setRunStartTrigger()


    def autoTestSignal(self, item, yes_or_no):
        item_list = Test_Items()
        if yes_or_no:
            result_show = QtGui.QPixmap(".\\icon\\d.png")
        else:
            result_show = QtGui.QPixmap(".\\icon\\x.png")
        if item == item_list.rs232:
            if yes_or_no:
                self.auto_rs232_yes_counter = self.auto_rs232_yes_counter + 1
            self.auto_label_rs232_state.setPixmap(result_show)
        if item == item_list.rs485:
            if yes_or_no:
                self.auto_rs485_yes_counter = self.auto_rs485_yes_counter + 1
            self.auto_label_rs485_state.setPixmap(result_show)
        if item == item_list.can:
            if yes_or_no:
                self.auto_can_yes_counter = self.auto_can_yes_counter + 1
            self.auto_label_can_state.setPixmap(result_show)
        if item == item_list.doOpen:
            if yes_or_no:
                self.auto_do_yes_counter = self.auto_do_yes_counter + 1
            self.auto_label_do_state.setPixmap(result_show)
        if item == item_list.bootLight:
            if yes_or_no:
                self.auto_bootlight_yes_counter = self.auto_bootlight_yes_counter + 1
            self.auto_label_bootlight_state.setPixmap(result_show)
        if item == item_list.emcOpen:
            if yes_or_no:
                self.auto_emc_yes_counter = self.auto_emc_yes_counter + 1
            self.auto_label_emc_state.setPixmap(result_show)
        if item == item_list.chargeGround:
            if yes_or_no:
                self.auto_charge_yes_counter = self.auto_charge_yes_counter + 1
            self.auto_label_charge_state.setPixmap(result_show)
        if item == item_list.brakeClose:
            if yes_or_no:
                self.auto_brake_yes_counter = self.auto_brake_yes_counter + 1
            self.auto_label_brake_state.setPixmap(result_show)
        if item == item_list.diBrake:
            if yes_or_no:
                self.auto_di_yes_counter = self.auto_di_yes_counter + 1
            self.auto_label_di_state.setPixmap(result_show)
        if item == item_list.delayBrake:
            if yes_or_no:
                self.auto_delay_yes_counter = self.auto_delay_yes_counter + 1
            self.auto_label_delay_state.setPixmap(result_show)
        if item == item_list.warnLightOpen:
            if yes_or_no:
                self.auto_warn_yes_counter = self.auto_warn_yes_counter + 1
            self.auto_label_warninglight_state.setPixmap(result_show)

    def updateAutoTestProcessBar(self, total_times, total_times_counter):
        self.progressBar.setRange(0, total_times)
        self.progressBar.setValue(total_times_counter)
        print("t :" + str(total_times) + " tt  :" + str(total_times_counter))
        if total_times == total_times_counter:
            self.onkeyReport()

    def updateStatusBar(self, string): 
        self.statusbar.showMessage(string, 99999)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "AutoTest v1.4"))
        self.push_reset.setText(_translate("MainWindow", "Reset"))
        self.manual_test_push_rs232.setText(_translate("MainWindow", "rs232测试"))
        self.manual_test_push_485.setText(_translate("MainWindow", "rs485测试"))
        self.manual_test_push_can.setText(_translate("MainWindow", "can测试"))
        self.manual_test_push_do_on.setText(_translate("MainWindow", "DO全开测试"))
        self.manual_test_push_do_off.setText(_translate("MainWindow", "DO全关测试"))
        self.manual_test_push_bootlight.setText(_translate("MainWindow", "bootlight测试"))
        self.manual_test_push_emc_on.setText(_translate("MainWindow", "emc输出开测试"))
        self.manual_test_push_emc_off.setText(_translate("MainWindow", "emc输出关测试"))
        self.manual_test_push_charge_groud.setText(_translate("MainWindow", "charge接地测试"))
        self.manual_test_push_charge_brake.setText(_translate("MainWindow", "charge断开测试"))
        self.manual_test_push_brake_on.setText(_translate("MainWindow", "brake输出24-12V测试"))
        self.manual_test_push_brake_off.setText(_translate("MainWindow", "brake输出关测试"))
        self.manual_test_push_di_brake.setText(_translate("MainWindow", "DI断开测试"))
        self.manual_test_push_di_ground.setText(_translate("MainWindow", "DI接地测试"))
        self.manual_test_push_delay_brake.setText(_translate("MainWindow", "delay断开测试"))
        self.manual_test_push_delay_on.setText(_translate("MainWindow", "delay闭合测试"))
        self.manual_test_push_warn_on.setText(_translate("MainWindow", "warninglight开测试"))
        self.manual_test_push_warn_off.setText(_translate("MainWindow", "warninglight关测试"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "手动测试"))
        self.label_19.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">rs485测试</p></body></html>"))
        self.label_37.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">bootlight测试</p></body></html>"))
        self.label_33.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">brake输出测试</p></body></html>"))
        self.label_29.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">delay测试</p></body></html>"))
        self.label_31.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">warninglight测试</p></body></html>"))
        self.label_21.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">can测试</p></body></html>"))
        self.label_38.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">emc输出测试</p></body></html>"))
        self.label_59.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">测试项</p></body></html>"))
        self.label_22.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">DO测试</p></body></html>"))
        self.label_23.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">charge测试</p></body></html>"))
        self.label_36.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">DI测试</p></body></html>"))
        self.label_32.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">关机测试</p></body></html>"))
        self.label_20.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">rs232测试</p></body></html>"))
        self.label_30.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">开机测试</p></body></html>"))
        self.label_60.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">测试次数</p></body></html>"))

        config_file = open('config.json')
        js = json.load(config_file)
        target_ip = js["ip"]
        auto_item_config = js["autoTest"]
        auto_item_test_times = auto_item_config["testTimes"]
        auto_item_timeout = auto_item_config["timeout"]
        auto_item_total_times = auto_item_config["totalTimes"]
        auto_item_pass_percent = auto_item_config["passPercent"]

        self.auto_line_text_brake.setText(_translate("MainWindow", str(auto_item_test_times["brake"])))
        self.auto_line_text_bootlight.setText(_translate("MainWindow", str(auto_item_test_times["bootlight"])))
        self.auto_line_text_charge.setText(_translate("MainWindow", str(auto_item_test_times["charge"])))
        self.auto_line_text_can.setText(_translate("MainWindow", str(auto_item_test_times["can"])))
        self.auto_line_text_do.setText(_translate("MainWindow", str(auto_item_test_times["do"])))
        self.auto_line_text_di.setText(_translate("MainWindow", str(auto_item_test_times["di"])))
        self.auto_line_text_poweron.setText(_translate("MainWindow", str(auto_item_test_times["openPC"])))
        self.auto_line_text_rs485.setText(_translate("MainWindow", str(auto_item_test_times["rs485"])))
        self.auto_line_text_poweroff.setText(_translate("MainWindow", str(auto_item_test_times["closePC"])))
        self.auto_line_text_rs232.setText(_translate("MainWindow", str(auto_item_test_times["rs232"])))
        self.auto_line_text_delay.setText(_translate("MainWindow", str(auto_item_test_times["delay"])))
        self.auto_line_text_warninglight.setText(_translate("MainWindow", str(auto_item_test_times["warninglight"])))
        self.auto_line_text_emc.setText(_translate("MainWindow", str(auto_item_test_times["emc"])))

        self.label_61.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">状态</p></body></html>"))

        self.label_62.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">超时时间</p></body></html>"))
        self.auto_line_text_warninglight_timeout.setText(_translate("MainWindow", str(auto_item_timeout["warninglight"])))
        self.auto_line_text_rs485_timeout.setText(_translate("MainWindow", str(auto_item_timeout["rs485"])))
        self.auto_line_text_brake_timeout.setText(_translate("MainWindow", str(auto_item_timeout["brake"])))
        self.auto_line_text_delay_timeout.setText(_translate("MainWindow", str(auto_item_timeout["delay"])))
        self.auto_line_text_can_timeout.setText(_translate("MainWindow", str(auto_item_timeout["can"])))
        self.auto_line_text_do_timeout.setText(_translate("MainWindow", str(auto_item_timeout["do"])))
        self.auto_line_text_poweroff_timeout.setText(_translate("MainWindow", str(auto_item_timeout["closePC"])))
        self.auto_line_text_charge_timeout.setText(_translate("MainWindow", str(auto_item_timeout["charge"])))
        self.auto_line_text_emc_timeout.setText(_translate("MainWindow", str(auto_item_timeout["emc"])))
        self.auto_line_text_rs232_timeout.setText(_translate("MainWindow", str(auto_item_timeout["rs232"])))
        self.auto_line_text_poweron_timeout.setText(_translate("MainWindow", str(auto_item_timeout["openPC"])))
        self.auto_line_text_bootlight_timeout.setText(_translate("MainWindow", str(auto_item_timeout["bootlight"])))
        self.auto_line_text_di_timeout.setText(_translate("MainWindow", str(auto_item_timeout["di"])))

        self.auto_push_button_report.setText(_translate("MainWindow", "一键生成报告"))
        self.auto_push_button_test.setText(_translate("MainWindow", "一键自动测试"))
        self.auto_push_button_pause.setText(_translate("MainWindow", "暂停"))
        self.label_69.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">总循环次数</p></body></html>"))
        self.auto_line_text_total.setText(_translate("MainWindow", str(auto_item_total_times)))
        self.auto_line_text_pass_percent.setText(_translate("MainWindow", str(auto_item_pass_percent)))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("MainWindow", "自动测试"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_7), _translate("MainWindow", "测试报告"))
        self.groupBox.setTitle(_translate("MainWindow", "connect"))
        self.label_70.setText(_translate("MainWindow", "IP"))
        self.label_71.setText(_translate("MainWindow", "PORT"))
        self.line_ip.setText(_translate("MainWindow", str(target_ip)))
        self.line_port.setText(_translate("MainWindow", "4822"))
        self.manual_test_push_openpc.setText(_translate("MainWindow", "开机"))
        self.manual_test_push_closepc.setText(_translate("MainWindow", "关机"))
        self.manual_print_barcode.setText(_translate("MainWindow", "打印条形码"))
        self.push_connect.setText(_translate("MainWindow", "connect"))
        self.groupBox_2.setTitle(_translate("MainWindow", "info"))
        self.label_74.setText(_translate("MainWindow", "MainVersion:"))
        self.label_73.setText(_translate("MainWindow", "GyroVersion:"))
        self.label_75.setText(_translate("MainWindow", "UID:"))
        self.gyroversion_label.setText(_translate("MainWindow", "unknown"))
        self.uid_label.setText(_translate("MainWindow", "unknown"))
        self.mainversion_label.setText(_translate("MainWindow", "unknown"))
        self.uidcode_bar_label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:28pt;\">unknown</span></p></body></html>"))


class connectThread(QThread):
    gyro_signal = pyqtSignal(str)
    main_signal = pyqtSignal(str, bool)
    uid_signal = pyqtSignal(str, str)

    def setSocket(self, so):
        self.so = so

    def hex2string(self, hex_int):
        if(hex_int < 0x10):
            return "0"+str(hex(hex_int)).replace("0x","")
        else:
            return str(hex(hex_int)).replace("0x","")

    def run(self):     
        TESTBOART_ADDR = (ui.line_ip.text(), 4822)

        self.is_connected = False
        self.so.sendto(struct.pack('>HB',0x1234,0x16),TESTBOART_ADDR)
        self.so.settimeout(2)
        try:
            ret,address= self.so.recvfrom(1024)
        except socket.timeout:
            pass
        try:
            head, item_index, main1,main2,main3 = struct.unpack('>H3BH',ret)
            self.mainversion_string = str(main1) + "." + str(main2) + "." + str(main3)
            self.is_connected = True
            self.main_signal.emit(self.mainversion_string, self.is_connected)
        except:
            self.is_connected = False
            self.main_signal.emit("解析失败", self.is_connected) 

        self.so.sendto(struct.pack('>HB',0x1234,0x17),TESTBOART_ADDR)
        self.so.settimeout(2)
        try:
            ret,address= self.so.recvfrom(1024)
        except socket.timeout:
            pass
        try:
            head, item_index, gyro1,gyro2,gyro3 = struct.unpack('>H4B',ret)
            self.gyroversion_string = "f"+str(gyro1)+"."+str(gyro2)+"."+str(gyro3)
            if self.gyroversion_string == "f0.0.0":
                self.gyro_signal.emit("解析失败")
            else:
                self.gyro_signal.emit(self.gyroversion_string)
        except:
            self.gyro_signal.emit("解析失败")

        self.so.sendto(struct.pack('>HB',0x1234,0x15),TESTBOART_ADDR)
        self.so.settimeout(2)
        # self.so.connect(TESTBOART_ADDR)
        ret = b''
        try:
            ret,address= self.so.recvfrom(1024)
        except socket.timeout:
            pass
        try:
            head, item_index, uid1,uid2,uid3,uid4,uid5,uid6 = struct.unpack('>H7B',ret)
            print(str(hex(uid1)) + " " + str(hex(uid2)) + " " + str(hex(uid3)) + " " + str(hex(uid4)) + " " + str(hex(uid5)) + " " + str(hex(uid6)))
            uid1_string = self.hex2string(uid1)
            uid2_string = self.hex2string(uid2)
            uid3_string = self.hex2string(uid3)
            uid4_string = self.hex2string(uid4)
            uid5_string = self.hex2string(uid5)
            uid6_string = self.hex2string(uid6)
            self.uid_string = ((uid1_string+uid2_string+uid3_string+uid4_string+uid5_string+uid6_string)[:-1]).upper()
            print(self.uid_string)
            encoder=Code128Encoder(self.uid_string)
            encoder.save('.\\code_image\\' + self.uid_string + ".png", bar_width=2)
            fullname = '.\\code_image\\' + self.uid_string + ".png"
            self.uid_signal.emit(self.uid_string, fullname)  
        except Exception as e:
            print(e)
            self.uid_string = ""
            self.uid_signal.emit("解析失败", "NULL")

class autoTestSendCmdThread(QThread):
    result_signal = pyqtSignal(int, bool)
    process_bar_signal = pyqtSignal(int, int)
    abnormal_msg_signal = pyqtSignal(str)

    def setSocketTool(self, so):
        self.socket = so

    def resetTotalTimesCounter(self):
        self.total_times_counter = 0

    def processBarPlus(self):
        self.total_times_counter += 1
        self.process_bar_signal.emit(self.total_times, self.total_times_counter)

    def clearLastTest(self):
        self.socket.sendTestCmd(0xFF, 0)

    def testProcess(self, index, times, timeout_t):
        if self.pause_signal or times == 0:
            return
        if type(index) == list:
            while(times):  
                self.socket.sendTestCmd(index[0], timeout_t)
                result_1 = self.socket.recvTestResult(index[0])
                time.sleep(0.2)
                # self.clearLastTest()
                time.sleep(1)
                print("result 1 is " + str(result_1))
                self.socket.sendTestCmd(index[1], timeout_t)
                result_2 = self.socket.recvTestResult(index[1])
                print("result 2 is " + str(result_2))
                if result_2 and result_1:
                    self.result_signal.emit(index[0], True)
                else:
                    self.result_signal.emit(index[0], False)
                times = times - 1
                self.processBarPlus()
        elif type(index) == int:
            while(times):  
                self.socket.sendTestCmd(index, timeout_t)
                if self.socket.recvTestResult(index):
                    self.result_signal.emit(index, True)
                else:
                    self.result_signal.emit(index, False)
                times = times - 1
                self.processBarPlus()
        self.clearLastTest()
        time.sleep(0.2)     
    
    def setRunStartTrigger(self):
        self.trigger_once = True
        self.pause_signal = False

    def run(self):
        if self.trigger_once:
            self.total_times_counter = 0
            self.item_list = Test_Items() 
            self.abnormal_msg_signal.emit("auto test starts...") 
            try:
                openpc_times = int(ui.auto_line_text_poweron.text())
                closepc_times = int(ui.auto_line_text_poweroff.text())
                rs232_times = int(ui.auto_line_text_rs232.text())
                rs485_times = int(ui.auto_line_text_rs485.text())
                can_times = int(ui.auto_line_text_can.text())
                do_times = int(ui.auto_line_text_do.text())
                brake_times = int(ui.auto_line_text_brake.text())
                bootlight_times = int(ui.auto_line_text_bootlight.text())
                emc_times = int(ui.auto_line_text_emc.text())
                charge_times = int(ui.auto_line_text_charge.text())
                di_times = int(ui.auto_line_text_di.text())
                delay_times = int(ui.auto_line_text_delay.text())
                warnlight_times = int(ui.auto_line_text_warninglight.text())
                cycle_times = int(ui.auto_line_text_total.text())
                cycle_time_for_pc = cycle_times
                self.total_times = openpc_times + closepc_times + rs232_times + rs485_times + can_times + do_times + brake_times + bootlight_times+ emc_times + charge_times + di_times + delay_times + warnlight_times
                self.total_times = cycle_times*self.total_times
            except:
                openpc_times = 0
                closepc_times = 0
                rs232_times = 0
                rs485_times = 0
                can_times = 0
                do_times = 0
                brake_times = 0
                bootlight_times = 0
                emc_times = 0
                charge_times = 0
                di_times = 0
                delay_times = 00
                warnlight_times = 0
                
                self.abnormal_msg_signal.emit("测试次数必须为整数!")
                self.total_times = 0
                cycle_times = 0
                cycle_time_for_pc = 0
            
            try:
                openpc_time = float(ui.auto_line_text_poweron_timeout.text())
                closepc_time = float(ui.auto_line_text_poweroff_timeout.text())
                rs232_time = float(ui.auto_line_text_rs232_timeout.text())
                rs485_time = float(ui.auto_line_text_rs485_timeout.text())
                can_time = float(ui.auto_line_text_can_timeout.text())
                do_time = float(ui.auto_line_text_do_timeout.text())
                brake_time = float(ui.auto_line_text_brake_timeout.text())
                bootlight_time = float(ui.auto_line_text_bootlight_timeout.text())
                emc_time = float(ui.auto_line_text_emc_timeout.text())
                charge_time = float(ui.auto_line_text_charge_timeout.text())
                di_time = float(ui.auto_line_text_di_timeout.text())
                delay_time = float(ui.auto_line_text_delay_timeout.text())
                warnlight_time = float(ui.auto_line_text_warninglight_timeout.text())
            except:
                openpc_time = float(0.0)
                closepc_time = float(0.0)
                rs232_time = float(0.0)
                rs485_time = float(0.0)
                can_time = float(0.0)
                do_time = float(0.0)
                brake_time = float(0.0)
                bootlight_time = float(0.0)
                emc_time = float(0.0)
                charge_time = float(0.0)
                di_time = float(0.0)
                delay_time = float(0.0)
                warnlight_time = float(0.0)
                self.abnormal_msg_signal.emit("超时时间必须为浮点数!")

            self.process_bar_signal.emit(self.total_times, self.total_times_counter)
            
            while(cycle_times):
                if self.pause_signal:
                    break
                self.testProcess(self.item_list.rs232, rs232_times, rs232_time)
                self.testProcess(self.item_list.rs485, rs485_times, rs485_time) 
                self.testProcess(self.item_list.can, can_times, can_time)
                self.testProcess([self.item_list.doOpen, self.item_list.doClose], do_times,do_time)
                self.testProcess(self.item_list.bootLight, bootlight_times, bootlight_time)
                self.testProcess([self.item_list.emcOpen,self.item_list.emcClose], emc_times, emc_time)
                self.testProcess([self.item_list.chargeGround,self.item_list.chargeBrake], charge_times, charge_time)
                self.testProcess([self.item_list.brakeClose,self.item_list.brakeOpen], brake_times, brake_time)
                self.testProcess([self.item_list.diBrake,self.item_list.diGround], di_times, di_time)
                self.testProcess([self.item_list.delayBrake,self.item_list.delayClose], delay_times, delay_time)
                self.testProcess([self.item_list.warnLightOpen,self.item_list.warnLightClose], warnlight_times, warnlight_time)
                cycle_times = cycle_times - 1
            while(cycle_time_for_pc):
                if self.pause_signal:
                    break
                self.testProcess(self.item_list.openPC, openpc_times, openpc_time)
                self.testProcess(self.item_list.closePC, closepc_times, closepc_time)
                cycle_time_for_pc = cycle_time_for_pc -1
            self.trigger_once = False

class listenReplyThread(QThread):
    signal = pyqtSignal()           

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    # MainWindow.setStyleSheet("#MainWindow{border-image:url(./background/1.jpg);}")
    # MainWindow.setStyleSheet("#MainWindow{background-color: black}")
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())