import Vars
import Offsets
from memorpy.WinStructures import PAGE_READWRITE
import re
from Player import Player
import time

def gTime ():
    return int(round(time.time() * 1000))

def reverseDir (dir):
    if dir == "left":
        return "right"
    if dir == "right":
        return "left"
    if dir == "up":
        return "down"
    if dir == "down":
        return "up"

def canGravityCancel ():
    if canAttack() and canDodge():
        return True
    return False

def canJump ():
    Vars.localPlayer.updateInfo()
    if Vars.localPlayer.jumpCount > 0:
        return True
    return False

def canDodge():
    Vars.localPlayer.updateInfo()
    if Vars.localPlayer.canDodge:
        return True
    return False

def canAttack ():
    Vars.localPlayer.updateInfo()
    if Vars.localPlayer.canAttack:
        return True
    return False

def isBaseOfEntity(address):
    try:
        ptr = address
        for offset in Offsets.recursivePtrOffsets:
            ptr = Vars.mem.Address(ptr + offset).read()
        if ptr != address:
            return False
    except:
        return False
    else:
        return True

def aobScan(entityPointers, start, size, pattern=None, offset = 0, entityCheck = False):
    allTheBytes = Vars.mem.process.read(Vars.mem.Address(start), type = 'bytes', maxlen = size)
    #print(allTheBytes)
    matches = re.finditer(pattern, allTheBytes)
    for match in matches:
        span = match.span()
        if span:
            address = start + span[0] + offset
            if not entityCheck:
                entityPointers.append(address)
            elif address not in entityPointers and isBaseOfEntity(address):
                #print(match)
                entityPointers.append(address)

def dereferenceOffsets(nameAndOffsets):
    modules = Vars.mem.process.list_modules()
    name, offsets = nameAndOffsets
    ptr = modules[name]
    for offset in offsets:
        ptr = Vars.mem.process.read(Vars.mem.Address(ptr + offset))
    return ptr

def groundWeaponScan():
    print('Scanning memory for ground weapons')
    modules = Vars.mem.process.list_modules()
    regions = Vars.mem.process.iter_region(start_offset = modules[Vars.PROCESS_NAME], protec = PAGE_READWRITE)
    entityPointers = []
    print("Performing deep scan for entities")
    for start, size in regions:
        #print(str(start) + " " + str(size))
        if len(entityPointers) >= 40:
            break
        aobScan(entityPointers, start, size, pattern = Offsets.groundWeaponSig, offset = 0, entityCheck = False)

    print('Found %d ground weapons: %s' % (len(entityPointers), ', '.join([hex(e) for e in entityPointers])))
    return entityPointers

def entitiesAobScan():
    print('Scanning memory for entities')
    modules = Vars.mem.process.list_modules()
    regions = Vars.mem.process.iter_region(start_offset = modules[Vars.PROCESS_NAME], protec = PAGE_READWRITE)
    entityPointers = []
    print("Performing deep scan for entities")
    for start, size in regions:
        #print(str(start) + " " + str(size))
        if len(entityPointers) >= 4:
            break
        aobScan(entityPointers, start, size, pattern = Offsets.entitySig, offset = 0, entityCheck = True)

    print('Found %d entities: %s' % (len(entityPointers), ', '.join([hex(e) for e in entityPointers])))
    entityPointers.remove(Vars.localPointer)
    return entityPointers

def findFirstPointers ():
    Vars.uniqueEntityID = 0
    print("Finding pointers..")
    Vars.entities = {}
    ginputPtr = dereferenceOffsets(Offsets.offsets["ginput"])
    Vars.ginput = Vars.mem.Address(ginputPtr + Offsets.ginputBaseOffset)
    Vars.localPointer = dereferenceOffsets(Offsets.offsets["local"])
    Vars.entityPointers = entitiesAobScan()
    preparePlayers()
    Vars.target = Vars.entities[2]
    Vars.started = True
    print("Your hex : " + hex(Vars.localPointer))
    print("ginput hex: " + hex(ginputPtr))

def addPlayer (pointer):
    Vars.uniqueEntityID += 1
    newPlayer = Player()
    newPlayer.id = Vars.uniqueEntityID
    newPlayer.pointer = pointer
    newPlayer.init()
    Vars.entities[newPlayer.id] = newPlayer
    return newPlayer

def preparePlayers ():
    Vars.localPlayer = addPlayer(Vars.localPointer)
    for i in Vars.entityPointers:
        addPlayer(i)

def getModule(module):
    returnModule = pyVars.mem.process.module_from_name(Vars.pm.process_handle, module)
    return returnModule

def listModules ():
    modules = Vars.mem.process.list_modules()
    for module in modules:
        print(module.name)
