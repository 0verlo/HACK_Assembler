#!/usr/bin/env python3
# coding=utf-8
import sys
import json

class jsonReader(object):
    def __init__(self,fileName):
        self.total_symbol = dict()
        self.__fileName = fileName
        self.__map_init()
        
    #get HACK default map for pattern convent
    def __map_init(self):
       json_file = open(self.__fileName,'r')
       self.total_symbol = json.loads(json_file.read())
       #print(self.total_symbol)

    def incode_symbol_builder(self):
        pass

class hackAsmSymbolReader(jsonReader):
    def __init__(self,fileName):
        super().__init__("hack_asm_symbols.json")
        self.asmSymbols = self.total_symbol[3]
        self.asmComp = self.total_symbol[0]
        self.asmDest = self.total_symbol[1]
        self.asmJmp = self.total_symbol[2]
        self.__symbol_builder(fileName):

    #label analysis
    def __symbol_table_write(self):
        pass
        #print(self.cur_instruction)
        #key = re.search(r'\(([\w\.\_\$]+)\)',self.cur_instruction).group(1)
        #self.__symbol_table[key] = str(self.code_line+1)
        #print(key+" in line:"+str(self.code_line))

    def __symbol_builder(self,fileName):
        print(self.total_symbol[3])
        pass
        #first_round = open(file_name,'r')
        #for line in first_round:
        #    self.__str_preprocess(line.strip())
        #    if(0 == self.cur_type):
        #        self.__symbol_table_write()
        ##print(self.__symbol_table)
        #first_round.close()
        #self.cur_line = -1
        #self.code_line = -1

symbol_read = hackAsmSymbolReader("hello")
symbol_read.symbol_builder()


