
ginputBaseOffset = 0x34

entitySig = b"\x90\x64......................\x01"
groundWeaponSig = b"\x90\x64\x30\x57\x02"
recursivePtrOffsets = [0x268, 0x4c]

offsets = {}

offsets["local"] = (b'Adobe AIR.dll', [0x01315508,0x60,0x64,0x314,0x568,0x230,0x24])
offsets["ginput"] = (b'Adobe AIR.dll', [0x01315500,0x330,0x7C,0x4,0x2C,0xE4,0x4F4])
offsets["x"] = 0x378
offsets["y"] = 0x370
offsets["grounded"] = 0xF4
offsets["inAnimation"] = 0xA0
offsets["xVel"] = 0x328
offsets["yVel"] = 0x320
offsets["inStun"] = 0x180
offsets["jumpCount"] = 0x1F0
offsets["canDodge"] = 0x154
offsets["canAttack"] = 0x3C
offsets["groundWeaponX"] = 0xF0

QUICK_ATTACK = 640
HEAVY_ATTACK = 64
UP = 17
DOWN = 2
LEFT = 4
RIGHT = 8
DODGE = 256
THROW = 516
SPEAR = 0x00005F77
SWORD = 0x00004222
KATAR = 25411
MELEE = 14969
