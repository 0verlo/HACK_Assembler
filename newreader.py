#!/usr/bin/env python
# coding=utf-8
import sys
import re
import json

print("hello")

class asmCode(object):
    def __init__(self,file_name):
        self.code_line = -1
        self.cur_line = -1
        self.cur_type = -1
        self.cur_instruction = '' 
        self.cur_symbol = ''
        self.cur_bin_inst = ''
        self.__inst_read = ''
        self.__default_map = dict()
        self.__symbol_table = dict()
        self.__map_init()
        self.__symbol_builder(file_name)
        self.file = open(file_name,'r')

    #A-instruction analysys
    def __A_inst_parsing(self):
        value = '0' 
        key = re.search(r'\@([A-z]\w+)',self.cur_instruction)
        if key:
            if key.group(1) in self.__symbol_table.keys():
                value = self.__symbol_table[key.group(1)]
        else:
            key = re.search(r'@(\d+)',self.cur_instruction)
            value = key.group(1)
        #print('value='+value+':'+bin(int(value,10))[2:].zfill(16))
        return bin(int(value,10))[2:].zfill(16)

    #C-instruction analysys
    def __C_inst_parsing(self):
        #print(self.cur_instruction)
        dest = ''
        comp = ''
        jmp = ''
        key = re.search(r'([A,M,D]+)\s*=\s*([-,+,!,D,M,A,&,|,1,0]+)',self.cur_instruction)
        if key:
            #print(key.group(1)+"---"+key.group(2))
            if (key.group(1) in self.__default_map[1]) and \
                (key.group(2) in self.__default_map[0]):
                dest = self.__default_map[1][key.group(1)]
                comp = self.__default_map[0][key.group(2)]
                jmp = '000'
            #print("inst is :"+"111"+comp+dest+jmp)
            return ("111"+comp+dest+jmp)
        key = re.search(r'([-,+,!,D,M,A,&,|,1,0]+)\s*;\s*(J\w{2})',self.cur_instruction)
        if key:
            #print(key.group(1)+"---"+key.group(2))
            if ((key.group(1) in self.__default_map[0]) and \
                (key.group(2) in self.__default_map[2])):
                dest = "000"
                comp = self.__default_map[0][key.group(1)]
                jmp = self.__default_map[2][key.group(2)]
            #print("inst is :"+"111"+comp+dest+jmp)
            return ("111"+comp+dest+jmp)
        print("Get C-inst paser error.")
        return

    #clean up the empty lines and comments
    def __commend_clean(self,string):
        return re.sub(r'\/\/.*','',string).strip()

    #separate 3 different pasering
    def __str_preprocess(self,string):
        if not (string):
            self.cur_type = -1
        #0.symbol_defin
 
        #1.a_instruction
        elif ('@'==string[0]):
            self.cur_type = 1 
            self.cur_instruction = self.__commend_clean(string)
            self.code_line = self.code_line+1
        #2.c_instruction
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
            self.cur_line = self.cur_line + 1
            #print('in'+str(self.cur_line))
            self.__str_preprocess(line.strip())
            if(0 == self.cur_type):
                self.__symbol_table_write()
        #print(self.__symbol_table)
        first_round.close()
        self.cur_line = -1
        self.code_line = -1

    #second round convert the asm to binary
    def nextInstruction(self):
        for line in self.file:
            self.__str_preprocess(line.strip())
            if(1 == self.cur_type):
                self.cur_bin_inst = self.__A_inst_parsing()
                yield self.cur_bin_inst
            if(2 == self.cur_type):
                self.cur_bin_inst = self.__C_inst_parsing()
                yield self.cur_bin_inst

    def close(self):
        self.file.close()

file_name = sys.argv[1]
key = re.search(r'((\.\/|\/)(\w+\/)*(\w+)).asm',file_name)
if key:
    output_file = (key.group(1)+".hack")
    output_fp = open(output_file,'w')
    print(output_file)
    currentCode = asmCode(file_name)
    i = 0
    outputlist = []
    try:
        while 1:
            next(currentCode.nextInstruction())
            #if ("0000000000000000" == currentCode.cur_bin_inst):
                print(currentCode.cur_instruction)
            outputlist.append(currentCode.cur_bin_inst+"\n")
    except StopIteration:
        output_fp.writelines(outputlist)

