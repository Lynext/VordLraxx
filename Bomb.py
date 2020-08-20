import Vars
import Offsets
from Player import Vector2

class Bomb ():
    type = "Bomb"
    id = 0
    x = 0
    y = 0
    xVel = 0
    yVel = 0
    name = "DefaultEntityName"
    pointer = 0

    def init (self):
        self.updateInfo()

    def printInfo (self):
        print("[X] : " + str(self.x) + " [Y] : " + str(self.y))

    def dist (self, targ, type = "est", rtnType = "vec"):
        self.updateInfo()
        if type == "real" and rtnType == "val":
            return math.sqrt((self.x - targ.x * Vars.velMultiplier) * (self.x - targ.x * Vars.velMultiplier) + (self.y - targ.y * Vars.velMultiplier) * (self.y - targ.y * Vars.velMultiplier))
        if type == "est" and rtnType == "val":
            return math.sqrt(((self.x + self.xVel * Vars.velMultiplier) - (targ.x + targ.xVel * Vars.velMultiplier)) * ((self.x + self.xVel * Vars.velMultiplier) - (targ.x + targ.xVel * Vars.velMultiplier)) + ((self.y + self.yVel * Vars.velMultiplier) - (targ.y + targ.yVel * Vars.velMultiplier)) * ((self.y + self.yVel * Vars.velMultiplier) - (targ.y + targ.yVel * Vars.velMultiplier)))
        if type == "est" and rtnType == "vec":
            rX = (self.x + self.xVel * Vars.velMultiplier) - (targ.x + targ.xVel * Vars.velMultiplier)
            rY = (self.y + self.yVel * Vars.velMultiplier) - (targ.y + targ.yVel * Vars.velMultiplier)
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
            rX = (self.x + self.xVel * Vars.velMultiplier) - (targ.x + targ.xVel * Vars.velMultiplier)
            rY = (self.y + self.yVel * Vars.velMultiplier) - (targ.y + targ.yVel * Vars.velMultiplier)
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

    def isOnMap (self):
        if Vars.mem.Address(self.pointer + Offsets.offsets["isBombOffset"]).read(type='double') == 35.0:
            return True
        return False

    def update (self):
        self.updateInfo()
        if self.id == 3:
            self.printInfo()
        # if Vars.mem.Address(self.pointer + Offsets.offsets["isBombOffset"]).read(type='double') != 35.0:
        #     Vars.entitiesToRemove.append(self.id)

    def updateInfo (self):
        self.x = Vars.mem.Address(self.pointer + Offsets.offsets["bombX"]).read(type='double')
        self.y = -Vars.mem.Address(self.pointer + Offsets.offsets["bombY"]).read(type='double')
        self.xVel = Vars.mem.Address(self.pointer + Offsets.offsets["bombXVel"]).read(type='double')
        self.yVel = -Vars.mem.Address(self.pointer + Offsets.offsets["bombYVel"]).read(type='double')
