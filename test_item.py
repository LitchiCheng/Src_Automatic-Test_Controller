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