entity_sig_1 = b"\x00\x90\x64......\xA0.......\x00" # base entity -1
entity_sig_2 = b"\x00.\x64..............\x00" # a looser variant

offsets = {}

offsets["local"] = [0x0131552C,0x564,0x344,0x460,0x568,0x230,0x24]
offsets["x"] = 0x378
offsets["y"] = 0x370
offsets["grounded"] = 0xF4
