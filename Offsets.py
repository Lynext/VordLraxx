
ginputBaseOffset = 0x34

entitySig = b"\x90\x64......................\x01"
baseEntitySig = b"\x90\x64" # Is it fully true ?
recursivePtrOffsets = [0x268, 0x4c]

offsets = {}

offsets["local"] = (b'Adobe AIR.dll', [0x01315508,0x60,0x64,0x314,0x568,0x230,0x24])
offsets["ginput"] = (b'Adobe AIR.dll', [0x01315500,0x338,0x58,0x8,0x2C,0x18C,0x4F4])
offsets["x"] = 0x378
offsets["y"] = 0x370
offsets["damageTaken"] = 0x418
offsets["grounded"] = 0xF4
offsets["inAnimation"] = 0xA0
offsets["xVel"] = 0x328
offsets["yVel"] = 0x320
offsets["inStun"] = 0x180
offsets["isDodgingCurrently"] = 0x408
offsets["jumpCount"] = 0x1F0
offsets["canDodge"] = 0x154
offsets["canAttack"] = 0x3C
offsets["groundWeaponX"] = 0xF0
offsets["bombX"] = 0xF8
offsets["bombY"] = 0xE8
offsets["bombYVel"] = 0xB0
offsets["bombXVel"] = 0xB8
offsets["isBombOffset"] = 0x130 # DOUBLE TYPE, 35 IF BOMB
offsets["weaponPtrOffsets"] = [0x2BC, 0x44, 0x8]

QUICK_ATTACK = 640
HEAVY_ATTACK = 64
UP = 17
DOWN = 2
LEFT = 4
RIGHT = 8
DODGE = 256
THROW = 516
LANCE = 19449
BLASTERS = 15929
MELEE = 14969
