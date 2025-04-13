import sys
import re
import asm_commands as asm

DEBUG =0
'''
eflags
Bit   Label    Desciption
---------------------------
0      CF      Carry flag
2      PF      Parity flag
4      AF      Auxiliary carry flag
6      ZF      Zero flag
7      SF      Sign flag
8      TF      Trap flag
9      IF      Interrupt enable flag
10     DF      Direction flag
11     OF      Overflow flag
12-13  IOPL    I/O Priviledge level
14     NT      Nested task flag
16     RF      Resume flag
17     VM      Virtual 8086 mode flag
18     AC      Alignment check flag (486+)
19     VIF     Virutal interrupt flag
20     VIP     Virtual interrupt pending flag
21     ID      ID flag
'''
#for now will be used only eflags
registers = {
	'ah': 0, 'al': 0, 'bh': 0, 'bl': 0, 'ch': 0, 'cl': 0, 'dh': 0, 'dl': 0,
	'ax': 0, 'bx': 0, 'cx': 0, 'dx': 0,
	'si': 0, 'di': 0,
	'sp': 0, 'bp': 0,
	'cs': 0, 'ds': 0, 'ss': 0, 'es': 0,
	'ip': 0,
	'flags': 0,
	
	'CR0': 0,'CR1': 0,'CR2': 0,'CR3': 0,'CR4': 0,
	'DR0': 0,'DR1': 0,'DR2': 0,'DR3': 0,'DR4': 0,'DR5': 0,'DR6': 0,'DR7': 0,
	'TR3': 0,'TR4': 0,'TR5': 0,'TR6': 0,'TR7': 0,
	'GDTR':0,'IDTR':0,'LDTR':0,'TR':0,
	
	'eax': 0, 'ebx': 0, 'ecx': 0, 'edx': 0,
	'esi': 0, 'edi': 0,
	'esp': 0, 'ebp': 0,
	'eip': 0,
	'eflags': 0,

	'rax': 0, 'rbx': 0, 'rcx': 0, 'rdx': 0,
	'rsi': 0, 'rdi': 0,
	'rsp': 0, 'rbp': 0,
	'rip': 0,
	'r8': 0, 'r9': 0, 'r10': 0, 'r11': 0, 'r12': 0, 'r13': 0, 'r14': 0, 'r15': 0,

	'xmm0': 0, 'xmm1': 0, 'xmm2': 0, 'xmm3': 0, 'xmm4': 0, 'xmm5': 0, 'xmm6': 0, 'xmm7': 0,
	'xmm8': 0, 'xmm9': 0, 'xmm10': 0, 'xmm11': 0, 'xmm12': 0, 'xmm13': 0, 'xmm14': 0, 'xmm15': 0,
	'xmm16': 0, 'xmm17': 0, 'xmm18': 0, 'xmm19': 0, 'xmm20': 0, 'xmm21': 0, 'xmm22': 0, 'xmm23': 0,
	'xmm24': 0, 'xmm25': 0, 'xmm26': 0, 'xmm27': 0, 'xmm28': 0, 'xmm29': 0, 'xmm30': 0, 'xmm31': 0,

	'ymm0': 0, 'ymm1': 0, 'ymm2': 0, 'ymm3': 0, 'ymm4': 0, 'ymm5': 0, 'ymm6': 0, 'ymm7': 0,
	'ymm8': 0, 'ymm9': 0, 'ymm10': 0, 'ymm11': 0, 'ymm12': 0, 'ymm13': 0, 'ymm14': 0, 'ymm15': 0,
	'ymm16': 0, 'ymm17': 0, 'ymm18': 0, 'ymm19': 0, 'ymm20': 0, 'ymm21': 0, 'ymm22': 0, 'ymm23': 0,
	'ymm24': 0, 'ymm25': 0, 'ymm26': 0, 'ymm27': 0, 'ymm28': 0, 'ymm29': 0, 'ymm30': 0, 'ymm31': 0,

	'zmm0': 0, 'zmm1': 0, 'zmm2': 0, 'zmm3': 0, 'zmm4': 0, 'zmm5': 0, 'zmm6': 0, 'zmm7': 0,  
	'zmm8': 0, 'zmm9': 0, 'zmm10': 0, 'zmm11': 0, 'zmm12': 0, 'zmm13': 0, 'zmm14': 0, 'zmm15': 0,
	'zmm16': 0, 'zmm17': 0, 'zmm18': 0, 'zmm19': 0, 'zmm20': 0, 'zmm21': 0, 'zmm22': 0, 'zmm23': 0,
	'zmm24': 0, 'zmm25': 0, 'zmm26': 0, 'zmm27': 0, 'zmm28': 0, 'zmm29': 0, 'zmm30': 0, 'zmm31': 0
}

