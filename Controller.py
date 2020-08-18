from Player import Vector2
from Player import Player
import Vars
import Utils
import Offsets
import keyboard
import time

def calculateActualInput():
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

def dodge (towards = "spot"):
    if towards == "spot":
        Vars.ginput.write(Offsets.DODGE)
    if towards == "left":
        Vars.ginput.write(Offsets.DODGE | Offsets.LEFT)
    if towards == "right":
        Vars.ginput.write(Offsets.DODGE | Offsets.RIGHT)
    resetInput()

def run (dir):
    if dir == "left":
        if Vars.ginput.read() != Offsets.LEFT:
            resetInput()
            Vars.ginput.write(calculateActualInput() | Offsets.LEFT)
    elif dir == "right":
        if Vars.ginput.read() != Offsets.RIGHT:
            resetInput()
            Vars.ginput.write(calculateActualInput() | Offsets.RIGHT)

def sideHeavy (towards):
    if towards == "right":
        Vars.ginput.write(calculateActualInput() | Offsets.RIGHT | Offsets.HEAVY_ATTACK)
        resetInput()
    elif towards == "left":
        Vars.ginput.write(calculateActualInput() | Offsets.LEFT | Offsets.HEAVY_ATTACK)
        resetInput()

def jump (towards = "up"):
    print("JUMP")
    Vars.lastJump = Utils.gTime()
    if towards == "up":
        while (Utils.gTime() - Vars.lastJump < 500):
            Vars.ginput.write(calculateActualInput() | Offsets.UP)
    if towards == "left":
        Vars.ginput.write(calculateActualInput() | Offsets.UP | Offsets.LEFT)
    if towards == "right":
        Vars.ginput.write(calculateActualInput() | Offsets.UP | Offsets.RIGHT)
    resetInput()

def resetInput(hard = False, u = 0):
    if hard:
        Vars.ginput.write(0)
        #time.sleep(0.03)
    #time.sleep(0.03)
    Vars.ginput.write(calculateActualInput() | u)
