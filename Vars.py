PROCESS_NAME = b'Brawlhalla.exe'
mem = None
debug = False
mode = "BombDodgeMode"
localPointer = 0
localPlayer = None
target = None
entities = {}
entitiesToRemove = []
uniqueEntityID = 0
entityPointers = []
ginput = None
end = False
map = "shipwreck"
directStart = False
started = False
velMultiplier = 2
keepPressed = 0

# GAME INFO
info = {}
info["maps"] = {}
info["maps"]["shipwreck"] = {"fallOffsetY": -1848.99 - 160, "centerOfX": 1673}
