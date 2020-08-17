from memorpy import MemWorker, Process
from memorpy.WinStructures import PAGE_READWRITE
import Vars
import Utils
import Offsets
import time
import keyboard

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

def calculate_actual_input():
    val = 0
    val |= Offsets.LEFT * keyboard.is_pressed('LEFT')
    val |= Offsets.RIGHT * keyboard.is_pressed('RIGHT')
    val |= Offsets.UP * keyboard.is_pressed('UP')
    val |= Offsets.DOWN * keyboard.is_pressed('DOWN')
    val |= Offsets.DODGE * keyboard.is_pressed('SHIFT')
    val |= Offsets.THROW * keyboard.is_pressed('q')
    val |= Offsets.QUICK_ATTACK * keyboard.is_pressed('c')
    val |= Offsets.HEAVY_ATTACK * keyboard.is_pressed('x')
    return val

def reset_input(hard=False, u=0):
    if hard:
        Vars.ginput.write(0)
        time.sleep(0.03)
    time.sleep(0.03)
    Vars.ginput.write(calculate_actual_input() | u)

def setMode (m):
    Vars.mode = m

def AI ():
    if Vars.localPlayer.inAnimation == True:
        return

    dx = Vars.target.x - Vars.localPlayer.x
    dy = Vars.target.y - Vars.localPlayer.y
    if Vars.localPlayer.grounded == False:
        if 1673 - Vars.localPlayer.x > 0:
            if Utils.gTime() - Vars.lastJump > 500:
                Vars.lastJump = Utils.gTime()
                Vars.ginput.write(calculate_actual_input() | Offsets.UP)
                reset_input()
            else:
                Vars.ginput.write(calculate_actual_input() | Offsets.RIGHT)
        else:
            if Utils.gTime() - Vars.lastJump > 500:
                Vars.lastJump = Utils.gTime()
                Vars.ginput.write(calculate_actual_input() | Offsets.UP)
                reset_input()
            else:
                Vars.ginput.write(calculate_actual_input() | Offsets.LEFT)
        return
    if Vars.mode == "SpamMaster":
        if abs(dx) < 350 and abs(dy) < 50:
            if Vars.localPlayer.x < Vars.target.x:
                Vars.ginput.write(calculate_actual_input() | Offsets.RIGHT | Offsets.HEAVY_ATTACK)
                reset_input()
                print("RIGHT ATTACK")
            else:
                Vars.ginput.write(calculate_actual_input() | Offsets.LEFT | Offsets.HEAVY_ATTACK)
                reset_input()
                print("LEFT ATTACK")
        else:
            if dx > 0:
                Vars.ginput.write(calculate_actual_input() | Offsets.RIGHT)
            else:
                Vars.ginput.write(calculate_actual_input() | Offsets.LEFT)

def update ():
    if Vars.end:
        exit()
    for i in Vars.entities:
        Vars.entities[i].update()
    AI()
    time.sleep(0.016 / 10)

init()
while True:
    update()
