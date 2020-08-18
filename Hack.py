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
    keyboard.add_hotkey('ctrl+r', lambda: act("right"))

def act (arg):
    Controller.run("right",800)

def setMode (m):
    Vars.mode = m

def setDebug (d):
    Vars.debug = d

def dontFallToDeath ():
    print("Trying not to fall.")
    dir = "left"
    if Vars.info["maps"][Vars.map]["centerOfX"] - Vars.localPlayer.x > 0:
        dir = "right"
    if Utils.canJump():
            Controller.jump(dir, 800)
    elif Utils.canDodge():
        Controller.dodge(dir, Offsets.UP)
    elif Vars.localPlayer.canAttack:
        Controller.sideHeavy(dir, 800)
    else:
        Controller.run(dir,800)

def OnlyDodge ():
    realEstDiff = Vars.localPlayer.dist(Vars.target, type = "realEst")
    if Vars.target.inAnimation and Vars.localPlayer.dist(Vars.target, rtnType = "val") <= 384:
        if Utils.canDodge():
            print('Cool Dodge')
            Controller.dodge(Utils.reverseDir(realEstDiff.xDir), Offsets.UP)
        elif Utils.canJump():
            print('Jump Dodge')
            Controller.jump(Utils.reverseDir(realEstDiff.xDir))

def AI ():
    if Vars.mode == "Manuel":
        return

    if Vars.localPlayer.y < Vars.info["maps"][Vars.map]["fallOffsetY"]:
        dontFallToDeath()

    if Vars.mode == "OnlyDodge":
        OnlyDodge()
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
