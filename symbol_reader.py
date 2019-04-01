#!/usr/bin/env python3
# coding=utf-8
import sys
import json

class symbolReader(object):
    def __init__(self,fileName):
        self.total_symbol = dict()
        self.__fileName = fileName
        self.__map_init()
        
    #get HACK default map for pattern convent
    def __map_init(self):
       json_file = open(self.__fileName,'r')
       self.total_symbol = json.loads(json_file.read())
       #print(self.total_symbol)

class hackAsmSymbolReader(symbolReader):
    def __init__(self,fileName):
        super().__init__("hack_asm_symbols.json")
        self.__symbol_builder(fileName)
        self.asmSymbols = self.total_symbol[3]
        self.asmComp = self.total_symbol[0]
        self.asmDest = self.total_symbol[1]
        self.asmJmp = self.total_symbol[2]
    
    def __symbol_builder(self,file_name):
        first_round = open(file_name,'r')
        for line in first_round:
            self.__str_preprocess(line.strip())
            if(0 == self.cur_type):
                self.__symbol_table_write()
        #print(self.__symbol_table)
        first_round.close()
        self.cur_line = -1
        self.code_line = -1

test = hackSymbolReader()
print(1111111)
print(test.asmSymbols)
