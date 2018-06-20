#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess

def writePdict (dirname, Patch_name, P_BoundCond):
    if P_BoundCond[0] == "freestreamPressure":
        subprocess.run(['pyFoamCreateBoundaryPatches.py --verbose --overwrite --filter="'+Patch_name+\
                        '" '+'--default="'+"{'type':'"+P_BoundCond[0]+"'}"+'" '+dirname+'/0/p'], shell=True)
    
    elif P_BoundCond[0] == "fixedValue" or P_BoundCond[0] == "totalPressure":
        subprocess.run(['pyFoamCreateBoundaryPatches.py --verbose --overwrite --filter="'+Patch_name+\
                        '" '+'--default="'+"{'type':'"+P_BoundCond[0]+"','value':"+"'uniform "+str(P_BoundCond[1])+"'}"+'" '+\
                        dirname+'/0/p'], shell=True)
        
    elif P_BoundCond[0] == "symmetryPlane":
        subprocess.run(['pyFoamCreateBoundaryPatches.py --verbose --overwrite --filter="'+Patch_name+\
                        '" '+'--default="'+"{'type':'"+P_BoundCond[0]+"'}"+'" '+dirname+'/0/p'], shell=True)
    
    elif P_BoundCond[0] == "zeroGradient":
        subprocess.run(['pyFoamCreateBoundaryPatches.py --verbose --overwrite --filter="'+Patch_name+\
                        '" '+'--default="'+"{'type':'"+P_BoundCond[0]+"'}"+'" '+dirname+'/0/p'], shell=True)
    
    elif P_BoundCond[0] == "empty":
        subprocess.run(['pyFoamCreateBoundaryPatches.py --verbose --overwrite --filter="'+Patch_name+\
                        '" '+'--default="'+"{'type':'"+P_BoundCond[0]+"'}"+'" '+dirname+'/0/p'], shell=True)

def writeUdict (dirname, Patch_name, U_BoundCond):
        
    if U_BoundCond[0] == "fixedValue" or U_BoundCond[0] == "pressureInletOutletVelocity":
        subprocess.run(['pyFoamCreateBoundaryPatches.py --verbose --overwrite --filter="'+Patch_name+\
                        '" '+'--default="'+"{'type':'"+U_BoundCond[0]+"','value':"+"'uniform ("+str(U_BoundCond[1])+\
                        ' '+str(U_BoundCond[2])+' '+str(U_BoundCond[3])+")'}"+'" '+dirname+'/0/U'], shell=True)
    
    elif U_BoundCond[0] == "inletOutlet":
        subprocess.run(['pyFoamCreateBoundaryPatches.py --verbose --overwrite --filter="'+Patch_name+\
                        '" '+'--default="'+"{'type':'"+U_BoundCond[0]+"','inletValue':"+"'uniform ("+str(U_BoundCond[1])+' '+str(U_BoundCond[2])+' '+str(U_BoundCond[3])+\
                        ")','value':"+"'uniform ("+str(U_BoundCond[4])+' '+str(U_BoundCond[5])+' '+str(U_BoundCond[6])+")'}"+'" '+dirname+'/0/U'], shell=True)
    
    elif U_BoundCond[0] == "freestream":
        subprocess.run(['pyFoamCreateBoundaryPatches.py --verbose --overwrite --filter="'+Patch_name+\
                        '" '+'--default="'+"{'type':'"+U_BoundCond[0]+"','freestreamValue':"+"'uniform ("+str(U_BoundCond[1])+\
                        ' '+str(U_BoundCond[2])+' '+str(U_BoundCond[3])+")'}"+'" '+dirname+'/0/U'], shell=True)
        
    elif U_BoundCond[0] == "symmetryPlane":
        subprocess.run(['pyFoamCreateBoundaryPatches.py --verbose --overwrite --filter="'+Patch_name+\
                        '" '+'--default="'+"{'type':'"+U_BoundCond[0]+"'}"+'" '+dirname+'/0/U'], shell=True)
    
    elif U_BoundCond[0] == "zeroGradient":
        subprocess.run(['pyFoamCreateBoundaryPatches.py --verbose --overwrite --filter="'+Patch_name+\
                        '" '+'--default="'+"{'type':'"+U_BoundCond[0]+"'}"+'" '+dirname+'/0/U'], shell=True)
    
    elif U_BoundCond[0] == "noSlip":
        subprocess.run(['pyFoamCreateBoundaryPatches.py --verbose --overwrite --filter="'+Patch_name+\
                        '" '+'--default="'+"{'type':'"+U_BoundCond[0]+"'}"+'" '+dirname+'/0/U'], shell=True)
    
    elif U_BoundCond[0] == "empty":
        subprocess.run(['pyFoamCreateBoundaryPatches.py --verbose --overwrite --filter="'+Patch_name+\
                        '" '+'--default="'+"{'type':'"+U_BoundCond[0]+"'}"+'" '+dirname+'/0/U'], shell=True)
    
def write_k_dict (dirname,Patch_name,k_BoundCond):
    if k_BoundCond[0] == "fixedValue" or k_BoundCond[0] == "kqRWallFunction":
        subprocess.run(['pyFoamCreateBoundaryPatches.py --verbose --overwrite --filter="'+Patch_name+\
                        '" '+'--default="'+"{'type':'"+k_BoundCond[0]+"','value':"+"'uniform "+str(k_BoundCond[1])+"'}"+'" '+\
                        dirname+'/0/k'], shell=True)
    
    elif k_BoundCond[0] == "inletOutlet":
        subprocess.run(['pyFoamCreateBoundaryPatches.py --verbose --overwrite --filter="'+Patch_name+\
                        '" '+'--default="'+"{'type':'"+k_BoundCond[0]+"','inletValue':'uniform 0','value':'uniform "+str(k_BoundCond[1])+"'}"+'" '+\
                        dirname+'/0/k'], shell=True)
    
    else:
        subprocess.run(['pyFoamCreateBoundaryPatches.py --verbose --overwrite --filter="'+Patch_name+\
                        '" '+'--default="'+"{'type':'"+k_BoundCond[0]+"'}"+'" '+dirname+'/0/k'], shell=True)
    