current_mode = 32


storage_max = 1_000_000_000	#1mb
storage= []

#its list of lists so this i is like a superposition and we wanna get the position

labels = {}

#intel commands https://en.wikipedia.org/wiki/X86_instruction_listings
asm_commands = {
	'AAA': asm.AAA,
	'AAD': asm.AAD,
	'AAM': asm.AAM,
	'AAS': asm.AAS,
	'ADC': asm.ADC,
	'ADD': asm.ADD,
	'AND': asm.AND,
	'CAL': asm.CALL,
	'CBW': asm.CBW,
	#todo: finish the rest
	'MOV': asm.MOV,
	'JMP': asm.JMP
}


def dprint(_str,**k):
	if DEBUG == 1:
		print(_str,**k)
	return

def storage_execute():
	#todo: update it while the instruction pointer is not on the end
	full_len = len(storage)
	dprint(f"full len: {len(storage)}")
	a = asm.get_instruction_ptr(registers)
	while a < full_len:
		dprint(a)
		dprint(storage[a])
		
		aexecute(storage[a])
		if not a == asm.get_instruction_ptr(registers):
			a = asm.get_instruction_ptr(registers)
		else:
			a+=1
			asm.set_instruction_ptr(a,registers)
		
def aexecute(linstr):
	dprint(linstr)
	#todo: support creating vars, aka if not an istruction then check if i the instructuins
	#is intended to create a var
	
	if linstr[0].upper() in asm_commands:
		#will pass even unused by the instruction arguments
		asm_commands[linstr[0].upper()]((linstr,registers,labels))
		
	else:
	
		raise Exception(f"Wrong/Unsupported instruction: {linstr[0]}")
		

#for now will pass only one argumen - the file to execute
def read_settings(*a,start=1):
	#_len = len(a[0])
	#args = list(a[0])
	#for i in range(start,_len):
	#	print(args[i])
	try:
		fpath = a[0][1]
		
		read_asm(fpath)
		
	#except Exception as error:
		#print(type(error).__name__ )
		#print(error)
	except IndexError:
		print("Error: the file was not inputed.")
		quit()



def read_asm(fpath):

	try:
		curr_index = 0
		lcurr_instruction=[]
		_file = open(fpath)
		lfile = _file.readlines()
		for i in lfile:
			sline = str(i)
			lline = re.split(r'[,\s]+',sline)
			lcurr_instruction = []
			for j in lline:
				
				if ';' in j:
					if j.split(";")[0] != '':
						lcurr_instruction.append(j.split(";")[0])	
						dprint(j.split(";")[0])
					dprint("skipping")
					break
				elif j != '':
					lcurr_instruction.append(j)
				dprint(j, end = ' ')
			
			if lcurr_instruction != []:
				
				#check if its an label
				dprint(f"{lcurr_instruction}")
				
				if ':' in lcurr_instruction[0] or  ':' == lcurr_instruction[1]:
					#currently dont have better idea how to do it
					_label = lcurr_instruction.pop(0)
					if len(lcurr_instruction):
						if ':' == lcurr_instruction[0]:
							lcurr_instruction.pop(0)
							
						elif not _label[-1] == ':':
							
							dprint("special case")
							label_split = _label.split(":")
							_label = label_split[0]
							lcurr_instruction.insert(0,label_split[1])
						else:
							#hope i dont have issues with this later on..
							_label = _label[0:-1]
					else:
						_label = _label[0:-1]
						
					if _label in labels.keys():
						#wont print the line for now
						raise Exception(f"{_label} inconsistently redefined!")
					
					dprint(f"curr_index: {len(storage)}")
					labels[_label] = len(storage)
					
					dprint(f"after {lcurr_instruction}")
				
				
				if lcurr_instruction == []:
					dprint("skipped")
					continue
				
				dprint(curr_index)
				
				#if i remember correctly, its actually curr_index+=len()*curr_bit_mode/8
				#but for now idc
				curr_index+=len(lcurr_instruction)
				if(curr_index>=storage_max):
					r = curr_index-storage_max
					
					storage.append(lcurr_instruction[0:r])
					print("STORAGE ALREADY FULL")
					print(f"{storage_max}bytes / {curr_index}bytes")
					curr_index=storage_max-1
					print("executing anyway...")
					return
				else:
					storage.append(lcurr_instruction)
			
			dprint('')
			
		return
		
	except FileNotFoundError:
		print("Error: file on path "+fpath+" not found")
		quit("quitting..")
	except Exception as error:
		print("Exception_Name:"+type(error).__name__)
		print("Error: "+str(error))
		quit("quitting..")


if __name__ == "__main__":
	try:
		read_settings(sys.argv)
		storage_execute()
		print(registers)
	except Exception as error:
		print("Error: "+str(error))

