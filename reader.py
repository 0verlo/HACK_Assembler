#!/usr/bin/env python
# coding=utf-8
import re

print("hello")

class asmCode(object):
    def __init__(self,file_name):
        self.code_line = -1
        self.cur_type = -1
        self.cur_instruction = '' 
        self.cur_symbol = ''
        self.cur_bin_inst = ''
        self.__inst_read = ''
        self.__symbol_table = dict()
        self.__symbol_init()
        self.__symbol_builder(file_name)
        self.file = open(file_name,'r')

    def __dec2Bin(self):
        pass

    def __compMap(self):
        pass

    def __destMap(self):
        pass

    def __jumpMap(self):
        pass
    
    def __symbol_init(self):
        self.__symbol_table['R0']='0'
        self.__symbol_table['R1']='1'
        self.__symbol_table['R2']='2'
        self.__symbol_table['R3']='3'
        self.__symbol_table['R4']='4'
        self.__symbol_table['R5']='5'
        self.__symbol_table['R6']='6'
        self.__symbol_table['R7']='7'
        self.__symbol_table['R8']='8'
        self.__symbol_table['R9']='9'
        self.__symbol_table['R10']='10'
        self.__symbol_table['R11']='11'
        self.__symbol_table['R12']='12'
        self.__symbol_table['R13']='13'
        self.__symbol_table['R14']='14'
        self.__symbol_table['R15']='15'
        self.__symbol_table['R16']='16'
        self.__symbol_table['SCREEN']='16384'
        self.__symbol_table['KBD']='24576'
        self.__symbol_table['SP']='0'
        self.__symbol_table['LCL']='1'
        self.__symbol_table['ARG']='2'
        self.__symbol_table['THIS']='3'
        self.__symbol_table['THAT']='4'

    def __symbol_table_write(self):
        key = re.search(r'\((\w+)\)',self.cur_instruction).group(1)
        self.__symbol_table[key] = str(self.code_line+1)

    def __A_inst_parsing(self):
        value = '0' 
        key = re.search(r'\@([A-z]\w+)',self.cur_instruction)
        if key:
            if key.group(1) in self.__symbol_table.keys():
                value = self.__symbol_table[key.group(1)]
        else:
            key = re.search(r'@(\d+)',self.cur_instruction)
            value = key.group(1)
        print('value='+value+':'+bin(int(value,10))[2:].zfill(16))
        return bin(int(value,10))[2:].zfill(16)

    def __C_inst_parsing(self):
        pass

    #clean up the empty lines and comments
    def __commend_clean(self,string):
        return re.sub(r'\/\/.*','',string).strip()

    def __str_preprocess(self,string):
        if not (string):
            self.cur_type = -1
        #symbol_defin
        elif ('('==string[0]):
            self.cur_type = 0 
            self.cur_instruction = self.__commend_clean(string)
        #a_instruction
        elif ('@'==string[0]):
            self.cur_type = 1 
            self.cur_instruction = self.__commend_clean(string)
            self.code_line = self.code_line+1
        #c_instruction
        elif ((ord(string[0]) in range(ord('A'),ord('z')+1))or(string[0] in ['0','1'])):
            self.cur_type = 2 
            self.cur_instruction = self.__commend_clean(string)
            self.code_line = self.code_line+1
        else:
            self.cur_type = -1
        #print(self.cur_instruction,self.cur_type)

    #first round 2 get symbols
    def __symbol_builder(self,file_name):
        first_round = open(file_name,'r')
        for line in first_round:
            self.__str_preprocess(line.strip())
            if(0 == self.cur_type):
                self.__symbol_table_write()
        print(self.__symbol_table)
        first_round.close()

    #second round convert the asm to binary
    def nextInstruction(self):
        for line in self.file:
            self.__str_preprocess(line.strip())
            if(1 == self.cur_type):
                print('--'+self.cur_instruction)
                self.cur_bin_inst = self.__A_inst_parsing()
            if(2 == self.cur_type):
                pass
            yield self.cur_bin_inst

currentCode = asmCode("./AsmCodes/Max.asm")
i = 0
while (i < 30):
    print(next(currentCode.nextInstruction()))
    i=i+1
