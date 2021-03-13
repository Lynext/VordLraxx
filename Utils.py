import Vars
import Offsets
from memorpy.WinStructures import PAGE_READWRITE
import re
from Player import Player
from Bomb import Bomb
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

def checkIfPlayer(address):
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

def aobScan(entityPointers, start, size, pattern=None, offset = 0, entityCheck = False, entityCheckType = ""):
    allTheBytes = Vars.mem.process.read(Vars.mem.Address(start), type = 'bytes', maxlen = size)
    #print(allTheBytes)
    matches = re.finditer(pattern, allTheBytes)
    for match in matches:
        span = match.span()
        if span:
            address = start + span[0] + offset
            if address in entityPointers:
                continue

            if not entityCheck:
                entityPointers.append(address)
            else:
                if entityCheckType == "Player" and checkIfPlayer(address):
                    entityPointers.append(address)
                elif entityCheckType == "Bomb" and checkIfBomb(address):
                    entityPointers.append(address)

def dereferenceOffsets(nameAndOffsets):
    modules = Vars.mem.process.list_modules()
    name, offsets = nameAndOffsets
    ptr = modules[name]
    for offset in offsets:
        ptr = Vars.mem.process.read(Vars.mem.Address(ptr + offset))
    return ptr

def checkIfBomb (address):
    rtn = True
    try:
        if not Vars.mem.Address(address + Offsets.offsets["isBombOffset"]).read(type='double') == 35.0:
            rtn = False
        if not Vars.mem.Address(address + Offsets.offsets["bombX"]).read(type='double') != 0.0:
            rtn = False
    except:
        rtn = False
    return rtn

def bombScan ():
    print('Scanning memory for bombs')
    modules = Vars.mem.process.list_modules()
    regions = Vars.mem.process.iter_region(start_offset = modules[Vars.PROCESS_NAME], protec = PAGE_READWRITE)
    entityPointers = []
    print("Performing deep scan for entities")
    for start, size in regions:
        #print(str(start) + " " + str(size))
        if len(entityPointers) >= 40:
            break
        aobScan(entityPointers, start, size, pattern = Offsets.baseEntitySig, offset = 0, entityCheck = True, entityCheckType = "Bomb")

    print('Found %d bombs: %s' % (len(entityPointers), ', '.join([hex(e) for e in entityPointers])))
    for i in entityPointers:
        canAdd = True
        for j in Vars.entities:
            if Vars.entities[j].pointer == i:
                canAdd = False
        if canAdd:
            addBomb(i)
    return entityPointers

def entitiesAobScan():
    print('Scanning memory for entities')
    modules = Vars.mem.process.list_modules()
    regions = Vars.mem.process.iter_region(start_offset = modules[Vars.PROCESS_NAME], protec = PAGE_READWRITE)
    entityPointers = []
    print("Performing deep scan for entities")
    for start, size in regions:
        #print(str(start) + " " + str(size))
        aobScan(entityPointers, start, size, pattern = Offsets.entitySig, offset = 0, entityCheck = True, entityCheckType = "Player")

    print('Found %d entities: %s' % (len(entityPointers), ', '.join([hex(e) for e in entityPointers])))
    entityPointers.remove(Vars.localPointer)
    print ('If I am still running, eveything should be fine...')
    return entityPointers

def findFirstPointers ():
    Vars.uniqueEntityID = 0
    print("Finding pointers..")
    Vars.entities = {}
    ginputPtr = dereferenceOffsets(Offsets.offsets["ginput"])
    print("ginput hex: " + hex(ginputPtr))
    Vars.ginput = Vars.mem.Address(ginputPtr + Offsets.ginputBaseOffset)
    Vars.localPointer = dereferenceOffsets(Offsets.offsets["local"])
    print("Your hex : " + hex(Vars.localPointer))
    Vars.entityPointers = entitiesAobScan()
    #preparePlayers()
    #if Vars.mode != "BombDodgeMode":
        #Vars.target = Vars.entities[2]
    Vars.started = True
    

def addPlayer (pointer):
    Vars.uniqueEntityID += 1
    newPlayer = Player()
    newPlayer.id = Vars.uniqueEntityID
    newPlayer.pointer = pointer
    newPlayer.init()
    Vars.entities[newPlayer.id] = newPlayer
    return newPlayer

def addBomb (pointer):
    Vars.uniqueEntityID += 1
    newBomb = Bomb()
    newBomb.id = Vars.uniqueEntityID
    newBomb.pointer = pointer
    newBomb.init()
    Vars.entities[newBomb.id] = newBomb
    return newBomb

def preparePlayers ():
    Vars.localPlayer = addPlayer(Vars.localPointer)
    for i in Vars.entityPointers:
        addPlayer(i)

#def getModule(module):
    #returnModule = pyVars.mem.process.module_from_name(Vars.pm.process_handle, module)
    #return returnModule

def listModules ():
    modules = Vars.mem.process.list_modules()
    for module in modules:
        print(module.name)