def write_epsilon_dict (dirname,Patch_name,epsilon_BoundCond):
    if epsilon_BoundCond[0] == "fixedValue" or epsilon_BoundCond[0] == "epsilonWallFunction":
        subprocess.run(['pyFoamCreateBoundaryPatches.py --verbose --overwrite --filter="'+Patch_name+\
                        '" '+'--default="'+"{'type':'"+epsilon_BoundCond[0]+"','value':"+"'uniform "+str(epsilon_BoundCond[1])+"'}"+'" '+\
                        dirname+'/0/epsilon'], shell=True)
    
    elif epsilon_BoundCond[0] == "inletOutlet":
        subprocess.run(['pyFoamCreateBoundaryPatches.py --verbose --overwrite --filter="'+Patch_name+\
                        '" '+'--default="'+"{'type':'"+epsilon_BoundCond[0]+"','inletValue':'uniform 0','value':'uniform "+str(epsilon_BoundCond[1])+"'}"+'" '+\
                        dirname+'/0/k'], shell=True)
    
    else:
        subprocess.run(['pyFoamCreateBoundaryPatches.py --verbose --overwrite --filter="'+Patch_name+\
                        '" '+'--default="'+"{'type':'"+epsilon_BoundCond[0]+"'}"+'" '+dirname+'/0/epsilon'], shell=True)
    
def write_omega_dict (dirname,Patch_name,omega_BoundCond):
    if omega_BoundCond[0] == "fixedValue" or omega_BoundCond[0] == "omegaWallFunction":
        subprocess.run(['pyFoamCreateBoundaryPatches.py --verbose --overwrite --filter="'+Patch_name+\
                        '" '+'--default="'+"{'type':'"+omega_BoundCond[0]+"','value':"+"'uniform "+str(omega_BoundCond[1])+"'}"+'" '+\
                        dirname+'/0/omega'], shell=True)
    
    elif omega_BoundCond[0] == "inletOutlet":
        subprocess.run(['pyFoamCreateBoundaryPatches.py --verbose --overwrite --filter="'+Patch_name+\
                        '" '+'--default="'+"{'type':'"+omega_BoundCond[0]+"','inletValue':'uniform 0','value':'uniform "+str(omega_BoundCond[1])+"'}"+'" '+\
                        dirname+'/0/k'], shell=True)
    
    else:
        subprocess.run(['pyFoamCreateBoundaryPatches.py --verbose --overwrite --filter="'+Patch_name+\
                        '" '+'--default="'+"{'type':'"+omega_BoundCond[0]+"'}"+'" '+dirname+'/0/omega'], shell=True)
    
def write_nut_dict (dirname,Patch_name,nut_BoundCond):
    if nut_BoundCond[0] == "calculated" or nut_BoundCond[0] == "nutkWallFunction":
        subprocess.run(['pyFoamCreateBoundaryPatches.py --verbose --overwrite --filter="'+Patch_name+\
                        '" '+'--default="'+"{'type':'"+nut_BoundCond[0]+"','value':"+"'uniform "+str(nut_BoundCond[1])+"'}"+'" '+\
                        dirname+'/0/nut'], shell=True)
    
    elif nut_BoundCond[0] == "freestream":
        subprocess.run(['pyFoamCreateBoundaryPatches.py --verbose --overwrite --filter="'+Patch_name+\
                        '" '+'--default="'+"{'type':'"+nut_BoundCond[0]+"','freestreamValue':"+"'uniform "+str(nut_BoundCond[1])+"'}"+'" '+\
                        dirname+'/0/nut'], shell=True)
    
    else:
        subprocess.run(['pyFoamCreateBoundaryPatches.py --verbose --overwrite --filter="'+Patch_name+\
                        '" '+'--default="'+"{'type':'"+nut_BoundCond[0]+"'}"+'" '+dirname+'/0/nut'], shell=True)
    
def write_nuTilda_dict (dirname,Patch_name,nuTilda_BoundCond):
    if nuTilda_BoundCond[0] == "fixedValue":
        subprocess.run(['pyFoamCreateBoundaryPatches.py --verbose --overwrite --filter="'+Patch_name+\
                        '" '+'--default="'+"{'type':'"+nuTilda_BoundCond[0]+"','value':"+"'uniform "+str(nuTilda_BoundCond[1])+"'}"+'" '+\
                        dirname+'/0/nuTilda'], shell=True)
    
    elif nuTilda_BoundCond[0] == "freestream":
        subprocess.run(['pyFoamCreateBoundaryPatches.py --verbose --overwrite --filter="'+Patch_name+\
                        '" '+'--default="'+"{'type':'"+nuTilda_BoundCond[0]+"','freestreamValue':"+"'uniform "+str(nuTilda_BoundCond[1])+"'}"+'" '+\
                        dirname+'/0/nuTilda'], shell=True)
    
    else:
        subprocess.run(['pyFoamCreateBoundaryPatches.py --verbose --overwrite --filter="'+Patch_name+\
                        '" '+'--default="'+"{'type':'"+nuTilda_BoundCond[0]+"'}"+'" '+dirname+'/0/nuTilda'], shell=True)
    
        
    
        
        
    