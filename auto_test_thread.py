from PyQt5.QtCore import QThread,pyqtSignal
from test_item import Test_Items
import time

class autoTestSendCmdThread(QThread):
    result_signal = pyqtSignal(int, bool)
    process_bar_signal = pyqtSignal(int, int)
    abnormal_msg_signal = pyqtSignal(str)
    
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
    delay_times = 0
    warnlight_times = 0
    cycle_times = 0

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
        if self.pause_signal:
            return
        
        if type(index) == list:
            while(times):  
                self.socket.sendTestCmd(index[0], timeout_t)
                result_1 = self.socket.recvTestResult(index[0])
                time.sleep(0.2)
                self.clearLastTest()
                time.sleep(0.2)
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
            self.cycle_time_for_pc = self.cycle_times  
            self.total_times = self.openpc_times + self.closepc_times + self.rs232_times + self.rs485_times + self.can_times + self.do_times + self.brake_times + self.bootlight_times+ self.emc_times + self.charge_times + self.di_times + self.delay_times + self.warnlight_times
            self.total_times = self.cycle_times*self.total_times
            self.process_bar_signal.emit(self.total_times, self.total_times_counter)            
            while(self.cycle_times):
                self.testProcess(self.item_list.rs232, self.rs232_times, self.rs232_time)
                self.testProcess(self.item_list.rs485, self.rs485_times, self.rs485_time) 
                self.testProcess(self.item_list.can, self.can_times, self.can_time)
                self.testProcess([self.item_list.doOpen, self.item_list.doClose], self.do_times,self.do_time)
                self.testProcess(self.item_list.bootLight, self.bootlight_times, self.bootlight_time)
                self.testProcess([self.item_list.emcOpen,self.item_list.emcClose], self.emc_times, self.emc_time)
                self.testProcess([self.item_list.chargeGround,self.item_list.chargeBrake], self.charge_times, self.charge_time)
                self.testProcess([self.item_list.brakeClose,self.item_list.brakeOpen], self.brake_times, self.brake_time)
                self.testProcess([self.item_list.diBrake,self.item_list.diGround], self.di_times, self.di_time)
                self.testProcess([self.item_list.delayBrake,self.item_list.delayClose], self.delay_times, self.delay_time)
                self.testProcess([self.item_list.warnLightOpen,self.item_list.warnLightClose], self.warnlight_times, self.warnlight_time)
                self.cycle_times = self.cycle_times - 1
            while(self.cycle_time_for_pc):
                self.testProcess(self.item_list.openPC, openpc_times, openpc_time)
                self.testProcess(self.item_list.closePC, closepc_times, closepc_time)
                self.cycle_time_for_pc = self.cycle_time_for_pc -1
            self.trigger_once = False