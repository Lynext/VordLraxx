import pymem
import Vars
import Offsets

def getModule(module):
    returnModule = pymem.process.module_from_name(Vars.pm.process_handle, module)
    return returnModule

def listModules ():
    modules = list(Vars.pm.list_modules())
    for module in modules:
        print(module.name)

def getAddress (offsets):
    address = Vars.moduleBase
    if Vars.debug:
        print(hex(address))
    for i in range(len(offsets)):
        address = Vars.pm.read_int(address + offsets[i])
        if Vars.debug:
            print(hex(address))
    return address

def getValueInt (offsets, name):
    val = -1
    val = Vars.pm.read_int(getAddress(offsets) + Offsets.offsets[name])
    return val

def getValueBytes (offsets, name, bytes):
    val = -1
    val = Vars.pm.read_bytes(getAddress(offsets) + Offsets.offsets[name],bytes)
    return val

def getValueDouble (offsets, name):
    val = -1
    val = Vars.pm.read_double(getAddress(offsets) + Offsets.offsets[name])
    return val

def setValueInt (offsets, name, val):
    Vars.pm.write_int(getAddress(offsets) + Offsets.offsets[name], val)
