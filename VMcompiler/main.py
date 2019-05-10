#!/usr/bin/env python3
# coding=utf-8
import sys
sys.path.append("..")
from vmReader import vmReader
from symbol_reader import hackVMSymbolReader

file_name = sys.argv[1]
a = vmReader(file_name)
b = hackVMSymbolReader()
if a and b:
    a.writeBegin()

    a.dict_vmPushpopParsers = b.vmPushPopParser.copy()
    a.dict_vmMathLogicParsers = b.vmMathLogicParser.copy()
    a.dict_vmSegment = b.vmSegment.copy()
    a.vmConvert()
    print("hello")
else:
    print("bad input")