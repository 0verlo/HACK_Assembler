#!/usr/bin/env python3
# coding=utf-8
import re
import sys
sys.path.append("..")
from _general._file_dealer import fileDealer
from symbol_reader import hackVMSymbolReader

class vmReader(fileDealer):
    def __init__(self,filename):
        #file input check
        inputParser = r'(^((\/)|(\.\/)|())(\w+\/)*(\w+)).vm'
        outputEx = ".asm"
        super(vmReader,self).__init__(inputParser,outputEx,filename)
        #Compile reference from json
        self.dict_vmSegment = dict()
        self.dict_vmPushpopParsers= dict()
        self.dict_vmMathLogicParsers= dict()
        self.dict_vmStatics = dict()
        self.int_compare_mark = 0

    def __func_PushPop(self,handle,memSegment,value):
        ##Deal with pop n push.Return asm instructions.##
        #####the specific convert rules are in .json#####

        #generalize the input
        handle = handle.lower()
        memSegment = memSegment.lower()

        #static variabl preprocess.Maping RAM addr to variable.
        if (("static" == memSegment) and \
            not(self.dict_vmStatics.get(value))):
            self.dict_vmStatics[value] = str(int(self.dict_vmSegment[memSegment])+self.dict_vmStatics.__len__())

        #for special cases
        if((("push" == handle) or ("pop" == handle)) and \
            (("temp" == memSegment) or \
            ("constant" == memSegment) or \
            ("pointer" == memSegment) or \
            ("static" == memSegment))):
            try:
                outAsm = self.dict_vmPushpopParsers[handle+" "+memSegment]
                if("pointer" == memSegment):
                    #pointer 0/1 need to be change into exact addr
                    value = str(int(self.dict_vmSegment["this"])+int(value))
                elif("static" == memSegment):
                    #static need to find the exact addr from static table.
                    value = str(self.dict_vmStatics[value])
                #just a few keywords need 2 be change
                outAsm = outAsm.replace("@value",("@"+value))
                spointer = self.dict_vmSegment["SP"]
                outAsm = outAsm.replace("@SP",("@"+spointer))
                segmentAddr = self.dict_vmSegment[memSegment]
                return outAsm.replace("@memSegment",("@"+segmentAddr))
            except KeyError:
                #XXX: Too many dict lookup mass togeter.Hard to debug.
                pass
        #for indirect segments (lcl, arg, ...)
        elif(("push" == handle) or ("pop" == handle)):
            try:
                #just a few keywords need 2 be change
                outAsm = self.dict_vmPushpopParsers[handle]
                outAsm = outAsm.replace("@value",("@"+value))
                spointer = self.dict_vmSegment["SP"]
                outAsm = outAsm.replace("@SP",("@"+spointer))
                segmentAddr = self.dict_vmSegment[memSegment]
                return outAsm.replace("@memSegment",("@"+segmentAddr))
            except KeyError:
                pass
        else:
            pass
        return ("Wrong input:"+handle+" "+memSegment+" "+value+"\n")

    def __func_MathLogic(self,handle):
        #deal with logic commands
        try:
            outAsm = self.dict_vmMathLogicParsers[handle]
            if(("eq" == handle) or ("gt" == handle) or ("lt" == handle)):
                outAsm = outAsm.replace("_forkmark",("If_"+handle+"_"+str(self.int_compare_mark)))
                outAsm = outAsm.replace("_endlogic",("End_"+handle+"_"+str(self.int_compare_mark)))
                self.int_compare_mark += 1
            spointer = self.dict_vmSegment["SP"]
            return outAsm.replace("@SP",("@"+spointer))
        except KeyError:
            print("Wrong input:"+handle+"\n")

    def vmConvert(self):
        try:
            self.writeBegin()
            while 1:
                inst = next(self.readNextInstruction())
                key = re.search(r'(\w+)(\s(\w+)\s(\d+))?',inst)
                #Group(1) is handle.Group(3) is segment.Group(4) is offset.
                if not(key):
                    #if regex get nothing
                    print("Wrong instruction input.\n")
                    continue
                elif key.group(2):
                    #case POP PUSH commands
                    print(self.__func_PushPop(key.group(1),key.group(3),key.group(4)))
                    self.writeLines(self.__func_PushPop(key.group(1),key.group(3),key.group(4)))
                elif key.group(1):
                    #case math n logic commands
                    print(self.__func_MathLogic(key.group(1)))
                    self.writeLines(self.__func_MathLogic(key.group(1)))
        except StopIteration:
            self.writeEnd()

