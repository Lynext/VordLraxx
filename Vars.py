PROCESS_NAME = b'Brawlhalla.exe'
mem = None
debug = False
mode = "OnlyDodge"
localPointer = 0
localPlayer = None
target = None
entities = {}
uniqueEntityID = 0
entityPointers = []
ginput = None
end = False
map = "shipwreck"


# GAME INFO
info = {}
info["maps"] = {}
info["maps"]["shipwreck"] = {"fallOffsetY": -1848.99 - 160, "centerOfX": 1673}
