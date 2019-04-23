#!/usr/bin/env python3
# coding=utf-8
import sys
import re
import json
import asmPreReader
import asmReader
import symbol_reader

file_name = sys.argv[1]
key = re.search(r'((\.\/|\/)(\w+\/)*(\w+)).asm',file_name)
if key:
    str_input = (key.group(1)+".asm")
    str_tmp = (key.group(1)+".tmp")
    str_output = (key.group(1)+".hack")
    sybol = symbol_reader.hackAsmSymbolReader()
    preRead = asmPreReader.asmPreReader(str_input)
    Reader = asmReader.asmReader(str_tmp)

    Reader.dict_symbolRef = sybol.asmSymbols.copy() 
    Reader.dict_symbolRef.update(preRead.inCodeSymbols)
    Reader.dict_compRef = sybol.asmComp
    Reader.dict_jmpRef = sybol.asmJmp
    Reader.dict_destRef = sybol.asmDest

    Reader.asmTranslator()

print("hello")
    