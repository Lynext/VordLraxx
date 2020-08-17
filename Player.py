import Vars
import Offsets

class Player ():
    id = 0
    x = 0
    y = 0
    xVel = 0
    yVel = 0
    grounded = False
    inAnimation = False
    inStun = False
    jumpCount = 2
    name = "DefaultEntityName"
    pointer = 0

    def init (self):
        self.updateInfo()

    def printInfo (self):
        print("[X] : " + str(self.x) + " [Y] : " + str(self.y))

    def update (self):
        self.updateInfo()

    def updateInfo (self):
        self.x = Vars.mem.Address(self.pointer + Offsets.offsets["x"]).read(type='double')
        self.y = -Vars.mem.Address(self.pointer + Offsets.offsets["y"]).read(type='double')
        self.xVel = Vars.mem.Address(self.pointer + Offsets.offsets["xVel"]).read(type='double')
        self.yVel = -Vars.mem.Address(self.pointer + Offsets.offsets["yVel"]).read(type='double')
        self.jumpCount = 2 - Vars.mem.Address(self.pointer + Offsets.offsets["jumpCount"]).read(type='int')
        if Vars.mem.Address(self.pointer + Offsets.offsets["inAnimation"]).read(type='int') != 0:
            self.inAnimation = True
        else:
            self.inAnimation = False

        if Vars.mem.Address(self.pointer + Offsets.offsets["inStun"]).read(type='int') == 0:
            self.inStun = True
        else:
            self.inStun = False

        if Vars.mem.Address(self.pointer + Offsets.offsets["grounded"]).read(type='int') == 0:
            self.grounded = True
        else:
            self.grounded = False
