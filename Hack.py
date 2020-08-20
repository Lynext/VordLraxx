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
    Controller.jump("right", 300)

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
    if dir == "left":
        Vars.ginput.write(Controller.calculateActualInput() | Offsets.LEFT)
    else:
        Vars.ginput.write(Controller.calculateActualInput() | Offsets.RIGHT)
    if Utils.canJump() and Vars.localPlayer.jumpCount == 2:
        print("Jumping to save us. " + str(Vars.localPlayer.jumpCount) + " left.")
        Controller.jump(dir, 300)
    elif Utils.canDodge():
        print("Dodging to save us.")
        Controller.dodge(dir, Offsets.UP)
    elif Utils.canAttack():
        print("Attacking to save us.")
        Controller.sideHeavy(dir, 200)
    else:
        print("Cant dodge, cant jump and no heavy attack. We are prob dead.")

def ZeroToDeath ():
    realEstDiff = Vars.localPlayer.dist(Vars.target, type = "realEst")
    if Vars.target.inAnimation and Vars.localPlayer.dist(Vars.target, rtnType = "val") <= 384:
        if Utils.canDodge():
            print('Cool Dodge')
            Controller.dodge(Utils.reverseDir(realEstDiff.xDir), Offsets.UP)
        elif Utils.canJump():
            print('Jump Dodge')
            Controller.jump(Utils.reverseDir(realEstDiff.xDir))

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
    if not Vars.localPlayer.grounded:
        return
    realEstDiff = Vars.localPlayer.dist(Vars.target, type = "realEst")
    if realEstDiff.x <= 512 and realEstDiff.y <= 16:
        Controller.sideQuick(realEstDiff.xDir)
        time.sleep(0.3)
        Controller.neutralHeavy(realEstDiff.xDir,0)
        Controller.resetInput()
    elif realEstDiff.yDir == "up" and realEstDiff.x >= 200 and realEstDiff.x <= 512 and realEstDiff.y >= 128 and realEstDiff.y <= 300:
        Controller.neutralHeavy(realEstDiff.xDir,0)
        time.sleep(0.5) # sucssesful, sleep
    elif realEstDiff.x <= 512 and realEstDiff.y <= 300:
        Controller.sideHeavy(realEstDiff.xDir,0)
        time.sleep(0.5) # sucssesful, sleep

def BombDodgeMode ():
    #Utils.bombScan()
    # for i in Vars.entities:
    #     if Vars.entities[i].type == "Bomb" and Vars.entities[i].isOnMap():
    #         print("Bomb found on map. ID : " + str(i))
    #         realEstDiff = Vars.localPlayer.dist(Vars.entities[i], rtnType = "val", type = "real")
    #         print("Diff :" + str(realEstDiff))
    #         if realEstDiff < 50:
    #             print("Dodging")
    #             Controller.dodge()
    #             break
    # time.sleep(0.05)
    pass

def AI ():
    if Vars.mode == "Manuel":
        return

    if Vars.mode == "BombDodgeMode":
        BombDodgeMode()
        return

    if not Vars.localPlayer.grounded and Vars.localPlayer.y < Vars.info["maps"][Vars.map]["fallOffsetY"]:
        Vars.keepPressed = Offsets.LEFT
        if Vars.info["maps"][Vars.map]["centerOfX"] - Vars.localPlayer.x > 0:
            Vars.keepPressed = Offsets.RIGHT
        dontFallToDeath()
    elif Vars.localPlayer.grounded and Vars.keepPressed != 0:
        Vars.keepPressed = 0
        Controller.resetInput()

    if Vars.mode == "OnlyDodge":
        OnlyDodge()
        return

    if Vars.mode == "SpamMaster":
        SpamMaster()
        return

    if Vars.mode == "ZeroToDeath":
        ZeroToDeath()
        return

def update ():
    if Vars.end:
        exit()

    if not Vars.started:
        return

    if Vars.started and Vars.localPointer == 0:
        Utils.findFirstPointers()
        Utils.bombScan()

    for i in Vars.entities:
        Vars.entities[i].update()

    for key in Vars.entitiesToRemove:
        del Vars.entities[key]
    Vars.entitiesToRemove = []

    if Vars.debug:
        Vars.localPlayer.printInfo()
    AI()
    #time.sleep(0.016 / 10)

init()
while True:
    update()
