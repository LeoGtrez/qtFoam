#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile
import subprocess
from PyQt5.QtWidgets import QMessageBox, QFileDialog


def GenerateBlockMesh (VertList,NumVerts,EdgeType,EdgeVertNum,InterpolPoints,DataBlock,gradType, \
                       VfacesBound,PatchInfo,NumBounds,dirname):
    subprocess.run(["cp -f $FOAM_TUTORIALS/incompressible/simpleFoam/motorBike/system/blockMeshDict "+\
                    dirname+"/system"],shell=True)
    os.chdir(dirname+"/system")
    #print(os.getcwd())
    file=ParsedParameterFile("blockMeshDict")
   
    #write vertices coordinates:
    if NumVerts < len(file["vertices"]):
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
    k=0
    vertperBound=[]
    vertices=[" "]*NumBounds
    print(vertices)
    for i in range(NumBounds):
        if (k+PatchInfo[(i*3)+2]) == len(VfacesBound):
            vertperBound.append(VfacesBound[k:])
        else:
            vertperBound.append(VfacesBound[k:k+PatchInfo[(i*3)+2]])
            k=k+PatchInfo[(i*3)+2]
    print(vertperBound)
        
    for i in range(NumBounds):
        for j in range(len(vertperBound[i])):
            #print(vertperBound[i][j][0])
            vertices[i]=vertices[i]+"("+str(vertperBound[i][j][0])+\
            " "+str(vertperBound[i][j][1])+\
            " "+str(vertperBound[i][j][2])+\
            " "+str(vertperBound[i][j][3])+")\n            "
    print(vertices)
    
    for i in range(len(file["boundary"])):
        del file["boundary"][-1]
    for i in range(NumBounds-1):
        #file["boundary"].append(str(PatchInfo[i][:]))
        file["boundary"].append(PatchInfo[i*3]+"\n"
             "    { \n"
             "      type "+PatchInfo[(i*3)+1]+"; \n"
             "      faces \n"
             "      ( \n"
             "           " +vertices[i]+
             "\n"
             "      ); \n"
             "    }")
   
    #generating blockMeshDict
    file.writeFile()
   
    #Generating base Mesh with command "blockMesh"
    os.chdir(dirname)
    
    try:
        subprocess.run(['blockMesh'], shell=True, check=True)
         #Update field dictionaries p and U
        subprocess.run(["pyFoamCreateBoundaryPatches.py --verbose --fix-types "+\
                        dirname+"/0/p"],shell=True)
        subprocess.run(["pyFoamCreateBoundaryPatches.py --verbose --clear-unused "+\
                        dirname+"/0/p"],shell=True)
        subprocess.run(["pyFoamCreateBoundaryPatches.py --verbose --fix-types "+\
                        dirname+"/0/U"],shell=True)
        subprocess.run(["pyFoamCreateBoundaryPatches.py --verbose --clear-unused "+\
                        dirname+"/0/U"],shell=True)
    except:
        blockmesh_exception()
    else:
        blockmesh_success()
     
        
def blockmesh_exception():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText("Error when generating base Mesh (blockMesh)!\n"+ \
                "Set mesh parameters and generate again!")
    #msg.setInformativeText("This is additional information")
    msg.setWindowTitle("Error in mesh generation")
    msg.setStandardButtons(QMessageBox.Ok)
    retval = msg.exec_()
    print("value of pressed message box button:", retval)
       
def blockmesh_success():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText("Base mesh (blockMesh) has been generated with success!")
    #msg.setInformativeText("This is additional information")
    msg.setWindowTitle("blockMesh generated")
    msg.setStandardButtons(QMessageBox.Ok)
    retval = msg.exec_()
    print("value of pressed message box button:", retval)
   
def PreviewMesh (dirname):
    os.chdir(dirname)
    print(os.getcwd())
    subprocess.Popen(["paraFoam"])
    
def BrowseCADFile ():
    dlg = QFileDialog()
    dlg.setWindowTitle("Select existing CAD file (.stl, .nas or .obj)")
    dlg.setFileMode(QFileDialog.AnyFile)
    dlg.setNameFilter("CAD files (*.stl *.nas *.obj)")
    #dlg.setFilter("CAD files (*.stl *.nas *.obj )")
    if dlg.exec_():
        global CADfile_url
        CADfile_url = dlg.selectedFiles()
        print(CADfile_url)
        CADfile_name=CADfile_url[0].rpartition("/")[2]
        print(CADfile_name)
    return (CADfile_url[0], CADfile_name)

