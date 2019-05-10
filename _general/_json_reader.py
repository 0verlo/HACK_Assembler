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
