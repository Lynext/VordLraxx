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
lastJump = 0
jumpCooldown = 500
map = "shipwreck"


# GAME INFO
info = {}
info["maps"] = {}
info["maps"]["shipwreck"] = {"fallOffsetY": -1848.99 - 320, "centerOfX": 1673}
