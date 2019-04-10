#!/usr/bin/env python
# coding=utf-8
import 

class asmReader(object):
    def __init__(self,file_name):
        key = re.search(r'((\.\/|\/)(\w+\/)*(\w+)).asm',file_name)
        if not(key):
            return
        self.inCodeSymbols = dict()
        self.__output_tmp = (key.group(1)+".tmp")
        self.__symbol_reader(file_name)
        self.__output_name = (key.group(1)+".hack")

    def __symbol_reader(self):
        fileReader = open(file_name,'r')
        fileWriter = open(self.__output_tmp,'r')
        self.__output_name = 
        for line in fileReader:
            self.cur_line = self.cur_line + 1
            #print('in'+str(self.cur_line))
            self.__str_preprocess(line.strip())
            if(0 == self.cur_type):
                self.__symbol_table_write()
        #print(self.__symbol_table)
        first_round.close()
        self.cur_line = -1
        self.code_line = -1
        