def CopyCADFile (url,name, dirname):
    try:
        subprocess.run(["cp "+url+" "+dirname+"/constant/triSurface/"+name], shell=True, check=True)
    except:
        copycadfile_exception(dirname)
    else:
        copycadfile_success(dirname)

def copycadfile_exception (dirname):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText("Error when copying CAD file to "+dirname+"/constant/triSurface")
    #msg.setInformativeText("This is additional information")
    msg.setWindowTitle("Error when loading geometry")
    msg.setStandardButtons(QMessageBox.Ok)
    retval = msg.exec_()
    print("value of pressed message box button:", retval)
    
def copycadfile_success (dirname):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText("Geometry copied with succes in "+dirname+"/constant/triSurface")
    #msg.setInformativeText("This is additional information")
    msg.setWindowTitle("Geometry loaded")
    msg.setStandardButtons(QMessageBox.Ok)
    retval = msg.exec_()
    print("value of pressed message box button:", retval)
    
def CreateSurfExtDict (CADname, dirname, Data):
    subprocess.call(["cp -f $FOAM_TUTORIALS/incompressible/simpleFoam/motorBike/system/surfaceFeatureExtractDict "\
                     +dirname+"/system"], shell=True)
    os.chdir(dirname+"/system")
    file=ParsedParameterFile("surfaceFeatureExtractDict")
    
    #Set IncludedAngle:
    if CADname != "motorBike.obj":
        file[CADname]=file["motorBike.obj"]
        del file["motorBike.obj"]
    file[CADname]["extractFromSurfaceCoeffs"]={"includedAngle":Data[0]}
    #Set "keep non manifold edges" and "keep open edges":
    file[CADname]["subsetFeatures"]["nonManifoldEdges"]=" ".join(Data[1])
    file[CADname]["subsetFeatures"]["openEdges"]=" ".join(Data[2])
    
    #generating surfaceFeatureExtractDict
    file.writeFile()
    
def Generate_eMesh (dirname):
    os.chdir(dirname)
    try:
        subprocess.run(["surfaceFeatureExtract"], shell=True, check=True)
    except:
        generate_emesh_exception(dirname)
    else:
        generate_emesh_success(dirname)
        
def generate_emesh_exception(dirname):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText("Error when generating .eMesh file in "+dirname+"/constant/triSurface\n"+\
                "Try to load the geometry again!")
    #msg.setInformativeText("This is additional information")
    msg.setWindowTitle("Error when generating Edge Features file")
    msg.setStandardButtons(QMessageBox.Ok)
    retval = msg.exec_()
    print("value of pressed message box button:", retval)
    
def generate_emesh_success(dirname):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText(".eMesh file generated with succes in "+dirname+"/constant/triSurface")
    #msg.setInformativeText("This is additional information")
    msg.setWindowTitle("Edge Features file .eMesh generated")
    msg.setStandardButtons(QMessageBox.Ok)
    retval = msg.exec_()
    print("value of pressed message box button:", retval)
    
def viewCAD (CADname, dirname):
    os.chdir(dirname+"/constant/triSurface")
    print(os.getcwd())
    subprocess.run(["paraview "+CADname],shell=True)

