#!/usr/bin/env python3
# coding=utf-8
import re

class asmPreReader(object):
    def __init__(self,file_name):
        #pick out the right path input "./xx/xx.asm" or "/xx/xx.asm"
        key = re.search(r'(^((\/)|(\.\/))(\w+\/)*(\w+)).asm',file_name)
        if not(key):
            print("Wrong file name input.")
            return
        self.inCodeSymbols = dict()
        self.__output_tmp = (key.group(1)+".tmp")
        self.__symbol_reader(file_name)

    def __symbol_reader(self,file_name):
        fileReader = open(file_name,'r')
        fileWriter = open(self.__output_tmp,'w')
        print(self.__output_tmp)
        cur_line = 0
        for line in fileReader:
            string = re.sub(r'\/\/.*','',line).strip()
            if not(string):
                continue
            if ('('==string[0]):
                key = re.search(r'\(([\w\.\_\$]+)\)',string).group(1)
                self.inCodeSymbols[key] = str(cur_line)
                print(key+" in line:"+str(cur_line))
            elif string:
                fileWriter.writelines(string+"\n")
                print(str(cur_line)+":"+string)
                cur_line = cur_line + 1

        fileWriter.close()
        fileReader.close()

a = asmPreReader("./AsmCodes/Max.asm")
print(a.inCodeSymbols)