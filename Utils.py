import Vars
import Offsets
from memorpy.WinStructures import PAGE_READWRITE
import re
from Player import Player
import time

def gTime ():
    return int(round(time.time() * 1000))

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
    #print(all_the_bytes)
    matches = re.finditer(pattern, allTheBytes)
    for match in matches:
        span = match.span()
        if span:
            address = start + span[0] + offset
            if not entityCheck:
                entityPointers.append(address)
            elif address not in entityPointers and isBaseOfEntity(address):
                entityPointers.append(address)

def dereferenceOffsets(nameAndOffsets):
    modules = Vars.mem.process.list_modules()
    name, offsets = nameAndOffsets
    ptr = modules[name]
    for offset in offsets:
        ptr = Vars.mem.process.read(Vars.mem.Address(ptr + offset))
    return ptr

def ginputAobScan():
    print('Scanning memory for ginput')
    modules = Vars.mem.process.list_modules()
    regions = Vars.mem.process.iter_region(start_offset = modules[Vars.PROCESS_NAME], protec = PAGE_READWRITE)
    ginput_pointers = []
    print("Performing deep scan for ginput")
    for start, size in regions:
        # if len(ginput_pointers) >= 1:
        #     break
        aobScan(ginput_pointers, start, size, pattern = Offsets.ginputSig, offset = 0)

    print('Found %d ginput : %s' % (len(ginput_pointers), ', '.join([hex(e) for e in ginput_pointers])))
    assert len(ginput_pointers) == 1, "invalid number of ginput pointers found, find a better sig"
    ginput_pointer = ginput_pointers[0]
    print('g_input: %s' % hex(ginput_pointer))
    return ginput_pointer

def entitiesAobScan():
    print('Scanning memory for entities')
    modules = Vars.mem.process.list_modules()
    regions = Vars.mem.process.iter_region(start_offset = modules[Vars.PROCESS_NAME], protec = PAGE_READWRITE)
    entityPointers = []
    print("Performing deep scan for entities")
    for start, size in regions:
        if len(entityPointers) >= 4:
            break
        aobScan(entityPointers, start, size, pattern = Offsets.entitySig, offset = 0, entityCheck=True)

    entityPointers.remove(Vars.localPointer)
    print('Found %d entities (except you) : %s' % (len(entityPointers), ', '.join([hex(e) for e in entityPointers])))
    return entityPointers

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