def GenerateSnappyHexMesh (dirname, Steps, CADname, BoxMinPoint, BoxMaxPoint, CMData, SnapData, \
                           AddLayerData):
    subprocess.run(["cp -f $FOAM_TUTORIALS/incompressible/simpleFoam/motorBike/system/snappyHexMeshDict "+\
                    dirname+"/system"],shell=True)
    os.chdir(dirname+"/system")
    file=ParsedParameterFile("snappyHexMeshDict")
    
    #Set Steps to run:
    file["castellatedMesh"]=" ".join(Steps[0])
    file["snap"]=" ".join(Steps[1])
    file["addLayers"]=" ".join(Steps[2])
    
    #Geometry definition:
    name=CADname.rpartition(".")[0]
    if name != "motorBike":
        file["geometry"][name]=file["geometry"]["motorBike"]
        del file["geometry"]["motorBike"]
    file["geometry"][name]["file"]='"'+CADname+'"'
    if BoxMinPoint == [] and BoxMaxPoint ==[]:
        del file["geometry"]["refinementBox"]
    else:
        file["geometry"]["refinementBox"]["min"]="("+str(BoxMinPoint[0])+" "+str(BoxMinPoint[1])+" "+str(BoxMinPoint[2])+")"
        file["geometry"]["refinementBox"]["max"]="("+str(BoxMaxPoint[0])+" "+str(BoxMaxPoint[1])+" "+str(BoxMaxPoint[2])+")"
    
    #Set castellated Mesh Controls:
    if " ".join(Steps[0]) == "true":
        eMesh='"'+name+'.eMesh"'
        FreeStanding=" ".join(CMData[-1])
        #mode inside / outside / no refinement box:
        if CMData[5][5] == "inside" or CMData[5][5] == "outside":
            if BoxMinPoint == [] and BoxMaxPoint ==[]:
                file["castellatedMeshControls"]={\
                    "maxLocalCells":CMData[0],\
                    "maxGlobalCells":CMData[1],\
                    "minRefinementCells":CMData[2],\
                    "maxLoadUnbalance":CMData[3],\
                    "nCellsBetweenLevels":CMData[4],\
                    "features":[{"file":eMesh, "level":CMData[5][0]}],\
                    "refinementSurfaces":{name:{"level":[CMData[5][1],CMData[5][2]],"patchInfo":{"type":CMData[5][3],"inGroups":[name+"Group"]}}},\
                    "resolveFeatureAngle":CMData[5][4],\
                    "refinementRegions":{},\
                    "locationInMesh":[CMData[6][0],CMData[6][1],CMData[6][2]],\
                    "allowFreeStandingZoneFaces":FreeStanding}
            else:
                file["castellatedMeshControls"]={\
                    "maxLocalCells":CMData[0],\
                    "maxGlobalCells":CMData[1],\
                    "minRefinementCells":CMData[2],\
                    "maxLoadUnbalance":CMData[3],\
                    "nCellsBetweenLevels":CMData[4],\
                    "features":[{"file":eMesh, "level":CMData[5][0]}],\
                    "refinementSurfaces":{name:{"level":[CMData[5][1],CMData[5][2]],"patchInfo":{"type":CMData[5][3],"inGroups":[name+"Group"]}}},\
                    "resolveFeatureAngle":CMData[5][4],\
                    "refinementRegions":{"refinementBox":{"mode":CMData[5][5],"levels":[[CMData[6][0],CMData[6][1]]]}},\
                    "locationInMesh":[CMData[7][0],CMData[7][1],CMData[7][2]],\
                    "allowFreeStandingZoneFaces":FreeStanding}
        else:
            file["castellatedMeshControls"]={\
                "maxLocalCells":CMData[0],\
                "maxGlobalCells":CMData[1],\
                "minRefinementCells":CMData[2],\
                "maxLoadUnbalance":CMData[3],\
                "nCellsBetweenLevels":CMData[4],\
                "features":[{"file":eMesh, "level":CMData[5][0]}],\
                "refinementSurfaces":{name:{"level":[CMData[5][1],CMData[5][2]],"patchInfo":{"type":CMData[5][3],"inGroups":[name+"Group"]}}},\
                "resolveFeatureAngle":CMData[5][4],\
                "refinementRegions":{"refinementBox":{"mode":CMData[5][5],"levels":[[CMData[6][0],CMData[6][1],CMData[6][2],CMData[6][3]]]}},\
                "locationInMesh":[CMData[7][0],CMData[7][1],CMData[7][2]],\
                "allowFreeStandingZoneFaces":FreeStanding}
    
        print(file["castellatedMeshControls"])
    
    #Set Snap Controls:
    if " ".join(Steps[1]) == "true":
        implicitFeat=str(SnapData[5])[2:-2:1]
        explicitFeat=str(SnapData[6])[2:-2:1]
    
        file["snapControls"]={\
            "nSmoothPatch":SnapData[0],\
            "tolerance":SnapData[1],\
            "nSolveIter":SnapData[2],\
            "nRelaxIter":SnapData[3],\
            "nFeatureSnapIter":SnapData[4],\
            "implicitFeatureSnap":implicitFeat,\
            "explicitFeatureSnap":explicitFeat,\
            "multiRegionFeatureSnap":'false'}
    
        print(file["snapControls"])

    #Set Snap Controls, some parameters are left by default:
    if " ".join(Steps[2]) == "true":
        Layers='"('+name+"|"+str(AddLayerData[3][0])[2:-2:1]+').*"'
        for j in range(1,len(AddLayerData[3])):
            Layers=Layers[0:-4:1]
            Layers+="|"+str(AddLayerData[3][j])[2:-2:1]+').*"'
    
        file["addLayersControls"]={\
            "relativeSizes":'true',\
            "layers":{Layers:{"nSurfaceLayers":AddLayerData[-1]}},\
            "expansionRatio":AddLayerData[0],\
            "finalLayerThickness":AddLayerData[1],\
            "minThickness":AddLayerData[2],\
            "nGrow":0,\
            "featureAngle":60,\
            "slipFeatureAngle":30,\
            "nRelaxIter":3,\
            "nSmoothSurfaceNormals":1,\
            "nSmoothNormals":3,\
            "nSmoothThickness":10,\
            "maxFaceThicknessRatio":0.5,\
            "maxThicknessToMedialRatio":0.3,\
            "minMedianAxisAngle":90,\
            "nBufferCellsNoExtrude":0,\
            "nLayerIter":50}
        print(file["addLayersControls"])
    
    file.writeFile()
    
    #Generating snappyHexMesh with command "snappyHexMesh"
    os.chdir(dirname)
    
    try:
        subprocess.run(['gnome-terminal -x sh -c "snappyHexMesh -overwrite; bash"'], shell=True, check=True)
    except:
        snappymesh_exception()
    else:
        pass
        #snappymesh_success()

