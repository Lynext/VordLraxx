import pymem
import Vars
import Offsets
import re

def is_base_of_entity(address):
    try:
        ptr = address
        for offset in recursive_ptr_offsets:
            ptr = Vars.pm.read_int(ptr + offset)
        if ptr != address:
            return False
    except:
        return False
    else:
        return True


def aob_scan(entity_pointers, start, size, pattern=None, offset=0, entity_check=False):
    all_the_bytes = Vars.pm.read_bytes(start, size)
    matches = re.finditer(pattern, all_the_bytes)
    for match in matches:
        print("Match!")
        span = match.span()
        if span:
            address = start + span[0] + offset
            if not entity_check:
                entity_pointers.append(address)
            elif address not in entity_pointers and is_base_of_entity(mem, address):
                print("Found!")
                entity_pointers.append(address)

def dereference_offsets(name_and_offsets):
    modules = list(Vars.pm.list_modules())
    name, offsets = name_and_offsets
    ptr = modules[name]
    for offset in offsets:
        ptr = Vars.pm.read_int(ptr + offset)
    return ptr

def entities_aob_scan():
    print('Scanning memory for entities')
    modules = list(Vars.pm.list_modules())
    entity_pointers = []
    print("Performing deep scan")
    off = 4
    while True:
        if len(entity_pointers) >= 4:
            break
        aob_scan(entity_pointers, Vars.moduleBase + off, 4, pattern=Offsets.entity_sig_2, offset=1, entity_check=True)
        off += 4

    print('Found %d entities : %s' % (len(entity_pointers), ', '.join([hex(e) for e in entity_pointers])))
    return entity_pointers

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
