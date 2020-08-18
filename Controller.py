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

def dash (towards):
    if towards == "left":
        Vars.ginput.write(Offsets.DODGE | Offsets.LEFT)
    if towards == "right":
        Vars.ginput.write(Offsets.DODGE | Offsets.RIGHT)

def gravityCancel ():
    Vars.ginput.write(Offsets.DODGE)
    resetInput()
    #time.sleep(0.1)

def dodge (towards = "spot", diagonal = 0):
    if towards == "spot":
        Vars.ginput.write(Offsets.DODGE)
    if towards == "left":
        Vars.ginput.write(Offsets.UP | Offsets.LEFT)
        resetInput()
        Vars.ginput.write(Offsets.DODGE | diagonal | Offsets.LEFT)
    if towards == "right":
        Vars.ginput.write(Offsets.UP | Offsets.RIGHT)
        resetInput()
        Vars.ginput.write(Offsets.DODGE | diagonal | Offsets.RIGHT)
    if towards == "up":
        Vars.ginput.write(Offsets.UP)
        resetInput()
        Vars.ginput.write(Offsets.DODGE | Offsets.UP)
    resetInput()
    time.sleep(0.1)

def run (dir, duration):
    if dir == "left":
        rt = Utils.gTime()
        while (Utils.gTime() - rt < duration):
            Vars.ginput.write(calculateActualInput() | Offsets.LEFT)
    elif dir == "right":
        rt = Utils.gTime()
        while (Utils.gTime() - rt < duration):
            Vars.ginput.write(calculateActualInput() | Offsets.RIGHT)
    resetInput()

def sideHeavy (towards, duration = 0):
    if towards == "right":
        rt = Utils.gTime()
        Vars.ginput.write(calculateActualInput() | Offsets.RIGHT | Offsets.HEAVY_ATTACK)
        while (Utils.gTime() - rt < duration):
            Vars.ginput.write(calculateActualInput() | Offsets.RIGHT | Offsets.HEAVY_ATTACK)
    elif towards == "left":
        rt = Utils.gTime()
        Vars.ginput.write(calculateActualInput() | Offsets.LEFT | Offsets.HEAVY_ATTACK)
        while (Utils.gTime() - rt < duration):
            Vars.ginput.write(calculateActualInput() | Offsets.LEFT | Offsets.HEAVY_ATTACK)
    resetInput()

def neutralHeavy (towards, duration = 0):
    if towards == "right":
        if duration == 0:
            Vars.ginput.write(calculateActualInput() | Offsets.RIGHT)
            resetInput()
            Vars.ginput.write(calculateActualInput() | Offsets.HEAVY_ATTACK)
            resetInput()
            return
        rt = Utils.gTime()
        Vars.ginput.write(calculateActualInput() | Offsets.RIGHT)
        resetInput()
        Vars.ginput.write(calculateActualInput() | Offsets.HEAVY_ATTACK)
        while (Utils.gTime() - rt < duration):
            Vars.ginput.write(calculateActualInput() | Offsets.HEAVY_ATTACK)
    elif towards == "left":
        if duration == 0:
            Vars.ginput.write(calculateActualInput() | Offsets.LEFT)
            resetInput()
            Vars.ginput.write(calculateActualInput() | Offsets.HEAVY_ATTACK)
            resetInput()
            return
        rt = Utils.gTime()
        Vars.ginput.write(calculateActualInput() | Offsets.LEFT)
        resetInput()
        Vars.ginput.write(calculateActualInput() | Offsets.HEAVY_ATTACK)
        while (Utils.gTime() - rt < duration):
            Vars.ginput.write(calculateActualInput() | Offsets.HEAVY_ATTACK)
    resetInput()

def sideQuick (towards):
    if towards == "right":
        Vars.ginput.write(calculateActualInput() | Offsets.RIGHT | Offsets.QUICK_ATTACK)
    elif towards == "left":
        Vars.ginput.write(calculateActualInput() | Offsets.LEFT | Offsets.QUICK_ATTACK)
    resetInput()

def jump (towards = "up", duration = 200):
    Vars.lastJump = Utils.gTime()
    if towards == "up":
        Vars.ginput.write(calculateActualInput() | Offsets.UP)
        rt = Utils.gTime()
        while (Utils.gTime() - rt < duration):
            Vars.ginput.write(calculateActualInput() | Offsets.UP)
    if towards == "left":
        Vars.ginput.write(calculateActualInput() | Offsets.UP)
        resetInput()
        rt = Utils.gTime()
        while (Utils.gTime() - rt < duration):
            Vars.ginput.write(calculateActualInput() | Offsets.UP | Offsets.LEFT)
    if towards == "right":
        Vars.ginput.write(calculateActualInput() | Offsets.UP)
        resetInput()
        rt = Utils.gTime()
        while (Utils.gTime() - rt < duration):
            Vars.ginput.write(calculateActualInput() | Offsets.UP | Offsets.RIGHT)
    resetInput()

def resetInput(hard = False, u = 0):
    if hard:
        time.sleep(0.03)
        Vars.ginput.write(0)
        return
    time.sleep(0.03)
    Vars.ginput.write(calculateActualInput() | u | Vars.keepPressed)