def snappymesh_exception():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText("Error when generating snappyHexMesh!\n"+ \
                "Set snappyHexMesh parameters and generate again!")
    #msg.setInformativeText("This is additional information")
    msg.setWindowTitle("Error in snappyHexMesh generation")
    msg.setStandardButtons(QMessageBox.Ok)
    retval = msg.exec_()
    print("value of pressed message box button:", retval)
    
def snappymesh_success():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText("snappyHexMesh has been generated with success!")
    #msg.setInformativeText("This is additional information")
    msg.setWindowTitle("snappyHexMesh generated")
    msg.setStandardButtons(QMessageBox.Ok)
    retval = msg.exec_()
    print("value of pressed message box button:", retval)
    
#Convert Mesh:
def SearchMeshFile():
    dlg = QFileDialog()
    dlg.setWindowTitle("Select existing Mesh file (.msh, .neu, .ans or .geo)")
    dlg.setFileMode(QFileDialog.AnyFile)
    dlg.setNameFilter("Mesh files (*.msh *.neu *.ans *.geo)")
    #dlg.setFilter("CAD files (*.stl *.nas *.obj )")
    if dlg.exec_():
        global Meshfile_url
        Meshfile_url = dlg.selectedFiles()
        print(Meshfile_url)
        Meshfile_name=Meshfile_url[0].rpartition("/")[2]
        print(Meshfile_name)
    return (Meshfile_url[0], Meshfile_name)

def ConvertMeshFile(dirname,Meshfile_url,Meshfile_name):
    os.chdir(dirname)
    if Meshfile_name.endswith('.msh'):
        try:
            subprocess.run(["fluentMeshToFoam "+Meshfile_url], shell=True, check=True)
        except:
            convertmesh_exception()
        else:
            convertmesh_success()
    elif Meshfile_name.endswith(".neu"):
        try:
            subprocess.run(["gambitToFoam "+Meshfile_url], shell=True, check=True)
        except:
            convertmesh_exception()
        else:
            convertmesh_success()
    elif Meshfile_name.endswith(".ans"):
        try:
            subprocess.run(["ideasToFoam "+Meshfile_url], shell=True, check=True)
        except:
            convertmesh_exception()
        else:
            convertmesh_success()
    else:
        try:
            subprocess.run(["cfx4ToFoam "+Meshfile_url], shell=True, check=True)
        except:
            convertmesh_exception()
        else:
            convertmesh_success()
        
def convertmesh_exception():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText("Error when converting Mesh file\n"+ \
                "Check origin of the mesh file and try again!")
    #msg.setInformativeText("This is additional information")
    msg.setWindowTitle("Error in Mesh file conversion")
    msg.setStandardButtons(QMessageBox.Ok)
    retval = msg.exec_()
    print("value of pressed message box button:", retval)
    
def convertmesh_success():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText("Mesh file has been converted with success!")
    #msg.setInformativeText("This is additional information")
    msg.setWindowTitle("Mesh file conversion")
    msg.setStandardButtons(QMessageBox.Ok)
    retval = msg.exec_()
    print("value of pressed message box button:", retval)







