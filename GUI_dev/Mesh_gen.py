#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile


def GenerateBlockMesh (VertList,NumVerts,EdgeType,EdgeVertNum,InterpolPoints,DataBlock,gradType, \
                       VfacesBound,PatchInfo,NumBounds,dirname):
   os.chdir(dirname+"/system")
   #print(os.getcwd())
   file=ParsedParameterFile("blockMeshDict")
   
   #write vertices coordinates:
   if NumVerts<len(file["vertices"]):
       for i in range(NumVerts):
           file["vertices"][i]="("+str(VertList[i][0])+" "+ str(VertList[i][1])+\
           " "+str(VertList[i][2])+")"
       for j in range(len(file["vertices"])-NumVerts):
           del file["vertices"][-1]
   else:
       for i in range(len(file["vertices"])):
           file["vertices"][i]="("+str(VertList[i][0])+" "+ str(VertList[i][1])+\
           " "+str(VertList[i][2])+")"
       for j in range(NumVerts-len(file["vertices"])):
           file["vertices"].append("("+str(VertList[j][0])+" "+ str(VertList[j][1])+\
           " "+str(VertList[j][2])+")")
   #write edges definition:
   for i in range(len(EdgeVertNum)):
       file["edges"].append(str(EdgeType)+" "+str(EdgeVertNum[i][0])+" "+str(EdgeVertNum[i][1])+ \
           " ("+str(InterpolPoints[i][0])+" "+str(InterpolPoints[i][1])+" "+str(InterpolPoints[i][2])+")")
   #write blocks definition:
   for i in range(len(file["blocks"])):
       del file["blocks"][-1]
   for i in range(len(DataBlock)):    
       file["blocks"].append("hex ("+str(DataBlock[i][0])+" "+str(DataBlock[i][1]) \
           +" "+str(DataBlock[i][2])+" "+str(DataBlock[i][3])+" "+str(DataBlock[i][4]) \
           +" "+str(DataBlock[i][5])+" "+str(DataBlock[i][6])+" "+str(DataBlock[i][7]) \
           +") ("+str(DataBlock[i][8])+" "+str(DataBlock[i][9])+" "+str(DataBlock[i][10]) \
           +") ")
       if gradType[i]=="simpleGrading":
           file["blocks"].append(gradType[i]+" ("+str(DataBlock[i][11])+" "+str(DataBlock[i][12]) \
               +" "+str(DataBlock[i][13])+") ")
       else:
           file["blocks"].append(gradType[i]+" ("+str(DataBlock[i][11])+" "+str(DataBlock[i][12]) \
               +" "+str(DataBlock[i][13])+" "+str(DataBlock[i][14])+" "+str(DataBlock[i][15]) \
               +" "+str(DataBlock[i][16])+" "+str(DataBlock[i][17])+" "+str(DataBlock[i][18]) \
               +" "+str(DataBlock[i][19])+" "+str(DataBlock[i][20])+" "+str(DataBlock[i][21]) \
               +" "+str(DataBlock[i][22])+")")
   #write boundaries definition:
   for i in range(len(file["boundary"])):
       del file["boundary"][-1]
   for i in range(NumBounds):
       #file["boundary"].append(str(PatchInfo[i][:]))
       file["boundary"].append(PatchInfo[i*2]+"\n"
            "    { \n"
            "      type "+PatchInfo[(i*2)+1]+"; \n"
            "      faces \n"
            "      ( \n"
            "           (" +str(VfacesBound[i][0])+" "+str(VfacesBound[i][1])+" "+str(VfacesBound[i][2])+" "+str(VfacesBound[i][3])+") \n"
            "      ); \n"
            "    }")
   file.writeFile()