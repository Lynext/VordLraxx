from memorpy import MemWorker, Process
from memorpy.WinStructures import PAGE_READWRITE
import re

PROCESS_NAME = b'Brawlhalla.exe'

entity_sig_1 = b"\x00\x90\x64......\xA0.......\x00"
entity_sig_2 = b"\x90\x64\xCB\x63.\x00\x00\x20\x30"


def is_base_of_entity(mem, address):
    try:
        ptr = address
        for offset in recursive_ptr_offsets:
            ptr = mem.Address(ptr + offset).read()
        if ptr != address:
            return False
    except:
        return False
    else:
        return True

def aob_scan(mem, entity_pointers, start, size, pattern=None, offset=0, entity_check=False):
    all_the_bytes = mem.process.read(mem.Address(start), type='bytes', maxlen=size)
    #print(all_the_bytes)
    matches = re.finditer(pattern, all_the_bytes)
    for match in matches:
        span = match.span()
        if span:
            address = start + span[0] + offset
            if not entity_check:
                entity_pointers.append(address)
            elif address not in entity_pointers and is_base_of_entity(mem, address):
                    entity_pointers.append(address)

def dereference_offsets(mem, name_and_offsets):
    modules = mem.process.list_modules()
    name, offsets = name_and_offsets
    ptr = modules[name]
    for offset in offsets:
        ptr = mem.process.read(mem.Address(ptr + offset))
    return ptr

def entities_aob_scan(mem):
    print('Scanning memory for entities')
    modules = mem.process.list_modules()
    regions = mem.process.iter_region(start_offset=modules[PROCESS_NAME], protec=PAGE_READWRITE)
    entity_pointers = []
    print("Performing deep scan")
    for start, size in regions:
        if len(entity_pointers) >= 4:
            break
        aob_scan(mem, entity_pointers, start, size, pattern=entity_sig_2, offset=0, entity_check=False)

    print('Found %d entities : %s' % (len(entity_pointers), ', '.join([hex(e) for e in entity_pointers])))
    return entity_pointers

mem = MemWorker(pid=16492)
modules = mem.process.list_modules()
#print(str(modules))
entities_aob_scan(mem)
