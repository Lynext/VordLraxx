from memorpy import MemWorker, Process
from memorpy.WinStructures import PAGE_READWRITE
import Vars
import Utils
import Offsets

def init ():
    Vars.mem = MemWorker(name = Vars.PROCESS_NAME)
    Vars.localPointer = Utils.dereferenceOffsets(Offsets.offsets["local"])
    Vars.entityPointers = Utils.entitiesAobScan()
    print("Your hex : " + hex(Vars.localPointer))

init()
