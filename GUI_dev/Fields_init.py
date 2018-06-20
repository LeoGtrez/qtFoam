#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 16 03:37:06 2018

@author: leonard
"""
import subprocess

def writePFieldInit (dirname, Pval):
    subprocess.run(["pyFoamWriteDictionary.py --strip-quotes-from-value "+dirname+"/0/p internalField 'uniform "+str(Pval)+"'"], shell=True)
    
def writeUFieldInit (dirname, Uval):
    subprocess.run(["pyFoamWriteDictionary.py --strip-quotes-from-value "+dirname+"/0/U internalField 'uniform ("+str(Uval[0])+" "+str(Uval[1])+" "+str(Uval[2])+")'"], shell=True)
    
def writekFieldInit (dirname, kval):
    subprocess.run(["pyFoamWriteDictionary.py --strip-quotes-from-value "+dirname+"/0/k internalField 'uniform "+str(kval)+"'"], shell=True)
    
def writeEpsilonFieldInit (dirname, epsilonval):
    subprocess.run(["pyFoamWriteDictionary.py --strip-quotes-from-value "+dirname+"/0/epsilon internalField 'uniform "+str(epsilonval)+"'"], shell=True)
    
def writeOmegaFieldInit (dirname, omegaval):
    subprocess.run(["pyFoamWriteDictionary.py --strip-quotes-from-value "+dirname+"/0/omega internalField 'uniform "+str(omegaval)+"'"], shell=True)
    
def writeNutFieldInit (dirname, nutval):
    subprocess.run(["pyFoamWriteDictionary.py --strip-quotes-from-value "+dirname+"/0/nut internalField 'uniform "+str(nutval)+"'"], shell=True)
    
def writeNuTildaFieldInit (dirname, nuTildaval):
    subprocess.run(["pyFoamWriteDictionary.py --strip-quotes-from-value "+dirname+"/0/nuTilda internalField 'uniform "+str(nuTildaval)+"'"], shell=True)
    
    
    
    
    
