#!/usr/bin/env python3
# coding=utf-8
import re

class fileDealer(object):
    def __init__(self,inputParser,outputExtension,file_name):
        key = re.search(inputParser,file_name)
        if not(key):
            print("Wrong file name input.")
            return None
        inputName = key.group(0)
        self.outputName = (key.group(1)+outputExtension)
        self.fileReader = open(inputName,'r')
        self.fileWriter = None
    
    def readNextInstruction(self):
        for line in self.fileReader:
            funcInst = re.sub(r'\/\/.*','',line).strip()
            if(funcInst):
                yield funcInst
        self.fileReader.close()

    def writeBegin(self):
        self.fileWriter = open(self.outputName,'w')

    def writeLines(self,string):
        self.fileWriter.writelines(string)

    def writeEnd(self):            
        self.fileWriter.close()

#inputParser = r'(^((\/)|(\.\/))(\w+\/)*(\w+)).asm'
#outputExtension = ".tmp"
#filename = "./Add.asm"
#
#a = fileDealer(inputParser,outputExtension,filename)
#a.writeBegin()
#try:
#    while 1:
#        line = next(a.readNextInstruction())
#        print(line)
#        a.writeLines(line+"\n")
#except StopIteration:
#    a.writeEnd()