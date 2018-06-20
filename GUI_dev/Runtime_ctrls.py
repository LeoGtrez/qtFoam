#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 16 10:40:45 2018

@author: leonard
"""
import os
import subprocess
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile

def writeRCtrls (dirname,TimeSettings, WritingSettings):
    subprocess.run(["pyFoamWriteDictionary.py --strip-quotes-from-value "+dirname+"/system/controlDict "+'"'+"startFrom"+'" '+"'"+TimeSettings[0]+"'"], shell=True)
    subprocess.run(["pyFoamWriteDictionary.py --strip-quotes-from-value "+dirname+"/system/controlDict "+'"'+"startTime"+'" '+"'"+TimeSettings[1]+"'"], shell=True)
    subprocess.run(["pyFoamWriteDictionary.py --strip-quotes-from-value "+dirname+"/system/controlDict "+'"'+"stopAt"+'" '+"'"+TimeSettings[2]+"'"], shell=True)
    subprocess.run(["pyFoamWriteDictionary.py --strip-quotes-from-value "+dirname+"/system/controlDict "+'"'+"endTime"+'" '+"'"+TimeSettings[3]+"'"], shell=True)
    subprocess.run(["pyFoamWriteDictionary.py --strip-quotes-from-value "+dirname+"/system/controlDict "+'"'+"deltaT"+'" '+"'"+TimeSettings[4]+"'"], shell=True)
    subprocess.run(["pyFoamWriteDictionary.py --strip-quotes-from-value "+dirname+"/system/controlDict "+'"'+"writeControl"+'" '+"'"+WritingSettings[0]+"'"], shell=True)
    subprocess.run(["pyFoamWriteDictionary.py --strip-quotes-from-value "+dirname+"/system/controlDict "+'"'+"writeInterval"+'" '+"'"+WritingSettings[1]+"'"], shell=True)
    subprocess.run(["pyFoamWriteDictionary.py --strip-quotes-from-value "+dirname+"/system/controlDict "+'"'+"purgeWrite"+'" '+"'"+WritingSettings[2]+"'"], shell=True)
    subprocess.run(["pyFoamWriteDictionary.py --strip-quotes-from-value "+dirname+"/system/controlDict "+'"'+"writeFormat"+'" '+"'"+WritingSettings[3]+"'"], shell=True)
    subprocess.run(["pyFoamWriteDictionary.py --strip-quotes-from-value "+dirname+"/system/controlDict "+'"'+"writePrecision"+'" '+"'"+WritingSettings[4]+"'"], shell=True)
    subprocess.run(["pyFoamWriteDictionary.py --strip-quotes-from-value "+dirname+"/system/controlDict "+'"'+"writeCompression"+'" '+"'"+WritingSettings[5]+"'"], shell=True)
    subprocess.run(["pyFoamWriteDictionary.py --strip-quotes-from-value "+dirname+"/system/controlDict "+'"'+"timeFormat"+'" '+"'"+WritingSettings[6]+"'"], shell=True)
    subprocess.run(["pyFoamWriteDictionary.py --strip-quotes-from-value "+dirname+"/system/controlDict "+'"'+"timePrecision"+'" '+"'"+WritingSettings[7]+"'"], shell=True)
    
    os.chdir(dirname+"/system")
    file=ParsedParameterFile("controlDict")
    file['graphFormat']=WritingSettings[8]
    file['runtimeModifiable']=WritingSettings[9]
    file.writeFile()