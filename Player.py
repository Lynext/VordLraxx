import Vars
import Offsets
import math

class Vector2 ():
    x = 0
    y = 0
    xDir = ""
    yDir = ""

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

    def dist (self, targ, type = "est", rtnType = "vec"):
        if type == "real" and rtnType == "val":
            return math.sqrt((self.x - targ.x) * (self.x - targ.x) + (self.y - targ.y) * (self.y - targ.y))
        if type == "est" and rtnType == "val":
            return math.sqrt(((self.x + self.xVel) - (targ.x + targ.xVel)) * ((self.x + self.xVel) - (targ.x + targ.xVel)) + ((self.y + self.yVel) - (targ.y + targ.yVel)) * ((self.y + self.yVel) - (targ.y + targ.yVel)))
        if type == "est" and rtnType == "vec":
            rX = (self.x + self.xVel) - (targ.x + targ.xVel)
            rY = (self.y + self.yVel) - (targ.y + targ.yVel)
            rtn = Vector2()
            rtn.x = rX
            rtn.y = rY
            if rtn.x < 0:
                rtn.xDir = "right"
            else:
                rtn.xDir = "left"
            if rtn.y < 0:
                rtn.yDir = "down"
            else:
                rtn.yDir = "up"
            return rtn
        if type == "real" and rtnType == "vec":
            rX = (self.x) - (targ.x)
            rY = (self.y) - (targ.y)
            rtn = Vector2()
            rtn.x = rX
            rtn.y = rY
            if rtn.x < 0:
                rtn.xDir = "right"
            else:
                rtn.xDir = "left"
            if rtn.y < 0:
                rtn.yDir = "down"
            else:
                rtn.yDir = "up"
            rtn.x = abs(rtn.x)
            rtn.y = abs(rtn.y)
            return rtn
        if type == "realEst" and rtnType == "vec":
            rX = (self.x + self.xVel) - (targ.x + targ.xVel)
            rY = (self.y + self.yVel) - (targ.y + targ.yVel)
            rtn = Vector2()
            rtn.x = rX
            rtn.y = rY
            if rtn.x < 0:
                rtn.xDir = "right"
            else:
                rtn.xDir = "left"
            if rtn.y < 0:
                rtn.yDir = "down"
            else:
                rtn.yDir = "up"
            rtn.x = abs(rtn.x)
            rtn.y = abs(rtn.y)
            return rtn

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

        if Vars.mem.Address(self.pointer + Offsets.offsets["canDodge"]).read(type='int') == 0:
            self.canDodge = True
        else:
            self.canDodge = False
