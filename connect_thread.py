from PyQt5.QtCore import QThread,pyqtSignal
import struct,socket

class connectThread(QThread):
    gyro_signal = pyqtSignal(str)
    main_signal = pyqtSignal(str, bool)
    uid_signal = pyqtSignal(str, str)
    def setIP(self, line_ip):
        self.line_ip = line_ip

    def setSocket(self, so):
        self.so = so

    def run(self):
        TESTBOART_ADDR = (self.line_ip, 4822)
        self.so.sendto(struct.pack('>HB',0x1234,0x15),TESTBOART_ADDR)
        self.so.settimeout(2)
        # self.so.connect(TESTBOART_ADDR)
        try:
            ret,address= self.so.recvfrom(1024)
        except socket.timeout:
            pass
        try:
            head, item_index, uid1,uid2,uid3,uid4,uid5,uid6 = struct.unpack('>H7B',ret)
            print(str(uid1) + " " + str(hex(uid2)) + " " + str(uid3) + " " + str(uid4) + " " + str(uid5) + " " + str(uid6))
            if(uid1 != 0):
                uid1_string = str(hex(uid1))
            else:
                uid1_string = "00"
            if(uid2 != 0):
                uid2_string = str(hex(uid2))
            else:
                uid2_string = "00"
            if(uid3 != 0):
                uid3_string = str(hex(uid3))
            else:
                uid3_string = "00"
            if(uid4 != 0):
                uid4_string = str(hex(uid4))
            else:
                uid4_string = "00"
            if(uid5 != 0):
                uid5_string = str(hex(uid5))
            else:
                uid5_string = "00"
            if(uid6 != 0):
                uid6_string = str(hex(uid6))
            else:
                uid6_string = "00"
            self.uid_string = (uid1_string+uid2_string+uid3_string+uid4_string+uid5_string+uid6_string).replace("0x","")[:-1]
            fullname = " "
            self.uid_signal.emit(self.uid_string, fullname)  
        except:
            self.uid_signal.emit("解析失败", "NULL")

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
            self.gyro_signal.emit(self.gyroversion_string)
        except:
            self.gyro_signal.emit("解析失败")
   