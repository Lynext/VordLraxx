import time
import pymem
from pymem import Pymem
import Vars
import Utils
import Offsets
import keyboard

class PlayerEntity ():
    id = 0
    x = 0
    y = 0
    grounded = False
    name = "DefaultEntityName"
    offset = []

    def init (self):
        self.updateVars()

    def updateVars (self):
        self.x = Utils.getValueDouble(self.offset,"x")
        self.y = Utils.getValueDouble(self.offset,"y")
        self.grounded = not Utils.getValueInt(self.offset,"grounded")

def addPlayerEntity (entityName, offset):
    Vars.uniqueEntityID += 1
    newPlayer = PlayerEntity()
    newPlayer.offset = offset
    newPlayer.name = entityName
    newPlayer.id = Vars.uniqueEntityID
    Vars.entities[newPlayer.id] = newPlayer
    newPlayer.init()
    return newPlayer

def setMode (m):
    Vars.mode = m

Vars.pm = Pymem('Brawlhalla.exe')
print('Process: %s' % Vars.pm.process_id)
#Utils.listModules()
Vars.modules["Adobe AIR.dll"] = Utils.getModule("Adobe AIR.dll")
Vars.moduleBase = Vars.modules["Adobe AIR.dll"].lpBaseOfDll
print("Adobe AIR.dll Base : " + hex(Vars.moduleBase).upper())
keyboard.add_hotkey('ctrl + shift + a', lambda: setMode("JumpWhenGrounded"))
keyboard.add_hotkey('ctrl + shift + c', lambda: setMode("Idle"))

Vars.localEntity = addPlayerEntity("Me",Offsets.offsets["local"])
Utils.entities_aob_scan()

while True:
    Vars.localEntity.updateVars()
    print("X : " + str(Vars.localEntity.x) + " Y : " + str(Vars.localEntity.y))
    if Vars.mode == "JumpWhenGrounded":
        if Vars.localEntity.grounded:
            keyboard.press_and_release('W')
    time.sleep(0.02)
