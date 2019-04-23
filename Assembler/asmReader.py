#!/usr/bin/env python3
# coding=utf-8
import re

class asmReader(object):
    def __init__(self,file_name):
        #check for a right path input "./xx/xx.tmp" or "/xx/xx.tmp"
        key = re.search(r'(^((\/)|(\.\/))(\w+\/)*(\w+)).tmp',file_name)
        if not(key):
            print("Wrong file name input.")
            return
        self.dict_symbolRef= dict() 
        self.dict_destRef= dict() 
        self.dict_compRef = dict() 
        self.dict_jmpRef = dict() 
        self.__input = key.group(0)
        self.__output = (key.group(1)+".hack")

    def asmTranslator(self):
        if (not(self.dict_symbolRef) or\
            not(self.dict_destRef) or\
            not(self.dict_compRef) or\
            not(self.dict_jmpRef)):
            print("Symbol seting not done yet.")
            return

        fileReader = open(self.__input,'r')
        fileWriter = open(self.__output,'w')
        outstr = ""
        print(self.__output)
        for line in fileReader:
            #1.a_instruction
            if ('@'==line[0]):
                outstr = self.__A_inst_parsing(line)
            #2.c_instruction
            elif ((ord(line[0]) in range(ord('A'),ord('z')+1))or(line[0] in ['0','1'])):
                outstr = self.__C_inst_parsing(line)
            else:
                continue
            print(outstr)
            fileWriter.writelines(outstr+"\n")

        fileWriter.close()
        fileReader.close()

    #A-instruction analysys
    def __A_inst_parsing(self,string):
        value = '' 
        key = re.search(r'\@([A-z]\w+)',string)
        if key:
            if key.group(1) in self.dict_symbolRef:
                value = self.dict_symbolRef[key.group(1)]
                return bin(int(value,10))[2:].zfill(16)

        key = re.search(r'\@(\d+)',string)
        if key:
            value = key.group(1)
            return bin(int(value,10))[2:].zfill(16)

        return "----sth-gose--wrong----" 

    #C-instruction analysys
    def __C_inst_parsing(self,string):
        #print(self.cur_instruction)
        dest = ''
        comp = ''
        jmp = ''
        key = re.search(r'([A,M,D]+)\s*=\s*([-,+,!,D,M,A,&,|,1,0]+)',string)
        if key:
            #print(key.group(1)+"---"+key.group(2))
            if (key.group(1) in self.dict_destRef) and \
                (key.group(2) in self.dict_compRef):
                dest = self.dict_destRef[key.group(1)]
                comp = self.dict_compRef[key.group(2)]
                jmp = '000'
            #print("inst is :"+"111"+comp+dest+jmp)
            return ("111"+comp+dest+jmp)
        key = re.search(r'([-,+,!,D,M,A,&,|,1,0]+)\s*;\s*(J\w{2})',string)
        if key:
            #print(key.group(1)+"---"+key.group(2))
            if ((key.group(1) in self.dict_compRef) and \
                (key.group(2) in self.dict_jmpRef)):
                dest = "000"
                comp = self.dict_compRef[key.group(1)]
                jmp = self.dict_jmpRef[key.group(2)]
            #print("inst is :"+"111"+comp+dest+jmp)
            return ("111"+comp+dest+jmp)

        print("Get C-inst paser error.")
        return "----sth-gose--wrong----" 

print("hello!")
import symbol_reader
s = symbol_reader.hackAsmSymbolReader()
a = asmReader("./AsmCodes/Max.tmp")

print(s.asmSymbols)
a.dict_symbolRef = s.asmSymbols
a.dict_compRef = s.asmComp
a.dict_jmpRef = s.asmJmp
a.dict_destRef = s.asmDest

a.asmTranslator()