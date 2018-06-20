#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile

def editTurb (dirname, turbmodel):
    subprocess.run(["cp -f $FOAM_TUTORIALS/incompressible/simpleFoam/motorBike/constant/turbulenceProperties "+\
                    dirname+"/constant"],shell=True)
    os.chdir(dirname+"/constant")
    print(os.getcwd())
    
    file=ParsedParameterFile("turbulenceProperties")
    if turbmodel == "laminar":
        file["simulationType"]="laminar"
        del file["RAS"]
    else:
        file["simulationType"]="RAS"
        file["RAS"]={"RASModel":turbmodel,"turbulence":"on","printCoeffs":"on"}
    file.writeFile()
    
def editTransport (dirname, transportmodel):
    subprocess.run(["cp -f $FOAM_TUTORIALS/incompressible/simpleFoam/airFoil2D/constant/transportProperties "+\
                    dirname+"/constant"],shell=True)
    os.chdir(dirname+"/constant")
    
    lines=[]
    with open("transportProperties","r") as file:
        data=file.readlines()
        lines=list(data)
        idx=lines.index('transportModel  Newtonian;\n')
        lines[idx]='transportModel  '+transportmodel+";\n"
        mod_data=' '.join(lines)
        file.close()
    
    with open("transportProperties","w") as file:
        file.write(mod_data)
        file.close()
        
def editMatProperties (dirname, rho, nu):
    os.chdir(dirname+"/constant")
    
    lines=[]
    with open("transportProperties","r") as file:
        data=file.readlines()
        lines=list(data)
        idx1=lines.index(' rho             [1 -3 0 0 0 0 0] 1;\n')
        idx2=lines.index(' nu              [0 2 -1 0 0 0 0] 1e-05;\n')
        print(idx1,idx2)
        lines[idx1]=' rho             [1 -3 0 0 0 0 0] '+str(rho)+";\n"
        lines[idx2]=' nu              [0 2 -1 0 0 0 0] '+str(nu)+";\n"
        mod_data=' '.join(lines)
        file.close()
    
    with open("transportProperties","w") as file:
        file.write(mod_data)
        file.close()
    
    
    
    
    
    
    
    
