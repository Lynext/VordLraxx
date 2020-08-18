from memorpy import MemWorker, Process
from memorpy.WinStructures import PAGE_READWRITE
import Vars
import Utils
import Offsets
import time
import keyboard
import Controller

def safeExit ():
    Vars.end = True

def init ():
    Vars.mem = MemWorker(name = Vars.PROCESS_NAME)
    Vars.localPointer = Utils.dereferenceOffsets(Offsets.offsets["local"])
    ginputPtr = Utils.dereferenceOffsets(Offsets.offsets["ginput"])
    Vars.ginput = Vars.mem.Address(ginputPtr + Offsets.ginputBaseOffset)
    Vars.entityPointers = Utils.entitiesAobScan()
    Utils.preparePlayers()
    print("Your hex : " + hex(Vars.localPointer))
    print("ginput hex: " + hex(ginputPtr))
    Vars.target = Vars.entities[2]
    keyboard.add_hotkey('ctrl+end', lambda: safeExit())
    keyboard.add_hotkey('ctrl+d', lambda: setDebug(not Vars.debug))

def setMode (m):
    Vars.mode = m

def setDebug (d):
    Vars.debug = d

def dontFallToDeath ():
    print("Trying not to fall.")
    if Vars.info["maps"][Vars.map]["centerOfX"] - Vars.localPlayer.x > 0:
        if Utils.canJump():
            Controller.jump("right")
        else:
            Controller.run("right")
    else:
        if Utils.canJump():
            Controller.jump("left")
        else:
            Controller.run("left")

def AI ():
    if Vars.mode == "Manuel":
        return

    if Vars.localPlayer.inAnimation == True:
        return

    if Vars.localPlayer.y < Vars.info["maps"][Vars.map]["fallOffsetY"]:
        dontFallToDeath()
        return

    if Vars.mode == "OnlyDodge":
        realEstDiff = Vars.localPlayer.dist(Vars.target, type = "realEst")
        if Vars.target.inAnimation and Vars.localPlayer.dist(Vars.target, rtnType = "val") <= 256:
            if Vars.localPlayer.canDodge:
                print('Cool Dodge')
                Controller.dodge("spot")
            elif Utils.canJump():
                print('Jump Dodge')
                Controller.jump()
        return

    if Vars.mode == "SpamMaster":
        realEstDiff = Vars.localPlayer.dist(Vars.target, type = "realEst")
        if Vars.target.inAnimation and Vars.localPlayer.dist(Vars.target, rtnType = "val") <= 256:
            if Vars.localPlayer.canDodge:
                print('Cool Dodge')
                Controller.dodge(Utils.reverseDir(realEstDiff.xDir))
            elif Utils.canJump():
                print('Jump Dodge')
                Controller.jump(Utils.reverseDir(realEstDiff.xDir))
            return

        if Vars.localPlayer.grounded and realEstDiff.x <= 750 and realEstDiff.y <= 8:
            print(realEstDiff.xDir.upper() + " HEAVY ATTACK")
            Controller.sideHeavy(realEstDiff.xDir)
            return

def update ():
    if Vars.end:
        exit()
    for i in Vars.entities:
        Vars.entities[i].update()
    if Vars.debug:
        Vars.localPlayer.printInfo()
    AI()
    #time.sleep(0.016 / 10)

init()
while True:
    update()
