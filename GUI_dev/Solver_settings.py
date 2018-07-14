#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 16 11:59:05 2018

@author: leonard
"""

import os
import subprocess
from PyQt5.QtWidgets import QMessageBox
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile

def writeSolverApp (dirname,solver,Pot_Init,value):
    subprocess.run(["pyFoamWriteDictionary.py --strip-quotes-from-value "+dirname+"/system/controlDict "+'"'+"application"+'" '+"'"+solver+"'"], shell=True)
    if solver == "potentialFoam":
        os.chdir(dirname+"/system")
        file=ParsedParameterFile("fvSolution")
        try:
            del file['SIMPLE']
        except:
            pass
        file['potentialFlow']={'nNonOrthogonalCorrectors':int(value)}
        file.writeFile()
    elif solver == "simpleFoam":
        if Pot_Init == "Potential Flow":
            os.chdir(dirname+"/system")
            file=ParsedParameterFile("fvSolution")
            file['SIMPLE']={'nNonOrthogonalCorrectors':int(value),'consistent':'yes'}
            file.writeFile()
        else:
            os.chdir(dirname+"/system")
            file=ParsedParameterFile("fvSolution")
            try:
                del file['potentialFlow']
            except:
                pass
            try:
                del file['solvers']['Phi']
            except:
                pass
            file['SIMPLE']={'nNonOrthogonalCorrectors':int(value),'consistent':'yes'}
            file.writeFile()
            
def writeResidualsRelax (dirname,params,residuals,relaxFactors):
    params.sort(key=lambda x: x.lower())
    print(params)
    if params == ['p','U']:
        os.chdir(dirname+"/system")
        file=ParsedParameterFile("fvSolution")
        try:
            del file['solvers']['k']
        except:
            pass
        try:
            del file['solvers']['epsilon']
        except:
            pass
        try:
            del file['solvers']['omega']
        except:
            pass
        try:
            del file['solvers']['nuTilda']
        except:
            pass
        file['SIMPLE']['residualControl']={'p':residuals['p'],'U':residuals['U']}
        file['relaxationFactors']['fields']={'p':relaxFactors['p']}
        file['relaxationFactors']['equations']={'U':relaxFactors['U']}
        file.writeFile()
    elif params == ['k','omega','p','U']:
        os.chdir(dirname+"/system")
        file=ParsedParameterFile("fvSolution")
        try:
            del file['solvers']['epsilon']
        except:
            pass
        try:
            del file['solvers']['nuTilda']
        except:
            pass
        file['SIMPLE']['residualControl']={'p':residuals['p'],'U':residuals['U'],'k':residuals['k'],'omega':residuals['omega']}
        file['relaxationFactors']['fields']={'p':relaxFactors['p']}
        file['relaxationFactors']['equations']={'U':relaxFactors['U'],'k':relaxFactors['k'],'omega':relaxFactors['omega']}
        file.writeFile()
    elif params == ['epsilon','k','p','U']:
        os.chdir(dirname+"/system")
        file=ParsedParameterFile("fvSolution")
        try:
            del file['solvers']['omega']
        except:
            pass
        try:
            del file['solvers']['nuTilda']
        except:
            pass
        file['SIMPLE']['residualControl']={'p':residuals['p'],'U':residuals['U'],'k':residuals['k'],'epsilon':residuals['epsilon']}
        file['relaxationFactors']['fields']={'p':relaxFactors['p']}
        file['relaxationFactors']['equations']={'U':relaxFactors['U'],'k':relaxFactors['k'],'epsilon':relaxFactors['epsilon']}
        file.writeFile()
    elif params == ['nuTilda','p','U']:
        os.chdir(dirname+"/system")
        file=ParsedParameterFile("fvSolution")
        try:
            del file['solvers']['k']
        except:
            pass
        try:
            del file['solvers']['epsilon']
        except:
            pass
        try:
            del file['solvers']['omega']
        except:
            pass
        file['SIMPLE']['residualControl']={'p':residuals['p'],'U':residuals['U'],'nuTilda':residuals['nuTilda']}
        file['relaxationFactors']['fields']={'p':relaxFactors['p']}
        file['relaxationFactors']['equations']={'U':relaxFactors['U'],'nuTilda':relaxFactors['nuTilda']}
        file.writeFile()
        
def writeSettingsSolvers(dirname,Param,Tol,Relax):
    if Param == "Pressure p":
        os.chdir(dirname+"/system")
        file=ParsedParameterFile("fvSolution")
        file['solvers']['p']={'solver':'GAMG','smoother':'GaussSeidel','tolerance':float(Tol),'relTol': 0.1}
        if Relax == "No":
            try:
                del file['relaxationFactors']['fields']['p']
            except:
                pass
        file.writeFile()
        
    elif Param == "Velocity potential Phi":
        os.chdir(dirname+"/system")
        file=ParsedParameterFile("fvSolution")
        file['solvers']['Phi']={'solver':'GAMG','smoother':'GaussSeidel','tolerance':float(Tol),'relTol': 0.1}
        file.writeFile()
        
    elif Param == "Velocity U":
        os.chdir(dirname+"/system")
        file=ParsedParameterFile("fvSolution")
        file['solvers']['U']={'solver':'smoothSolver','smoother':'GaussSeidel','tolerance':float(Tol),'relTol': 0.1,'nSweeps':1}
        if Relax == "No":
            try:
                del file['relaxationFactors']['equations']['U']
            except:
                pass
        file.writeFile()
        
    elif Param == "Turbulence param. k":
        os.chdir(dirname+"/system")
        file=ParsedParameterFile("fvSolution")
        file['solvers']['k']={'solver':'smoothSolver','smoother':'GaussSeidel','tolerance':float(Tol),'relTol': 0.1,'nSweeps':1}
        if Relax == "No":
            try:
                del file['relaxationFactors']['equations']['k']
            except:
                pass
        file.writeFile()
        
    elif Param == "Turbulence param. omega":
        os.chdir(dirname+"/system")
        file=ParsedParameterFile("fvSolution")
        file['solvers']['omega']={'solver':'smoothSolver','smoother':'GaussSeidel','tolerance':float(Tol),'relTol': 0.1,'nSweeps':1}
        if Relax == "No":
            try:
                del file['relaxationFactors']['equations']['omega']
            except:
                pass
        file.writeFile()
        
    elif Param == "Turbulence param. epsilon":
        os.chdir(dirname+"/system")
        file=ParsedParameterFile("fvSolution")
        file['solvers']['epsilon']={'solver':'smoothSolver','smoother':'GaussSeidel','tolerance':float(Tol),'relTol': 0.1,'nSweeps':1}
        if Relax == "No":
            try:
                del file['relaxationFactors']['equations']['epsilon']
            except:
                pass
        file.writeFile()
        
    elif Param == "Turbulence param. nuTilda":
        os.chdir(dirname+"/system")
        file=ParsedParameterFile("fvSolution")
        file['solvers']['nuTilda']={'solver':'smoothSolver','smoother':'GaussSeidel','tolerance':float(Tol),'relTol': 0.1,'nSweeps':1}
        if Relax == "No":
            del file['relaxationFactors']['equations']['nuTilda']
        file.writeFile()
        
def RUN_function (solver_name, logFile_name):
    subprocess.run(['gnome-terminal -x sh -c "pyFoamPlotRunner.py --logname='+logFile_name+" "+solver_name+'; bash"'], shell=True, check=True)

        
        