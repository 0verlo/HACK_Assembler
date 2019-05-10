#!/usr/bin/env python3
# coding=utf-8
import sys
sys.path.append("..")
from _general._json_reader import jsonReader

class hackAsmSymbolReader(jsonReader):
    def __init__(self):
        super(hackAsmSymbolReader,self).__init__("hack_asm_symbols.json")
        self.asmSymbols = self.total_symbol[3]
        self.asmComp = self.total_symbol[0]
        self.asmDest = self.total_symbol[1]
        self.asmJmp = self.total_symbol[2]

a=hackAsmSymbolReader()

print(a.asmSymbols)
