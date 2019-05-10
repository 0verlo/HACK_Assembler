#!/usr/bin/env python3
# coding=utf-8
import sys
sys.path.append("..")
from _general._json_reader import jsonReader

class hackVMSymbolReader(jsonReader):
    def __init__(self):
        super(hackVMSymbolReader,self).__init__("hack_vm_symbols.json")
        self.vmPushPopParser = self.total_symbol[0]
        self.vmMathLogicParser = self.total_symbol[1]
        self.vmSegment = self.total_symbol[2]
        self.vmStatic = dict()

a=hackVMSymbolReader()

#print(a.vmMaping)
