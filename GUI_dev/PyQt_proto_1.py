#!/usr/bin/python

import sys
import os
import subprocess
import File_options as fopt
import Mesh_gen as mesh
import Properties as prop
import Bound_cond as b_cond
from PyQt5 import uic, QtWidgets

qtCreatorFile = "proto_1.ui" # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtWidgets.QTabWidget):
    def __init__(self):
        super(MyApp,self).__init__()
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        #FILE TAB
        global dirname
        dirname="text"
        self.ui.New_case.clicked.connect(self.NewDialog)
        self.ui.Load_case.clicked.connect(self.LoadDialog)
        self.ui.Exit.clicked.connect(self.closeEvent)
        # MESH TAB
        #---------blockMesh------------#
        #Vertices definition:
        global VertList,NumVerts
        VertList=[]
        NumVerts=[]
        self.ui.Add_vert.clicked.connect(self.AddVertex)
        self.ui.Reset_vert.clicked.connect(self.ResetVertex)
        #Curved edges definition:
        global EdgeType,EdgeVertNum,InterpolPoints
        EdgeType=[]
        #self.ui.comboBox_22.activated.connect(self.GetEdgeType)
        EdgeVertNum=[]
        self.ui.Add_edgevert.clicked.connect(self.AddEdgeVert)
        InterpolPoints=[]
        self.ui.Add_interp.clicked.connect(self.AddInterpPoints)
        self.ui.Reset_curvedg.clicked.connect(self.ResetCurvEdges)
        #Simple grading or Edge grading -> enabled / disabled:
        self.ui.checkBox_2.stateChanged.connect(self.SimplGrad)
        self.ui.checkBox_3.stateChanged.connect(self.EdgeGrad)
        #Blocks definition:
        global DataBlock, BlockCounter, gradType
        DataBlock=[]
        BlockCounter=0
        gradType=[]
        self.ui.Create_block.clicked.connect(self.CreateBlock)
        self.ui.Reset_block.clicked.connect(self.ResetBlock)
        #Get boundaries:
        global VfacesBound,PatchInfo,NumBounds
        VfacesBound=[]
        PatchInfo=[]
        NumBounds=0
        self.ui.Set_bound.clicked.connect(self.SetBoundary)
        self.ui.Reset_bound.clicked.connect(self.ResetBoundary)
        #Call generation of blockMesh
        self.ui.Create_mesh.clicked.connect(lambda: mesh.GenerateBlockMesh(VertList,NumVerts,\
                                                                           EdgeType,EdgeVertNum, \
                                                                           InterpolPoints, \
                                                                           DataBlock,gradType, \
                                                                           VfacesBound,PatchInfo, \
                                                                           NumBounds,dirname))
        #Call preview of blockMesh
        self.ui.Preview_bMesh.clicked.connect (lambda: mesh.PreviewMesh(dirname))
        #----------snappyHexMesh-----------#
        #Steps to run:
        global Steptorun
        Steptorun=[]
        self.ui.SetSteps.clicked.connect(self.EnabDisabSteps)
        #Load geometry
        global CADfile_url, CADfile_name
        self.ui.browseCAD.clicked.connect(self.GetGeometry)
        self.ui.loadCAD.clicked.connect(self.LoadGeometry)
        #Refinement Area -> enabled / disabled:
        self.ui.checkBox_4.stateChanged.connect(self.RefineArea)
        #Get refinement box points:
        global BoxMinPoint,BoxMaxPoint
        BoxMinPoint=[]
        BoxMaxPoint=[]
        self.ui.AddBoxPoints.clicked.connect(self.AddRBoxPoints)
        self.ui.ResetBoxPoints.clicked.connect(self.ResetRBoxPoints)
        #Get Castellated Mesh Controls 1:
        global CastMeshData
        CastMeshData=[]
        self.ui.SetParam1.clicked.connect(self.SetParams1)
        self.ui.ResetParam1.clicked.connect(self.ResetParams1)
        #Get surface extract Dict data:
        global SurfExtDictData
        SurfExtDictData=[]
        self.ui.SurfExtDict.clicked.connect(self.GetandCreateSED)
        #Generate Edge Features file (.eMesh):
        self.ui.Gen_eMesh.clicked.connect(self.Gen_eMesh)
        #Refinement in Box [Mode] -> enabled / disabled:
        self.ui.comboBox_25.currentIndexChanged.connect(self.EnabDisabInput)
        #open CAD -> find location in Mesh:
        self.ui.openCAD.clicked.connect(self.OpenCad)
        #Get Castellated Mesh Controls 2:
        self.ui.SetParam2.clicked.connect(self.SetParams2)
        self.ui.ResetParam2.clicked.connect(self.ResetParams2)
        #Get Snap Controls:
        global SnapData
        SnapData=[]
        self.ui.SetSnapParam.clicked.connect(self.SetSnapParams)
        self.ui.ResetSnapParam.clicked.connect(self.ResetSnapParams)
        #Get boundaries to add layers:
        global boundstolayer
        boundstolayer=[]
        self.ui.AddBoundLayer.clicked.connect(self.AddBoundtobeLayered)
        #Get Add Layer Controls:
        global AddLayerData
        AddLayerData=[]
        self.ui.SetLayerParam.clicked.connect(self.SetLayerParams)
        self.ui.ResetLayerParam.clicked.connect(self.ResetLayerParams)
        #Generate snappyHexMeshDict and snappyHexMesh:
        self.ui.CreateSnappy.clicked.connect(lambda: mesh.GenerateSnappyHexMesh(dirname,Steptorun,CADfile_name,BoxMinPoint,BoxMaxPoint, \
                                                                               CastMeshData,SnapData, \
                                                                               AddLayerData))
         #Call preview of snappyMesh
        self.ui.Preview_snappymesh.clicked.connect (lambda: mesh.PreviewMesh(dirname))
        #----------Convert Mesh (Fluent, Gambit, I-Deas, CFX) -----------#
        global Meshfile_url, Meshfile_name
        self.ui.SearchMeshFile.clicked.connect(self.SearchMesh)
        self.ui.ConvertMesh.clicked.connect(self.ConvertMesh)
        self.ui.ViewMeshConv.clicked.connect(lambda: mesh.PreviewMesh(dirname))
        #MODEL TAB
        self.ui.steady_btn.toggled.connect(self.steadyButton)
        self.ui.transient_btn.toggled.connect(self.transientButton)
        self.ui.RANS_btn.toggled.connect(self.ransButton)
        self.ui.LESDES_btn.toggled.connect(self.lesdesButton)
        self.ui.comboBox.activated.connect(self.turbModel)
        self.ui.comboBox_26.activated.connect(self.transportModel)
        # MATERIALS TAB
        self.ui.comboBox_27.activated.connect(self.setParamsMaterials)
        self.ui.Default_mat.clicked.connect(self.setParamsMaterials)
        self.ui.setProp_mat.clicked.connect(self.setMatProperties)
        # BOUND COND TAB
        self.ui.P_inlet_frame.hide()
        self.ui.P_outlet_frame.hide()
        self.ui.P_flowinlet_frame.hide()
        self.ui.P_symmetry_frame.hide()
        self.ui.P_wall_frame.hide()
        self.ui.P_empty_frame.hide()
        self.ui.U_inlet_frame.hide()
        self.ui.U_outlet_frame.hide()
        self.ui.U_inletoutlet_frame.hide()
        self.ui.U_outflow_frame.hide()
        self.ui.U_symmetry_frame.hide()
        self.ui.U_wall_frame.hide()
        self.ui.U_empty_frame.hide()
        self.ui.pushButton_7.clicked.connect(self.seeBoundaries)
        self.ui.listWidget.itemPressed.connect(self.selectBoundName)
        self.ui.comboBox_3.currentIndexChanged.connect(self.selectPressureFrames)
        self.ui.comboBox_4.currentIndexChanged.connect(self.selectVelocityFrames)
        self.ui.comboBox_38.currentIndexChanged.connect(self.kTypes)
        self.ui.comboBox_39.currentIndexChanged.connect(self.epsilonTypes)
        self.ui.comboBox_40.currentIndexChanged.connect(self.omegaTypes)
        self.ui.comboBox_41.currentIndexChanged.connect(self.nutTypes)
        self.ui.comboBox_42.currentIndexChanged.connect(self.nuTildaTypes)
        #Get pressure boundary conditions
        global P_BoundCond
        P_BoundCond=[]
        self.ui.pushButton.clicked.connect(self.getPressureWall)
        self.ui.pushButton_2.clicked.connect(self.getPressureSymmetry)
        self.ui.pushButton_3.clicked.connect(self.getPressureOutlet)
        self.ui.pushButton_4.clicked.connect(self.getPressureInlet)
        self.ui.pushButton_5.clicked.connect(self.getFlowInlet)
        self.ui.pushButton_6.clicked.connect(self.getPressureEmpty)
        #Get velocity boundary conditions
        global U_BoundCond
        U_BoundCond=[]
        self.ui.pushButton_8.clicked.connect(self.getVelocityInlet)
        self.ui.pushButton_9.clicked.connect(self.getVelocityOutlet)
        self.ui.pushButton_10.clicked.connect(self.getInletOutlet)
        self.ui.pushButton_11.clicked.connect(self.getOutflow)
        self.ui.pushButton_12.clicked.connect(self.getVelocitySymmetry)
        self.ui.pushButton_13.clicked.connect(self.getVelocityWall)
        self.ui.pushButton_14.clicked.connect(self.getVelocityEmpty)
        
        # SOLVER TAB
        self.ui.residualsbtn.setEnabled(False)

    #**********************************FUNCTIONS FILE TAB*********************************************#
    def NewDialog (self):
        global dirname  
        dirname=fopt.NewCase()
        
    def LoadDialog (self):
        global dirname
        try:
            dirname=fopt.LoadCase()
        except:
            print("Case not loaded")
            dirname=[]
        else:
            fopt.LoadSuccessDialog(dirname)

    def closeEvent(self, event):
        print("Closing")
        self.deleteLater()

    #**********************************FUNCTIONS MESH TAB*********************************************#
    #BLOCKMESH:
    def AddVertex (self):
        VertAdd=[int(self.ui.lineEdit_35.text()),int(self.ui.lineEdit_36.text()), int(self.ui.lineEdit_37.text())];
        VertList.append(VertAdd)
        self.ui.lineEdit_35.clear()
        self.ui.lineEdit_36.clear()
        self.ui.lineEdit_37.clear()
        global NumVerts
        NumVerts=len(VertList)
        self.ui.listWidget_2.addItem("Vertex #"+str(NumVerts-1)+": ["+str(VertAdd[0])+"] ["+str(VertAdd[1])+"] ["+str(VertAdd[2])+"]")
        print(NumVerts)
        print(VertList)
        
    def ResetVertex (self):
        global VertList
        VertList=[]
        global NumVerts
        NumVerts=0
        print(VertList)
        self.ui.listWidget_2.clear()
        
    def AddEdgeVert (self):
        VertEdgeAdd=[int(self.ui.lineEdit_38.text()),int(self.ui.lineEdit_39.text())]
        EdgeVertNum.append(VertEdgeAdd)
        self.ui.lineEdit_38.clear()
        self.ui.lineEdit_39.clear()
        print(EdgeVertNum)
        global EdgeType
        j=self.ui.comboBox_22.currentText()
        if j == "Arc":
            EdgeType="arc"
        elif j == "spline":
            EdgeType="Spline"
        elif j == "Polyline":
            EdgeType="polyLine"
        else:
            EdgeType="BSpline"
        print(EdgeType)
        
    def AddInterpPoints (self):
        InterpAdd=[int(self.ui.lineEdit_40.text()),int(self.ui.lineEdit_41.text()),int(self.ui.lineEdit_42.text())]
        InterpolPoints.append(InterpAdd)
        self.ui.lineEdit_40.clear()
        self.ui.lineEdit_41.clear()
        self.ui.lineEdit_42.clear()
        print(InterpolPoints)
        
    def ResetCurvEdges (self):
        EdgeVertNum=[]
        InterpolPoints=[]
        print(EdgeVertNum)
        print(InterpolPoints)
        
    def SimplGrad (self):
        if self.ui.checkBox_2.isChecked() == True:
            self.ui.lineEdit_54.setEnabled(True)
            self.ui.lineEdit_55.setEnabled(True)
            self.ui.lineEdit_56.setEnabled(True)
            self.ui.checkBox_3.setChecked(False)
        else:
            self.ui.lineEdit_54.setEnabled(False)
            self.ui.lineEdit_55.setEnabled(False)
            self.ui.lineEdit_56.setEnabled(False)
            self.ui.checkBox_3.setChecked(True)
            
    def EdgeGrad (self):
        if self.ui.checkBox_3.isChecked() == True:
            self.ui.lineEdit_57.setEnabled(True)
            self.ui.lineEdit_58.setEnabled(True)
            self.ui.lineEdit_59.setEnabled(True)
            self.ui.lineEdit_60.setEnabled(True)
            self.ui.lineEdit_61.setEnabled(True)
            self.ui.lineEdit_62.setEnabled(True)
            self.ui.lineEdit_63.setEnabled(True)
            self.ui.lineEdit_64.setEnabled(True)
            self.ui.lineEdit_65.setEnabled(True)
            self.ui.lineEdit_66.setEnabled(True)
            self.ui.lineEdit_67.setEnabled(True)
            self.ui.lineEdit_68.setEnabled(True)
            self.ui.checkBox_2.setChecked(False)
        else:
            self.ui.lineEdit_57.setEnabled(False)
            self.ui.lineEdit_58.setEnabled(False)
            self.ui.lineEdit_59.setEnabled(False)
            self.ui.lineEdit_60.setEnabled(False)
            self.ui.lineEdit_61.setEnabled(False)
            self.ui.lineEdit_62.setEnabled(False)
            self.ui.lineEdit_63.setEnabled(False)
            self.ui.lineEdit_64.setEnabled(False)
            self.ui.lineEdit_65.setEnabled(False)
            self.ui.lineEdit_66.setEnabled(False)
            self.ui.lineEdit_67.setEnabled(False)
            self.ui.lineEdit_68.setEnabled(False)
            self.ui.checkBox_2.setChecked(True)
    
    def CreateBlock (self):
        FacesVerts=[int(self.ui.lineEdit_43.text()),int(self.ui.lineEdit_44.text()) \
                    ,int(self.ui.lineEdit_45.text()),int(self.ui.lineEdit_46.text()) \
                    ,int(self.ui.lineEdit_47.text()),int(self.ui.lineEdit_48.text()) \
                    ,int(self.ui.lineEdit_49.text()),int(self.ui.lineEdit_50.text())]
        nNodesAxis=[int(self.ui.lineEdit_51.text()),int(self.ui.lineEdit_52.text()) \
                    ,int(self.ui.lineEdit_53.text())]
        if self.ui.checkBox_2.isChecked() == True:
            gradType.append("simpleGrading")
            gradRatio=[int(self.ui.lineEdit_54.text()),int(self.ui.lineEdit_55.text()) \
                       ,int(self.ui.lineEdit_56.text())]
        elif self.ui.checkBox_3.isChecked() == True:
            gradType.append("edgeGrading")
            gradRatio=[int(self.ui.lineEdit_57.text()),int(self.ui.lineEdit_58.text()) \
                       ,int(self.ui.lineEdit_59.text()),int(self.ui.lineEdit_60.text()) \
                       ,int(self.ui.lineEdit_61.text()),int(self.ui.lineEdit_62.text()) \
                       ,int(self.ui.lineEdit_63.text()),int(self.ui.lineEdit_64.text()) \
                       ,int(self.ui.lineEdit_65.text()),int(self.ui.lineEdit_66.text()) \
                       ,int(self.ui.lineEdit_67.text()),int(self.ui.lineEdit_68.text())]
        global BlockCounter
        DataBlock.append(FacesVerts+nNodesAxis+gradRatio)
        BlockCounter=BlockCounter+1
        self.ui.lineEdit_43.clear()
        self.ui.lineEdit_44.clear()
        self.ui.lineEdit_45.clear()
        self.ui.lineEdit_46.clear()
        self.ui.lineEdit_47.clear()
        self.ui.lineEdit_48.clear()
        self.ui.lineEdit_49.clear()
        self.ui.lineEdit_50.clear()
        self.ui.lineEdit_51.clear()
        self.ui.lineEdit_52.clear()
        self.ui.lineEdit_53.clear()
        self.ui.lineEdit_54.clear()
        self.ui.lineEdit_55.clear()
        self.ui.lineEdit_56.clear()
        self.ui.lineEdit_57.clear()
        self.ui.lineEdit_58.clear()
        self.ui.lineEdit_59.clear()
        self.ui.lineEdit_60.clear()
        self.ui.lineEdit_61.clear()
        self.ui.lineEdit_62.clear()
        self.ui.lineEdit_63.clear()
        self.ui.lineEdit_64.clear()
        self.ui.lineEdit_65.clear()
        self.ui.lineEdit_66.clear()
        self.ui.lineEdit_67.clear()
        self.ui.lineEdit_68.clear()
        print(gradType)
        print(DataBlock[0][:])
        print(len(DataBlock))
        
    def ResetBlock (self):
        global DataBlock, gradType
        DataBlock=[]       
        gradType=[]
        global BlockCounter
        BlockCounter=0
        print(gradType)
        print(DataBlock)

    def SetBoundary (self):
        VfacesBound.append([int(self.ui.lineEdit_69.text()),int(self.ui.lineEdit_70.text()), \
                            int(self.ui.lineEdit_71.text()),int(self.ui.lineEdit_72.text())])
        global PatchInfo
        PatchInfo.append(self.ui.lineEdit_73.text())
        PatchInfo.append(self.ui.comboBox_23.currentText())
        self.ui.lineEdit_69.clear()
        self.ui.lineEdit_70.clear()
        self.ui.lineEdit_71.clear()
        self.ui.lineEdit_72.clear()
        self.ui.lineEdit_73.clear()
        global NumBounds
        NumBounds=NumBounds+1
        self.ui.listWidget_2.addItem("'"+PatchInfo[-2]+"'"+"("+str(VfacesBound[-1][-4])+" "+str(VfacesBound[-1][-3])+ \
                                     " "+str(VfacesBound[-1][-2])+" "+str(VfacesBound[-1][-1])+ \
                                     ") -> "+PatchInfo[-1])
        print(VfacesBound)
        print(PatchInfo)
        
    def ResetBoundary (self):
        global VfacesBound,PatchInfo,NumBounds
        VfacesBound=[]
        PatchInfo=[]
        NumBounds=0
        print(VfacesBound)
        print(PatchInfo)
        self.ui.listWidget_2.clear()
        global NumVerts
        for i in range(NumVerts):
            self.ui.listWidget_2.addItem("Vertex #"+str(i+1)+": ["+str(VertList[i][0])+"] ["+str(VertList[i][1])+"] ["+str(VertList[i][2])+"]")

    #SNAPPYHEXMESH:
    def EnabDisabSteps (self):
        global Steptorun
        if self.ui.checkBox_6.isChecked() == True:
            Steptorun.append(["true"])
            self.ui.lineEdit_77.setEnabled(True)
            self.ui.lineEdit_78.setEnabled(True)
            self.ui.lineEdit_79.setEnabled(True)
            self.ui.lineEdit_80.setEnabled(True)
            self.ui.lineEdit_81.setEnabled(True)
            self.ui.lineEdit_106.setEnabled(True)
            self.ui.lineEdit_82.setEnabled(True)
            self.ui.lineEdit_83.setEnabled(True)
            self.ui.lineEdit_84.setEnabled(True)
            self.ui.lineEdit_85.setEnabled(True)
            self.ui.lineEdit_90.setEnabled(True)
            self.ui.lineEdit_91.setEnabled(True)
            self.ui.lineEdit_92.setEnabled(True)
        else:
            Steptorun.append(["false"])
            self.ui.lineEdit_77.setEnabled(False)
            self.ui.lineEdit_78.setEnabled(False)
            self.ui.lineEdit_79.setEnabled(False)
            self.ui.lineEdit_80.setEnabled(False)
            self.ui.lineEdit_81.setEnabled(False)
            self.ui.lineEdit_106.setEnabled(False)
            self.ui.lineEdit_82.setEnabled(False)
            self.ui.lineEdit_83.setEnabled(False)
            self.ui.lineEdit_84.setEnabled(False)
            self.ui.lineEdit_85.setEnabled(False)
            self.ui.lineEdit_90.setEnabled(False)
            self.ui.lineEdit_91.setEnabled(False)
            self.ui.lineEdit_92.setEnabled(False)
            
        if self.ui.checkBox_7.isChecked() == True:
            Steptorun.append(["true"])
            self.ui.lineEdit_93.setEnabled(True)
            self.ui.lineEdit_94.setEnabled(True)
            self.ui.lineEdit_95.setEnabled(True)
            self.ui.lineEdit_96.setEnabled(True)
            self.ui.lineEdit_105.setEnabled(True)
        else:
            Steptorun.append(["false"])
            self.ui.lineEdit_93.setEnabled(False)
            self.ui.lineEdit_94.setEnabled(False)
            self.ui.lineEdit_95.setEnabled(False)
            self.ui.lineEdit_96.setEnabled(False)
            self.ui.lineEdit_105.setEnabled(False)
            
        if self.ui.checkBox_8.isChecked() == True:
            Steptorun.append(["true"])
            self.ui.lineEdit_97.setEnabled(True)
            self.ui.lineEdit_98.setEnabled(True)
            self.ui.lineEdit_99.setEnabled(True)
            self.ui.lineEdit_100.setEnabled(True)
            self.ui.lineEdit_101.setEnabled(True)
        else:
            Steptorun.append(["false"])
            self.ui.lineEdit_97.setEnabled(False)
            self.ui.lineEdit_98.setEnabled(False)
            self.ui.lineEdit_99.setEnabled(False)
            self.ui.lineEdit_100.setEnabled(False)
            self.ui.lineEdit_101.setEnabled(False)
        print(Steptorun)
            
    def GetGeometry (self):
        global CADfile_url,CADfile_name
        (CADfile_url,CADfile_name)=mesh.BrowseCADFile()
        
    def LoadGeometry (self):
        global CADfile_url,CADfile_name, dirname
        mesh.CopyCADFile(CADfile_url,CADfile_name, dirname)
        
    def RefineArea(self):
        if self.ui.checkBox_4.isChecked() == True:
            self.ui.lineEdit_102.setEnabled(True)
            self.ui.lineEdit_103.setEnabled(True)
            self.ui.lineEdit_104.setEnabled(True)
            self.ui.lineEdit_74.setEnabled(True)
            self.ui.lineEdit_75.setEnabled(True)
            self.ui.lineEdit_76.setEnabled(True)
            self.ui.comboBox_25.setEnabled(True)
            self.ui.lineEdit_88.setEnabled(True)
            self.ui.lineEdit_89.setEnabled(True)
        else:
            self.ui.lineEdit_102.setEnabled(False)
            self.ui.lineEdit_103.setEnabled(False)
            self.ui.lineEdit_104.setEnabled(False)
            self.ui.lineEdit_74.setEnabled(False)
            self.ui.lineEdit_75.setEnabled(False)
            self.ui.lineEdit_76.setEnabled(False)
            self.ui.comboBox_25.setEnabled(False)
            self.ui.lineEdit_88.setEnabled(False)
            self.ui.lineEdit_89.setEnabled(False)
            
    def AddRBoxPoints (self):
        global BoxMinPoint,BoxMaxPoint
        BoxMinPoint=[float(self.ui.lineEdit_102.text()),float(self.ui.lineEdit_103.text()), float(self.ui.lineEdit_104.text())];
        BoxMaxPoint=[float(self.ui.lineEdit_74.text()),float(self.ui.lineEdit_75.text()), float(self.ui.lineEdit_76.text())];
        print(BoxMinPoint)
        print(BoxMaxPoint)
        
    def ResetRBoxPoints (self):
        global BoxMinPoint,BoxMaxPoint
        BoxMinPoint=[]
        BoxMaxPoint=[]
        self.ui.lineEdit_102.clear()
        self.ui.lineEdit_103.clear()
        self.ui.lineEdit_104.clear()
        self.ui.lineEdit_74.clear()
        self.ui.lineEdit_75.clear()
        self.ui.lineEdit_76.clear()
        
    def SetParams1 (self):
        global CastMeshData
        CastMeshData=[int(self.ui.lineEdit_77.text()),int(self.ui.lineEdit_78.text()), \
                      int(self.ui.lineEdit_79.text()),float(self.ui.lineEdit_80.text()), \
                      int(self.ui.lineEdit_81.text())]
        print(CastMeshData)
        
    def ResetParams1 (self):
        global CastMeshData
        CastMeshData=[]
        self.ui.lineEdit_77.clear()
        self.ui.lineEdit_78.clear()
        self.ui.lineEdit_79.clear()
        self.ui.lineEdit_80.clear()
        self.ui.lineEdit_81.clear()
        
    def GetandCreateSED (self):
        global SurfExtDictData
        SurfExtDictData=[int(self.ui.lineEdit_106.text())]
        if self.ui.radioButton_10.isChecked() == True:
            SurfExtDictData.append(["yes"])
        else:
            SurfExtDictData.append(["no"])
        if self.ui.radioButton_11.isChecked() == True:
            SurfExtDictData.append(["yes"])
        else:
            SurfExtDictData.append(["no"])
        print(SurfExtDictData)
        #Create SurfaceExtractDict function
        global dirname, CADfile_name
        mesh.CreateSurfExtDict(CADfile_name,dirname, SurfExtDictData)
        
    def Gen_eMesh (self):
        global dirname
        mesh.Generate_eMesh(dirname)
        
    def EnabDisabInput (self):
        j = self.ui.comboBox_25.currentText()
        if j == "distance":
            self.ui.lineEdit_86.setEnabled(True)
            self.ui.lineEdit_87.setEnabled(True)
        else:
            self.ui.lineEdit_86.setEnabled(False)
            self.ui.lineEdit_87.setEnabled(False)
            
    def OpenCad (self):
        global CADfile_name, dirname
        mesh.viewCAD(CADfile_name, dirname)
        
    def SetParams2 (self):
        global CastMeshData
        CastMeshData.append([int(self.ui.lineEdit_82.text()),int(self.ui.lineEdit_83.text()), \
                             int(self.ui.lineEdit_84.text()),self.ui.comboBox_24.currentText(), \
                             int(self.ui.lineEdit_85.text()),self.ui.comboBox_25.currentText()])
        if self.ui.checkBox_4.isChecked() == True:
            j=self.ui.comboBox_25.currentText()
            if j == "inside" or j == "outside":
                CastMeshData.append([int(self.ui.lineEdit_88.text()),int(self.ui.lineEdit_89.text())])
            else:
                CastMeshData.append([int(self.ui.lineEdit_86.text()),int(self.ui.lineEdit_87.text()), \
                                     int(self.ui.lineEdit_88.text()),int(self.ui.lineEdit_89.text())])
        CastMeshData.append([float(self.ui.lineEdit_90.text()),float(self.ui.lineEdit_91.text()), \
                             float(self.ui.lineEdit_92.text())])
        if self.ui.checkBox_5.isChecked() == True:
            CastMeshData.append(["true"])
        else:
            CastMeshData.append(["false"])
        print(CastMeshData)
        name=CADfile_name.rpartition(".")[0]
        global PatchInfo
        PatchInfo.append(name+"Group")
        PatchInfo.append(CastMeshData[5][3])
        print(PatchInfo)
        
    def ResetParams2 (self):
        global CastMeshData
        CastMeshData=CastMeshData[0:5:1]
        print(CastMeshData)
        self.ui.lineEdit_82.clear()
        self.ui.lineEdit_83.clear()
        self.ui.lineEdit_84.clear()
        self.ui.lineEdit_85.clear()
        self.ui.lineEdit_86.clear()
        self.ui.lineEdit_87.clear()
        self.ui.lineEdit_88.clear()
        self.ui.lineEdit_89.clear()
        self.ui.lineEdit_90.clear()
        self.ui.lineEdit_90.clear()
        self.ui.lineEdit_91.clear()
        self.ui.lineEdit_92.clear()
    
    def SetSnapParams (self):
        global SnapData
        SnapData=[int(self.ui.lineEdit_93.text()),int(self.ui.lineEdit_94.text()),int(self.ui.lineEdit_95.text()), \
                  int(self.ui.lineEdit_96.text()),int(self.ui.lineEdit_105.text())]
        if self.ui.radioButton_8.isChecked() == True:
            SnapData.append(["yes"])
        else:
            SnapData.append(["no"])
        if self.ui.radioButton_9.isChecked() == True:
            SnapData.append(["yes"])
        else:
            SnapData.append(["no"])
        print(SnapData)
        
    def ResetSnapParams (self):
        global SnapData
        SnapData=[]
        print(SnapData)
        self.ui.lineEdit_93.clear()
        self.ui.lineEdit_94.clear()
        self.ui.lineEdit_95.clear()
        self.ui.lineEdit_96.clear()
        self.ui.lineEdit_105.clear()
        self.group = QtWidgets.QButtonGroup()
        self.group.addButton(self.ui.radioButton_8)
        self.group.addButton(self.ui.radioButton_9) 
        self.group.setExclusive(False)
        self.ui.radioButton_8.setChecked(False)
        self.ui.radioButton_9.setChecked(False)
        self.group.setExclusive(True)
        
    def AddBoundtobeLayered (self):
        global boundstolayer
        boundstolayer.append([str(self.ui.lineEdit_101.text())])
        self.ui.lineEdit_101.clear()
    
    def SetLayerParams (self):
        global AddLayerData
        AddLayerData=[float(self.ui.lineEdit_97.text()),float(self.ui.lineEdit_98.text()),float(self.ui.lineEdit_99.text()), \
            boundstolayer,int(self.ui.lineEdit_100.text())]
        print(AddLayerData)
        
    def ResetLayerParams (self):
        global AddLayerData
        AddLayerData=[]
        print(AddLayerData)
        self.ui.lineEdit_97.clear()
        self.ui.lineEdit_98.clear()
        self.ui.lineEdit_99.clear()
        self.ui.lineEdit_100.clear()
        self.ui.lineEdit_101.clear()
        
    #SNAPPYHEXMESH:
    def SearchMesh (self):
        global Meshfile_url, Meshfile_name
        (Meshfile_url, Meshfile_name)=mesh.SearchMeshFile()
        
    def ConvertMesh (self):
        global dirname, Meshfile_url, Meshfile_name
        mesh.ConvertMeshFile(dirname,Meshfile_url,Meshfile_name)
    #******************************************FUNCTION MODEL TAB*****************************************#
    def steadyButton (self):
        if self.ui.steady_btn.isChecked() == True:
            self.ui.transient_btn.setChecked(False)
            self.ui.comboBox_2.clear()
            self.ui.comboBox_2.addItem("steadyState")
            self.ui.RANS_btn.setChecked(False)
            self.ui.LESDES_btn.setChecked(False)
            self.ui.RANS_btn.setEnabled(False)
            self.ui.LESDES_btn.setEnabled(False)
            self.ui.comboBox.clear()
            self.ui.comboBox.addItem("Select turbulence model")
            self.ui.comboBox.addItem("k-w SST")
            self.ui.comboBox.addItem("Spalart-Allmaras")
            self.ui.comboBox.addItem("Realizable k-epsilon")
            self.ui.comboBox.addItem("RNG k-epsilon")
            self.ui.comboBox.addItem("Lien-Leschziner")
            self.ui.comboBox.addItem("Laminar")
            
    def transientButton (self):
        if self.ui.transient_btn.isChecked() == True:
            self.ui.steady_btn.setChecked(False)
            self.ui.comboBox_2.clear()
            self.ui.comboBox_2.addItem("Euler")
            self.ui.comboBox_2.addItem("backward")
            self.ui.comboBox_2.addItem("CrankNicolson 0.9")
            self.ui.RANS_btn.setEnabled(True)
            self.ui.LESDES_btn.setEnabled(True)
            
    def ransButton (self):
        if self.ui.RANS_btn.isChecked() == True:
            self.ui.LESDES_btn.setChecked(False)
            self.ui.comboBox.clear()
            self.ui.comboBox.addItem("Select turbulence model")
            self.ui.comboBox.addItem("k-w SST")
            self.ui.comboBox.addItem("Spalart-Allmaras")
            self.ui.comboBox.addItem("Realizable k-epsilon")
            self.ui.comboBox.addItem("RNG k-epsilon")
            self.ui.comboBox.addItem("Lien-Leschziner")
            self.ui.comboBox.addItem("Laminar")
    
    def lesdesButton (self):
        if self.ui.LESDES_btn.isChecked() == True:
            self.ui.RANS_btn.setChecked(False)
            self.ui.comboBox.clear()
            self.ui.comboBox.addItem("Select turbulence model")
            self.ui.comboBox.addItem("DES Spalart-Allmaras")
            self.ui.comboBox.addItem("DDES Spalart-Allmaras")
            self.ui.comboBox.addItem("IDDES Spalart-Allmaras")
            self.ui.comboBox.addItem("LES Smagorinsky")
            self.ui.comboBox.addItem("Laminar")
            
    def turbModel (self):
        j=self.ui.comboBox.currentIndex()
        if self.ui.steady_btn.isChecked() == True or self.ui.RANS_btn.isChecked() == True:
            if j == 1:
                prop.editTurb(dirname,"kOmegaSST")
                self.ui.epsilon_frame.setEnabled(False)
                self.ui.nut_frame.setEnabled(False)
                self.ui.nutilda_frame.setEnabled(False)
                self.ui.k_frame.setEnabled(True)
                self.ui.omega_frame.setEnabled(True)
            elif j == 2:
                prop.editTurb(dirname,"SpalartAllmaras")
                self.ui.epsilon_frame.setEnabled(False)
                self.ui.nut_frame.setEnabled(True)
                self.ui.nutilda_frame.setEnabled(True)
                self.ui.k_frame.setEnabled(False)
                self.ui.omega_frame.setEnabled(False)
            elif j == 3:
                prop.editTurb(dirname,"realizableKE")
                self.ui.epsilon_frame.setEnabled(True)
                self.ui.nut_frame.setEnabled(False)
                self.ui.nutilda_frame.setEnabled(False)
                self.ui.k_frame.setEnabled(True)
                self.ui.omega_frame.setEnabled(False)
            elif j == 4:
                prop.editTrub(dirname,"RNGkEpsilon")
                self.ui.epsilon_frame.setEnabled(True)
                self.ui.nut_frame.setEnabled(False)
                self.ui.nutilda_frame.setEnabled(False)
                self.ui.k_frame.setEnabled(True)
                self.ui.omega_frame.setEnabled(False)
            elif j == 5:
                prop.editTurb(dirname,"LienLeschziner")
                self.ui.epsilon_frame.setEnabled(True)
                self.ui.nut_frame.setEnabled(False)
                self.ui.nutilda_frame.setEnabled(False)
                self.ui.k_frame.setEnabled(True)
                self.ui.omega_frame.setEnabled(False)
            elif j == 6:
                prop.editTurb(dirname,"laminar")
                self.ui.turb_tab.setEnabled(False)
        elif self.ui.LESDES_btn.isChecked() == True:
            if j == 5:
                prop.editTurb(dirname,"laminar")
                self.ui.turb_tab.setEnabled(False)
            else:
                print("feature not yet implemented in OpenFoam GUI")
                
    def transportModel (self):
        j=self.ui.comboBox_26.currentIndex()
        if j == 1:
            prop.editTransport(dirname,"Newtonian")
    
    #******************************************FUNCTIONS MATERIALS TAB************************************#
    def setParamsMaterials (self):
        global density, dyn_visc, kin_visc, idxProp
        density=[1.205, 998.2, 1.205, 998.2, 13529.0, 500]
        dyn_visc=[0.000019137, 0.001002, 0.0000173144, 0.001002, 0.0015220125, 0.05]
        kin_visc=[0.0000158813, 0.0000010038, 0.0000143688, 0.0000010038, 0.0000001125, 0.0001]
        
        j=self.ui.comboBox_27.currentText()
        if j == "air":
            self.ui.lineEdit_107.setText(str(density[0]))
            self.ui.lineEdit_108.setText(str(dyn_visc[0]))
            self.ui.lineEdit_109.setText(str(kin_visc[0]))
            idxProp=0
        elif j == "water":
            self.ui.lineEdit_107.setText(str(density[1]))
            self.ui.lineEdit_108.setText(str(dyn_visc[1]))
            self.ui.lineEdit_109.setText(str(kin_visc[1]))
        elif j == "waterVapour":
            self.ui.lineEdit_107.setText(str(density[2]))
            self.ui.lineEdit_108.setText(str(dyn_visc[2]))
            self.ui.lineEdit_109.setText(str(kin_visc[2]))
        elif j == "liquidWater":
            self.ui.lineEdit_107.setText(str(density[3]))
            self.ui.lineEdit_108.setText(str(dyn_visc[3]))
            self.ui.lineEdit_109.setText(str(kin_visc[3]))
        elif j == "mercury":
            self.ui.lineEdit_107.setText(str(density[4]))
            self.ui.lineEdit_108.setText(str(dyn_visc[4]))
            self.ui.lineEdit_109.setText(str(kin_visc[4]))
        elif j == "oil":
            self.ui.lineEdit_107.setText(str(density[5]))
            self.ui.lineEdit_108.setText(str(dyn_visc[5]))
            self.ui.lineEdit_109.setText(str(kin_visc[5]))
            
    def setMatProperties (self):
        global rho, nu
        rho=float(self.ui.lineEdit_107.text())
        nu=float(self.ui.lineEdit_109.text())
        prop.editMatProperties(dirname,rho,nu)
    
    #******************************************FUNCTIONS BOUNDARY CONDITIONS TAB**************************#
    def seeBoundaries (self):
        for i in range(0,len(PatchInfo),2):
            self.ui.listWidget.addItem(PatchInfo[i]+"  "+chr(187)+"  "+PatchInfo[i+1])
        #Write boundary dictionaries p and U
        subprocess.run(["cp -f $FOAM_TUTORIALS/incompressible/simpleFoam/pitzDaily/0/p "+dirname+"/0"],shell=True)
        subprocess.run(["pyFoamCreateBoundaryPatches.py --verbose --fix-types "+dirname+"/0/p"],shell=True)
        subprocess.run(["pyFoamCreateBoundaryPatches.py --verbose --clear-unused "+dirname+"/0/p"],shell=True)
        subprocess.run(["cp -f $FOAM_TUTORIALS/incompressible/simpleFoam/pitzDaily/0/U "+dirname+"/0"],shell=True)
        subprocess.run(["pyFoamCreateBoundaryPatches.py --verbose --fix-types "+dirname+"/0/U"],shell=True)
        subprocess.run(["pyFoamCreateBoundaryPatches.py --verbose --clear-unused "+dirname+"/0/U"],shell=True)
            
    def selectBoundName (self):
        j=self.ui.listWidget.currentRow()
        if j == 0:
            self.ui.lineEdit.setText(PatchInfo[j])
            self.ui.lineEdit_2.setText(PatchInfo[j])
            self.ui.lineEdit_120.setText(PatchInfo[j])
            self.ui.lineEdit_122.setText(PatchInfo[j])
            self.ui.lineEdit_124.setText(PatchInfo[j])
            self.ui.lineEdit_126.setText(PatchInfo[j])
            self.ui.lineEdit_128.setText(PatchInfo[j])
        else:
            self.ui.lineEdit.setText(PatchInfo[j+j])
            self.ui.lineEdit_2.setText(PatchInfo[j+j])
            self.ui.lineEdit_120.setText(PatchInfo[j+j])
            self.ui.lineEdit_122.setText(PatchInfo[j+j])
            self.ui.lineEdit_124.setText(PatchInfo[j+j])
            self.ui.lineEdit_126.setText(PatchInfo[j+j])
            self.ui.lineEdit_128.setText(PatchInfo[j+j])
            
    def selectPressureFrames (self):
        j=self.ui.comboBox_3.currentText()
        if j == "Pressure Inlet":
            self.ui.P_outlet_frame.hide()
            self.ui.P_flowinlet_frame.hide()
            self.ui.P_symmetry_frame.hide()
            self.ui.P_wall_frame.hide()
            self.ui.P_empty_frame.hide()
            self.ui.P_inlet_frame.show()
        elif j == "Pressure Outlet":
            self.ui.P_inlet_frame.hide()
            self.ui.P_flowinlet_frame.hide()
            self.ui.P_symmetry_frame.hide()
            self.ui.P_wall_frame.hide()
            self.ui.P_empty_frame.hide()
            self.ui.P_outlet_frame.show()
        elif j == "Flow Inlet":
            self.ui.P_inlet_frame.hide()
            self.ui.P_outlet_frame.hide()
            self.ui.P_symmetry_frame.hide()
            self.ui.P_wall_frame.hide()
            self.ui.P_empty_frame.hide()
            self.ui.P_flowinlet_frame.show()
        elif j == "Symmetry":
            self.ui.P_inlet_frame.hide()
            self.ui.P_outlet_frame.hide()
            self.ui.P_flowinlet_frame.hide()
            self.ui.P_wall_frame.hide()
            self.ui.P_empty_frame.hide()
            self.ui.P_symmetry_frame.show()
        elif j == "Wall":
            self.ui.P_inlet_frame.hide()
            self.ui.P_outlet_frame.hide()
            self.ui.P_flowinlet_frame.hide()
            self.ui.P_symmetry_frame.hide()
            self.ui.P_empty_frame.hide()
            self.ui.P_wall_frame.show()
        elif j == "Empty":
            self.ui.P_inlet_frame.hide()
            self.ui.P_outlet_frame.hide()
            self.ui.P_flowinlet_frame.hide()
            self.ui.P_symmetry_frame.hide()
            self.ui.P_wall_frame.hide()
            self.ui.P_empty_frame.show()
        elif j == "Select type":
            self.ui.P_inlet_frame.hide()
            self.ui.P_outlet_frame.hide()
            self.ui.P_flowinlet_frame.hide()
            self.ui.P_symmetry_frame.hide()
            self.ui.P_wall_frame.hide()
            self.ui.P_empty_frame.hide()
            
    def selectVelocityFrames (self):
        j=self.ui.comboBox_4.currentText()
        if j == "Velocity Inlet":
            self.ui.U_outlet_frame.hide()
            self.ui.U_inletoutlet_frame.hide()
            self.ui.U_outflow_frame.hide()
            self.ui.U_symmetry_frame.hide()
            self.ui.U_wall_frame.hide()
            self.ui.U_empty_frame.hide()
            self.ui.U_inlet_frame.show()
        elif j == "Velocity Outlet":
            self.ui.U_inlet_frame.hide()
            self.ui.U_inletoutlet_frame.hide()
            self.ui.U_outflow_frame.hide()
            self.ui.U_symmetry_frame.hide()
            self.ui.U_wall_frame.hide()
            self.ui.U_empty_frame.hide()
            self.ui.U_outlet_frame.show()
        elif j == "Inlet Outlet":
            self.ui.U_inlet_frame.hide()
            self.ui.U_outlet_frame.hide()
            self.ui.U_outflow_frame.hide()
            self.ui.U_symmetry_frame.hide()
            self.ui.U_wall_frame.hide()
            self.ui.U_empty_frame.hide()
            self.ui.U_inletoutlet_frame.show()
        elif j == "Outflow":
            self.ui.U_inlet_frame.hide()
            self.ui.U_outlet_frame.hide()
            self.ui.U_inletoutlet_frame.hide()
            self.ui.U_symmetry_frame.hide()
            self.ui.U_wall_frame.hide()
            self.ui.U_empty_frame.hide()
            self.ui.U_outflow_frame.show()
        elif j == "Symmetry":
            self.ui.U_inlet_frame.hide()
            self.ui.U_outlet_frame.hide()
            self.ui.U_inletoutlet_frame.hide()
            self.ui.U_outflow_frame.hide()
            self.ui.U_wall_frame.hide()
            self.ui.U_empty_frame.hide()
            self.ui.U_symmetry_frame.show()
        elif j == "Wall":
            self.ui.U_inlet_frame.hide()
            self.ui.U_outlet_frame.hide()
            self.ui.U_inletoutlet_frame.hide()
            self.ui.U_outflow_frame.hide()
            self.ui.U_symmetry_frame.hide()
            self.ui.U_empty_frame.hide()
            self.ui.U_wall_frame.show()
        elif j == "Empty":
            self.ui.U_inlet_frame.hide()
            self.ui.U_outlet_frame.hide()
            self.ui.U_inletoutlet_frame.hide()
            self.ui.U_outflow_frame.hide()
            self.ui.U_symmetry_frame.hide()
            self.ui.U_wall_frame.hide()
            self.ui.U_empty_frame.show()
        elif j == "Select type":
            self.ui.U_inlet_frame.hide()
            self.ui.U_outlet_frame.hide()
            self.ui.U_inletoutlet_frame.hide()
            self.ui.U_outflow_frame.hide()
            self.ui.U_symmetry_frame.hide()
            self.ui.U_wall_frame.hide()
            self.ui.U_empty_frame.hide()
            
    def kTypes (self):
        j=self.ui.comboBox_38.currentText()
        if j == "fixedValue":
            self.ui.label_172.setEnabled(True)
            self.ui.lineEdit_121.setEnabled(True)
        else:
            self.ui.label_172.setEnabled(False)
            self.ui.lineEdit_121.setEnabled(False)
            
    def epsilonTypes(self):
        j=self.ui.comboBox_39.currentText()
        if j == "fixedValue":
            self.ui.label_175.setEnabled(True)
            self.ui.lineEdit_123.setEnabled(True)
        else:
            self.ui.label_175.setEnabled(False)
            self.ui.lineEdit_123.setEnabled(False)
            
    def omegaTypes (self):
        j=self.ui.comboBox_40.currentText()
        if j == "fixedValue":
            self.ui.label_178.setEnabled(True)
            self.ui.lineEdit_125.setEnabled(True)
        else:
            self.ui.label_178.setEnabled(False)
            self.ui.lineEdit_125.setEnabled(False)
            
    def nutTypes (self):
        j=self.ui.comboBox_41.currentText()
        if j == "freestream" or "calculated":
            self.ui.label_181.setEnabled(True)
            self.ui.lineEdit_127.setEnabled(True)
        else:
            self.ui.label_181.setEnabled(False)
            self.ui.lineEdit_127.setEnabled(False)
            
    def nuTildaTypes (self):
        j=self.ui.comboBox_42.currentText()
        if j == "freestream" or "fixedValue":
            self.ui.label_184.setEnabled(True)
            self.ui.lineEdit_129.setEnabled(True)
        else:
            self.ui.label_184.setEnabled(True)
            self.ui.lineEdit_129.setEnabled(True)
            
    def getPressureWall (self):
        global P_BoundCond
        #Patch_name.append([self.ui.])
        P_BoundCond.append([self.ui.comboBox_30.currentText()])
        b_cond.writePdict(dirname,P_BoundCond)
        
    def getPressureSymmetry (self):
        global P_BoundCond
        P_BoundCond.append([self.ui.comboBox_28.currentText()])
        b_cond.writePdict(dirname,P_BoundCond)
        
    def getPressureOutlet (self):
        global P_BoundCond
        P_BoundCond.append([self.ui.comboBox_6.currentText(),self.ui.lineEdit_4.text()])
        b_cond.writePdict(dirname,P_BoundCond)
        
    def getPressureInlet (self):
        global P_BoudCond
        P_BoundCond.append([self.ui.comboBox_5.currentText(),self.ui.lineEdit_3.text()])
        b_cond.writePdict(dirname,P_BoundCond)
        
    def getFlowInlet (self):
        global P_BoundCond
        P_BoundCond.append([self.ui.comboBox_29.currentText()])
        b_cond.writePdict(dirname,P_BoundCond)
        
    def getPressureEmpty (self):
        global P_BoundCond
        P_BoundCond.append([self.ui.comboBox_31.currentText()])
        b_cond.writePdict(dirname,P_BoundCond)
        
    def getVelocityInlet (self):
        global U_BoundCond
        U_BoundCond.append([self.ui.comboBox_32.currentText(),self.ui.lineEdit_5.text(),self.ui.lineEdit_6.text(),self.ui.lineEdit_7.text()])
        b_cond.writeUdict(dirname,U_BoundCond)
        
    def getVelocityOutlet (self):
        global U_BoundCond
        U_BoundCond.append([self.ui.comboBox_33.currentText(),self.ui.lineEdit_8.text(),self.ui.lineEdit_9.text(),self.ui.lineEdit_10.text()])
        b_cond.writeUdict(dirname,U_BoundCond)
        
    def getInletOutlet (self):
        global U_BoundCond
        U_BoundCond.append([self.ui.lineEdit_11.text(),self.ui.lineEdit_12.text(),self.ui.lineEdit_13.text(),self.ui.lineEdit_117.text(),\
                            self.ui.lineEdit_118.text(),self.ui.lineEdit_119.text()])
        b_cond.writeUdict(dirname,U_BoundCond)
        
    def getOutflow (self):
        global U_BoundCond
        U_BoundCond.append([self.ui.comboBox_34.currentText()])
        b_cond.writeUdict(dirname,U_BoundCond)
        
    def getVelocitySymmetry (self):
        global U_BoundCond
        U_BoundCond.append([self.ui.comboBox_35.currentText()])
        b_cond.writeUdict(dirname,U_BoundCond)
        
    def getVelocityWall (self):
        global U_BoundCond
        U_BoundCond.append([self.ui.comboBox_36.currentText()])
        b_cond.writeUdict(dirname,U_BoundCond)
        
    def getVelocityEmpty (self):
        global U_BoundCond
        U_BoundCond.append([self.ui.comboBox_37.currentText()])
        b_cond.writeUdict(dirname,U_BoundCond)



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.setWindowTitle("OpenFOAM GUI")
    window.show()
    sys.exit(app.exec_())
