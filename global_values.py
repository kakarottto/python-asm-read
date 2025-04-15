DEBUG =0
storage_max = 1_000_000_000	#1gb
current_mode = 32
stack_size = 1_000			#1kb
#default is the protected mode
asm_mode = 32

supported_modes = [16,32,64]
#'','e','r' as sp, esp, rsp
mode_char = ''


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


def set_mode(mode):
	if mode not in supported_modes:
		raise Exception(f"ASM MODE SUPPORTED: {supported_modes}")
	global asm_mode
	global mode_char
	
	#wont make it algorithmitically cuz they are only 3 modes(at far as i know)
	if mode == supported_modes[0]:
		mode_char = ''
	elif mode==supported_modes[1]:
		mode_char = 'e'
	elif mode==supported_modes[2]:
		mode_char = 'r'
	
	asm_mode = mode
	return

def dprint(_str,**k):
	if DEBUG == 1:
		print(_str,**k)
	return

