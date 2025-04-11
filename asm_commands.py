#todo: read hex

def AAA(args,regs):
	return

def AAD(args,regs):
	
	return

def AAM(args,regs):
	return

def AAS(args,regs):
	return

def ADC(args,regs):
	return

def ADD(args,regs):
	regs[args[1]] += int(args[2],0)
	
	update_regs(regs, args[1])
	return

def AND(args,regs):
	regs[args[1]] &= int(args[2],0)
	update_regs(regs, args[1])
	return

def CALL(args,regs):
	return

def CBW(args,regs):
	return

def MOV(args,regs):
	assert len(args)==3,"MOV: passed more arguments than required"
	
	regs[args[1]] = int(args[2],0)
	

	update_regs(regs, args[1])
	return


##############################

def set_CF(regs):
	regs['eflags'] = regs['eflags'] | 1

def clear_CF(regs):
	regs['eflags'] = regs['eflags'] & 0

def is_CF(regs):
	#print(regs['eflags'])
	return regs['eflags']

def set_SF(regs):
	#set the 7th bit
	regs['eflags'] = regs['eflags'] | (1 << 7)

def clear_SF(regs):
	regs['eflags'] = regs['eflags'] & (0 << 7)

def is_SF(regs):
	#print(regs['eflags']>>7 & 1)
	return (regs['eflags']>>7 & 1)
