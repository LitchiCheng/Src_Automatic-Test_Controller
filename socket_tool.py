import socket
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