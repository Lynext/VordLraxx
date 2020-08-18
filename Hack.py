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
    if Vars.directStart:
        Utils.findFirstPointers()
    keyboard.add_hotkey('ctrl+end', lambda: safeExit())
    keyboard.add_hotkey('ctrl+d', lambda: setDebug(not Vars.debug))
    keyboard.add_hotkey('ctrl+r', lambda: act("right"))
    keyboard.add_hotkey('ctrl+v', lambda: setStarted(True))
    print("Started!")

def act (arg):
    Controller.sideQuick("right")
    time.sleep(0.29)
    Controller.neutralHeavy("right",0)

def setMode (m):
    Vars.mode = m

def setStarted (st):
    Vars.localPointer = 0
    Vars.started = st

def setDebug (d):
    Vars.debug = d

def dontFallToDeath ():
    print("Trying not to fall.")
    dir = "left"
    if Vars.info["maps"][Vars.map]["centerOfX"] - Vars.localPlayer.x > 0:
        dir = "right"
    if Utils.canJump() and Vars.localPlayer.jumpCount == 2:
        print("Jumping to save us. " + str(Vars.localPlayer.jumpCount) + " left.")
        Controller.jump(dir, 500)
    elif Utils.canDodge():
        print("Dodging to save us.")
        Controller.dodge(dir, Offsets.UP)
    elif Utils.canAttack():
        print("Attacking to save us.")
        Controller.sideHeavy(dir, 500)
    else:
        print("Cant dodge, cant jump and no heavy attack. We are prob dead.")
        Controller.run(dir,500)

def OnlyDodge ():
    realEstDiff = Vars.localPlayer.dist(Vars.target, type = "realEst")
    if Vars.target.inAnimation and Vars.localPlayer.dist(Vars.target, rtnType = "val") <= 384:
        if Utils.canDodge():
            print('Cool Dodge')
            Controller.dodge(Utils.reverseDir(realEstDiff.xDir), Offsets.UP)
        elif Utils.canJump():
            print('Jump Dodge')
            Controller.jump(Utils.reverseDir(realEstDiff.xDir))

def SpamMaster ():
    realEstDiff = Vars.localPlayer.dist(Vars.target, type = "realEst")
    if realEstDiff.x <= 512 and realEstDiff.y <= 16:
        Controller.sideQuick(realEstDiff.xDir)
        time.sleep(0.3)
        Controller.neutralHeavy(realEstDiff.xDir,0)
    elif realEstDiff.yDir == "up" and realEstDiff.x >= 300 and realEstDiff.x <= 512 and realEstDiff.y >= 64 and realEstDiff.y <= 128:
        Controller.neutralHeavy(realEstDiff.xDir,0)

def AI ():
    if Vars.mode == "Manuel":
        return

    if Vars.localPlayer.y < Vars.info["maps"][Vars.map]["fallOffsetY"]:
        dontFallToDeath()

    if Vars.mode == "OnlyDodge":
        OnlyDodge()
        return

    if Vars.mode == "SpamMaster":
        SpamMaster()
        return

def update ():
    if Vars.end:
        exit()
    if not Vars.started:
        return
    if Vars.started and Vars.localPointer == 0:
        Utils.findFirstPointers()
        Utils.groundWeaponScan()
    for i in Vars.entities:
        Vars.entities[i].update()
    if Vars.debug:
        Vars.localPlayer.printInfo()
    AI()
    #time.sleep(0.016 / 10)

init()
while True:
    update()