#level: *l - 0, *h - 1, *x - 2, e*x - 3, r*x - 4
def update_regs(regs, r):
	if not check_general_reg(r):
		raise Exception("not supported/existing register")
		return
	
	level = 0
	type_r = ''
	
	if len(r) == 2:
		if r[-1] == 'l':
			pass
		elif r[-1] == 'h':
			level = 1
		elif r[-1] == 'x':
			level = 2
		else:
			return
		type_r = r[0]
		
		
	elif len(r) ==3:
		if r[0] == 'e':
			level = 3
		elif r[0] == 'r':
			level = 4
		else:
			return
		type_r = r[1]
	else:
		return
		
		
	#rn dont have better ideas
	#note: it may have some shitty bug, check it out
	if level == 0:
		regs[r] = u8(regs[r])
		if is_CF(regs):
			clear_CF(regs)
			regs[type_r+"h"] += u8(regs[type_r+"h"],regs)+1
		
		
		#set the *x 
		regs[type_r+"x"] = (u8(regs[type_r+'h']) << 8) + u8(regs[r])
		if is_CF(regs):
			clear_CF(regs)
			regs[type_r+"x"] += u16(regs[type_r+"x"],regs)+1
		
		regs["e"+type_r+"x"] = (u32(regs["e"+type_r+"x"]) >> 16 ) + u16(regs[type_r+"x"]) 
		if is_CF(regs):
			clear_CF(regs)
			regs["e"+type_r+"x"] += u32(regs["e"+type_r+"x"],regs)+1
		
		regs["r"+type_r+"x"] = (u64(regs["r"+type_r+"x"]) >> 32 ) + u32(regs["e"+type_r+"x"]) 
		if is_CF(regs):
			clear_CF(regs)
			regs["r"+type_r+"x"] += u64(regs["r"+type_r+"x"],regs)+1
	elif level == 1:
		#regs[type_r+"h"] = u8(int(regs[type_r+"h"]),regs)

		regs[r] = u16(regs[r])
		regs[type_r+"x"] = (u8(regs[r]) << 8) + u8(regs[type_r+"l"])
		
		if is_CF(regs):
			clear_CF(regs)
			regs[type_r+"x"] += u16(regs[type_r+"x"],regs)+1
		
		regs["e"+type_r+"x"] = (u32(regs["e"+type_r+"x"]) >> 16 ) + u16(regs[type_r+"x"]) 
		if is_CF(regs):
			clear_CF(regs)
			regs["e"+type_r+"x"] += u32(regs["e"+type_r+"x"],regs)+1
		
		regs["r"+type_r+"x"] = (u64(regs["r"+type_r+"x"]) >> 32 ) + u32(regs["e"+type_r+"x"]) 
		if is_CF(regs):
			clear_CF(regs)
			regs["r"+type_r+"x"] += u64(regs["r"+type_r+"x"],regs)+1
		
	elif level == 2:
		#regs[type_r+"x"] = u16(int(regs[type_r+"x"]),regs)
	
		regs[type_r+"x"]=u16(regs[type_r+"x"])
		regs["e"+type_r+"x"] = (u32(regs["e"+type_r+"x"]) >>16 ) + u16(regs[type_r+"x"]) 
		if is_CF(regs):
			clear_CF(regs)
			regs["e"+type_r+"x"] += u32(regs["e"+type_r+"x"],regs)+1
		
		regs["r"+type_r+"x"] = (u64(regs["r"+type_r+"x"]) >> 32 ) + u32(regs["e"+type_r+"x"]) 
		if is_CF(regs):
			clear_CF(regs)
			regs["r"+type_r+"x"] += u64(regs["r"+type_r+"x"],regs)+1

		regs[type_r+"l"] = u8(regs[type_r+"x"],regs)
		regs[type_r+"h"] = u8(regs[type_r+"x"]>>8,regs)

	elif level == 3:
		regs["e"+type_r+"x"] =  u32(regs["e"+type_r+"x"])
		
		regs[type_r+"x"] = (u32(regs["e"+type_r+"x"])&0xffff)
		regs[type_r+"h"] = (u16(regs[type_r+"x"])&0xff)
		regs[type_r+"l"] = (u16(regs[type_r+"x"])&0xff)
		
		regs["r"+type_r+"x"] = (u64(regs["r"+type_r+"x"]) >> 32 ) + u32(regs["e"+type_r+"x"]) 
		if is_CF(regs):
			clear_CF(regs)
			regs["r"+type_r+"x"] += u64(regs["r"+type_r+"x"],regs)+1
		
		if is_CF(regs):
			clear_CF(regs)
			regs["r"+type_r+"x"] += u64(regs["r"+type_r+"x"],regs)+1

	elif level == 4:
		regs["r"+type_r+"x"]= u64(regs["r"+type_r+"x"])
		regs["e"+type_r+"x"]= regs["r"+type_r+"x"] & 0xffffffff
		regs[type_r+"x"] 	= regs["r"+type_r+"x"] & 0xffff
		regs[type_r+"h"] 	= u16((regs["r"+type_r+"x"] & 0xff00)>>8)
		regs[type_r+"l"] 	= regs["r"+type_r+"x"] & 0x00ff

	return

def check_general_reg(r):
	if r[-1] in ['x','h','l']:
		return True
	return False

#casters from int to int8 uint8, etc..
def u8(x,regs=None):
	if abs(x) > 0xff:
		if regs != None:
			set_CF(regs)
		if x < 0:
			set_SF(regs)
			x = 255-((x<<8) & 0xff)
		else:
			x = ((x<<8) & 0xff)
	return x

def u16(x,regs=None):
	if abs(x) > 0xffff:
		if regs != None:
			set_CF(regs)
		if x < 0:
			x = 0xffff-((x<<16) & 0xffff)
		else:
			x = ((x << 16) & 0xffff)
	return x
def u32(x,regs=None):
	if abs(x) > 0xffffffff:
		if regs != None:
			set_CF(regs)
		if x < 0:
			set_SF(regs)
			x = 0xffffffff-((x<<32) & 0xffffffff)
		else:
			x = ((x<<32) & 0xffffffff)
	return x

def u64(x,regs=None):
	if abs(x) > 0xffffffffffffffff:
		if regs != None:
			set_CF(regs)
		if x < 0:
			set_SF(regs)
			x = 0xffffffffffffffff-((x<<64) & 0xffffffffffffffff)
		else:
			x = ((x<<64) & 0xffffffffffffffff)
	return x
