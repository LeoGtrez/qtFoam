#!/usr/bin/python

import sys
import os
import subprocess
import File_options as fopt
import Mesh_gen as mesh
import Properties as prop
import Bound_cond as b_cond
import Fields_init as f_init
import Runtime_ctrls as R_ctrls
import Solver_settings as solv
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
        self.ui.Create_mesh.clicked.connect\
        (lambda: mesh.GenerateBlockMesh(VertList,NumVerts,\
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
        self.ui.CreateSnappy.clicked.connect\
        (lambda: mesh.GenerateSnappyHexMesh(dirname,Steptorun, \
                                            CADfile_name, \
                                            BoxMinPoint,BoxMaxPoint, \
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
        # FIELDS INITIALISATION TAB
        self.ui.comboBox_43.currentIndexChanged.connect(self.selectTypePField)
        self.ui.comboBox_44.currentIndexChanged.connect(self.selectTypeUField)
        self.ui.pushButton_26.clicked.connect(self.setDefaultPField)
        self.ui.pushButton_28.clicked.connect(self.setDefaultUField)
        self.ui.pushButton_27.clicked.connect(self.setPFieldInit)
        self.ui.pushButton_29.clicked.connect(self.setUFieldInit)
        self.ui.pushButton_31.clicked.connect(self.setkFieldInit)
        self.ui.pushButton_33.clicked.connect(self.setEpsilonFieldInit)
        self.ui.pushButton_35.clicked.connect(self.setOmegaFieldInit)
        self.ui.pushButton_37.clicked.connect(self.setNutFieldInit)
        self.ui.pushButton_38.clicked.connect(self.setNuTildaFieldInit)
        
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
        self.ui.pushButton_25.clicked.connect(self.clearList)
        self.ui.listWidget.itemPressed.connect(self.selectBoundName)
        self.ui.comboBox_3.currentIndexChanged.connect(self.selectPressureFrames)
        self.ui.comboBox_4.currentIndexChanged.connect(self.selectVelocityFrames)
        self.ui.comboBox_5.currentIndexChanged.connect(self.pInletTypes)
        self.ui.comboBox_6.currentIndexChanged.connect(self.pOutletTypes)
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
        #Get k parameter boundary conditions
        global k_BoundCond
        k_BoundCond=[]
        self.ui.pushButton_15.clicked.connect(self.getkBoundConds)
        #Get epsilon parameter boundary conditions
        global epsilon_BoundCond
        epsilon_BoundCond=[]
        self.ui.pushButton_16.clicked.connect(self.getEpsilonBoundConds)
        #Get omega parameter boundary conditions
        global omega_BoundCond
        omega_BoundCond=[]
        self.ui.pushButton_17.clicked.connect(self.getOmegaBoundConds)
        #Get nut parameter boundary conditions
        global nut_BoundCond
        nut_BoundCond=[]
        self.ui.pushButton_18.clicked.connect(self.getNutBoundConds)
        #Get nTilda parameter boundary conditions
        global nuTilda_BoundCond
        nuTilda_BoundCond=[]
        self.ui.pushButton_19.clicked.connect(self.getNuTildaBoundConds)
        
        # NUMERICAL SCHEMES TAB
        self.ui.pushButton_30.clicked.connect(self.setDefaultNumSchemes)
        self.ui.pushButton_20.clicked.connect(self.setNumSchemes)
        
        # RUNTIME CONTROLS TAB
        self.ui.pushButton_21.clicked.connect(self.setDefaultRuntimeCtrls)
        self.ui.pushButton_22.clicked.connect(self.setRuntimeCtrls)
        
        # SOLVER TAB
        self.ui.comboBox_21.currentIndexChanged.connect(self.setSolverApp)
        self.ui.spinBox.valueChanged.connect(self.setSolverApp)
        self.ui.pushButton_32.clicked.connect(self.loadListParam)
        self.ui.listWidget_4.itemPressed.connect(self.ActivDefault)
        self.ui.checkBox.toggled.connect(self.ActivRelaxFact)
        self.ui.pushButton_23.clicked.connect(self.defaultSettingsParam)
        global residuals,relaxFactors
        residuals={'p':'1e-3','U':'1e-3','k':'1e-3','epsilon':'1e-3','omega':\
                   '1e-3','nuTilda':'1e-3'}
        relaxFactors={'p':'0','U':'0','k':'0','epsilon':'1e-3','omega':'0',\
                      'nuTilda':'0'}
        self.ui.pushButton_24.clicked.connect(self.applySettingsParam)
        self.ui.runButton.clicked.connect(self.RUN)

    #*************FUNCTIONS FILE TAB*****************************************#
    def NewDialog (self):
        global dirname  
        dirname=fopt.NewCase()
        
    def LoadDialog (self):
        global dirname
        dirname=fopt.LoadCase()

    def closeEvent(self, event):
        print("Closing")
        self.deleteLater()

    #*************FUNCTIONS MESH TAB*****************************************#
    #BLOCKMESH:
    def AddVertex (self):
        VertAdd=[float(self.ui.lineEdit_35.text()),\
                 float(self.ui.lineEdit_36.text()),\
                 float(self.ui.lineEdit_37.text())];
        VertList.append(VertAdd)
        self.ui.lineEdit_35.clear()
        self.ui.lineEdit_36.clear()
        self.ui.lineEdit_37.clear()
        global NumVerts
        NumVerts=len(VertList)
        self.ui.listWidget_2.addItem("Vertex #"+\
                                     str(NumVerts-1)+": ["+\
                                     str(VertAdd[0])+"] ["+\
                                     str(VertAdd[1])+"] ["+\
                                     str(VertAdd[2])+"]")
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
        VertEdgeAdd=[int(self.ui.lineEdit_38.text()),\
                     int(self.ui.lineEdit_39.text())]
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
        InterpAdd=[float(self.ui.lineEdit_40.text()),\
                   float(self.ui.lineEdit_41.text()),\
                   float(self.ui.lineEdit_42.text())]
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
        FacesVerts=[int(self.ui.lineEdit_43.text()),\
                    int(self.ui.lineEdit_44.text()),\
                    int(self.ui.lineEdit_45.text()),\
                    int(self.ui.lineEdit_46.text()),\
                    int(self.ui.lineEdit_47.text()),\
                    int(self.ui.lineEdit_48.text()),\
                    int(self.ui.lineEdit_49.text()),\
                    int(self.ui.lineEdit_50.text())]
        nNodesAxis=[int(self.ui.lineEdit_51.text()),\
                    int(self.ui.lineEdit_52.text()) \
                    ,int(self.ui.lineEdit_53.text())]
        if self.ui.checkBox_2.isChecked() == True:
            gradType.append("simpleGrading")
            gradRatio=[float(self.ui.lineEdit_54.text()),\
                       float(self.ui.lineEdit_55.text()) \
                       ,float(self.ui.lineEdit_56.text())]
        elif self.ui.checkBox_3.isChecked() == True:
            gradType.append("edgeGrading")
            gradRatio=[float(self.ui.lineEdit_57.text()),\
                       float(self.ui.lineEdit_58.text()) \
                       ,float(self.ui.lineEdit_59.text()),\
                       float(self.ui.lineEdit_60.text()) \
                       ,float(self.ui.lineEdit_61.text()),\
                       float(self.ui.lineEdit_62.text()) \
                       ,float(self.ui.lineEdit_63.text()),\
                       float(self.ui.lineEdit_64.text()) \
                       ,float(self.ui.lineEdit_65.text()),\
                       float(self.ui.lineEdit_66.text()) \
                       ,float(self.ui.lineEdit_67.text()),\
                       float(self.ui.lineEdit_68.text())]
        global BlockCounter
        DataBlock.append(FacesVerts+nNodesAxis+gradRatio)
        BlockCounter=BlockCounter+1
        self.ui.listWidget_2.addItem(" ")
        self.ui.listWidget_2.addItem("Block #"+
                                     str(BlockCounter)+": ["+\
                                     str(FacesVerts[0])+"] ["+\
                                     str(FacesVerts[1])+"] ["+\
                                     str(FacesVerts[2])+"] ["+\
                                     str(FacesVerts[3])+"] ["+\
                                     str(FacesVerts[4])+"] ["+\
                                     str(FacesVerts[5])+"] ["+\
                                     str(FacesVerts[6])+"] ["+\
                                     str(FacesVerts[7])+"]")
        self.ui.listWidget_2.addItem("Nodes per axis: "+\
                                     str(nNodesAxis[0])+"[x] "+\
                                     str(nNodesAxis[1])+"[y] "+\
                                     str(nNodesAxis[2])+"[z]")
        if self.ui.checkBox_2.isChecked() == True:
            self.ui.listWidget_2.addItem("simpleGrading: ["+\
                                                          str(gradRatio[0])+" "+\
                                                          str(gradRatio[1])+" "+\
                                                          str(gradRatio[2])+"]")
        elif self.ui.checkBox_3.isChecked() == True:
            self.ui.listWidget_2.addItem("edgeGrading: ["+\
                                                        str(gradRatio[0])+" "+\
                                                        str(gradRatio[1])+" "+\
                                                        str(gradRatio[2])+" "+\
                                                        str(gradRatio[3])+" "+\
                                                        str(gradRatio[4])+" "+\
                                                        str(gradRatio[5])+" "+\
                                                        str(gradRatio[6])+" "+\
                                                        str(gradRatio[7])+" "+\
                                                        str(gradRatio[8])+" "+\
                                                        str(gradRatio[9])+" "+\
                                                        str(gradRatio[10])+" "+\
                                                        str(gradRatio[11])+"]")
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
        print(DataBlock)
        
    def ResetBlock (self):
        global DataBlock, gradType
        DataBlock=[]       
        gradType=[]
        global BlockCounter
        BlockCounter=0
        print(gradType)
        print(DataBlock)
        self.ui.listWidget_2.clear()
        global NumVerts
        for i in range(NumVerts):
            self.ui.listWidget_2.addItem("Vertex #"+str(i)+": ["+\
                                         str(VertList[i][0])+"] ["+\
                                         str(VertList[i][1])+"] ["+\
                                         str(VertList[i][2])+"]")

    def SetBoundary (self):
        VfacesBound.append([int(self.ui.lineEdit_69.text()),\
                            int(self.ui.lineEdit_70.text()), \
                            int(self.ui.lineEdit_71.text()),\
                            int(self.ui.lineEdit_72.text())])
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
        if len(PatchInfo) == 2:
            self.ui.listWidget_2.addItem(" ")
        self.ui.listWidget_2.addItem("Boundary: '"+PatchInfo[-2]+"'"+"("+\
                                     str(VfacesBound[-1][-4])+\
                                     " "+str(VfacesBound[-1][-3])+ \
                                     " "+str(VfacesBound[-1][-2])+" "+\
                                     str(VfacesBound[-1][-1])+ \
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
            self.ui.listWidget_2.addItem("Vertex #"+str(i)+": ["+\
                                         str(VertList[i][0])+"] ["+\
                                         str(VertList[i][1])+"] ["+\
                                         str(VertList[i][2])+"]")
        for i in range(0,BlockCounter):
            self.ui.listWidget_2.addItem(" ")
            self.ui.listWidget_2.addItem("Block #"+str(i+1)+": ["+\
                                         str(DataBlock[i][0])+"] ["+\
                                         str(DataBlock[i][1])+"] ["+\
                                         str(DataBlock[i][2])+"] ["+\
                                         str(DataBlock[i][3])+"] ["+\
                                         str(DataBlock[i][4])+"] ["+\
                                         str(DataBlock[i][5])+"] ["+\
                                         str(DataBlock[i][6])+"] ["+\
                                         str(DataBlock[i][7])+"]")
            self.ui.listWidget_2.addItem("Nodes per axis: "+\
                                         str(DataBlock[i][8])+"[x] "+\
                                         str(DataBlock[i][9])+"[y] "+\
                                         str(DataBlock[i][10])+"[z]")
        if gradType[i] == "simpleGrading":
            self.ui.listWidget_2.addItem("simpleGrading: ["+\
                                                          str(DataBlock[i][11])+" "+\
                                                          str(DataBlock[i][12])+" "+\
                                                          str(DataBlock[i][13])+"]")
        elif gradType[i] == "edgeGrading":
            self.ui.listWidget_2.addItem("edgeGrading: ["+\
                                                        str(DataBlock[i][11])+" "+\
                                                        str(DataBlock[i][12])+" "+\
                                                        str(DataBlock[i][13])+" "+\
                                                        str(DataBlock[i][14])+" "+\
                                                        str(DataBlock[i][15])+" "+\
                                                        str(DataBlock[i][16])+" "+\
                                                        str(DataBlock[i][17])+" "+\
                                                        str(DataBlock[i][18])+" "+\
                                                        str(DataBlock[i][19])+" "+\
                                                        str(DataBlock[i][20])+" "+\
                                                        str(DataBlock[i][21])+" "+\
                                                        str(DataBlock[i][22])+"]")

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
        BoxMinPoint=[float(self.ui.lineEdit_102.text()),\
                     float(self.ui.lineEdit_103.text()),\
                     float(self.ui.lineEdit_104.text())];
        BoxMaxPoint=[float(self.ui.lineEdit_74.text()),\
                     float(self.ui.lineEdit_75.text()),\
                     float(self.ui.lineEdit_76.text())];
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
        CastMeshData=[int(self.ui.lineEdit_77.text()),\
                      int(self.ui.lineEdit_78.text()), \
                      int(self.ui.lineEdit_79.text()),\
                      float(self.ui.lineEdit_80.text()), \
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
        CastMeshData.append([int(self.ui.lineEdit_82.text()),\
                             int(self.ui.lineEdit_83.text()),\
                             int(self.ui.lineEdit_84.text()),\
                             self.ui.comboBox_24.currentText(),\
                             int(self.ui.lineEdit_85.text()),\
                             self.ui.comboBox_25.currentText()])
        if self.ui.checkBox_4.isChecked() == True:
            j=self.ui.comboBox_25.currentText()
            if j == "inside" or j == "outside":
                CastMeshData.append([int(self.ui.lineEdit_88.text()),\
                                     int(self.ui.lineEdit_89.text())])
            else:
                CastMeshData.append([int(self.ui.lineEdit_86.text()),\
                                     int(self.ui.lineEdit_87.text()),\
                                     int(self.ui.lineEdit_88.text()),\
                                     int(self.ui.lineEdit_89.text())])
        CastMeshData.append([float(self.ui.lineEdit_90.text()),\
                             float(self.ui.lineEdit_91.text()), \
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
        SnapData=[int(self.ui.lineEdit_93.text()),\
                  float(self.ui.lineEdit_94.text()),\
                  int(self.ui.lineEdit_95.text()), \
                  int(self.ui.lineEdit_96.text()), \
                  int(self.ui.lineEdit_105.text())]
        if self.ui.radioButton_8.isChecked() == True:
            SnapData.append(["true"])
        else:
            SnapData.append(["false"])
        if self.ui.radioButton_9.isChecked() == True:
            SnapData.append(["true"])
        else:
            SnapData.append(["false"])
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
        AddLayerData=[float(self.ui.lineEdit_97.text()),\
                      float(self.ui.lineEdit_98.text()),\
                      float(self.ui.lineEdit_99.text()),\
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
    #*********************FUNCTION MODEL TAB*********************************#
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
                self.ui.Init_epsilon_frame.setEnabled(False)
                self.ui.Init_nut_frame.setEnabled(False)
                self.ui.Init_nuTilda_frame.setEnabled(False)
                self.ui.Init_k_frame.setEnabled(True)
                self.ui.Init_omega_frame.setEnabled(True)
                subprocess.run(["rm "+dirname+"/0/epsilon"],shell=True)
                subprocess.run(["rm "+dirname+"/0/nut"],shell=True)
                subprocess.run(["rm "+dirname+"/0/nuTilda"],shell=True)
                subprocess.run(["cp -f $FOAM_TUTORIALS/incompressible/simpleFoam/pitzDaily/0/k "+\
                                dirname+"/0"],shell=True)
                subprocess.run(["pyFoamCreateBoundaryPatches.py --verbose --fix-types "+\
                                dirname+"/0/k"],shell=True)
                subprocess.run(["pyFoamCreateBoundaryPatches.py --verbose --clear-unused "+\
                                dirname+"/0/k"],shell=True)
                subprocess.run(["cp -f $FOAM_TUTORIALS/incompressible/simpleFoam/pitzDaily/0/omega "+\
                                dirname+"/0"],shell=True)
                subprocess.run(["pyFoamCreateBoundaryPatches.py --verbose --fix-types "+\
                                dirname+"/0/omega"],shell=True)
                subprocess.run(["pyFoamCreateBoundaryPatches.py --verbose --clear-unused "+\
                                dirname+"/0/omega"],shell=True)
            elif j == 2:
                prop.editTurb(dirname,"SpalartAllmaras")
                self.ui.epsilon_frame.setEnabled(False)
                self.ui.nut_frame.setEnabled(True)
                self.ui.nutilda_frame.setEnabled(True)
                self.ui.k_frame.setEnabled(False)
                self.ui.omega_frame.setEnabled(False)
                self.ui.Init_epsilon_frame.setEnabled(False)
                self.ui.Init_nut_frame.setEnabled(True)
                self.ui.Init_nuTilda_frame.setEnabled(True)
                self.ui.Init_k_frame.setEnabled(False)
                self.ui.Init_omega_frame.setEnabled(False)
                subprocess.run(["rm "+dirname+"/0/k"],shell=True)
                subprocess.run(["rm "+dirname+"/0/epsilon"],shell=True)
                subprocess.run(["rm "+dirname+"/0/omega"],shell=True)
                subprocess.run(["cp -f $FOAM_TUTORIALS/incompressible/simpleFoam/pitzDaily/0/nut "\
                                +dirname+"/0"],shell=True)
                subprocess.run(["pyFoamCreateBoundaryPatches.py --verbose --fix-types "+\
                                dirname+"/0/nut"],shell=True)
                subprocess.run(["pyFoamCreateBoundaryPatches.py --verbose --clear-unused "+\
                                dirname+"/0/nut"],shell=True)
                subprocess.run(["cp -f $FOAM_TUTORIALS/incompressible/simpleFoam/pitzDaily/0/nuTilda "\
                                +dirname+"/0"],shell=True)
                subprocess.run(["pyFoamCreateBoundaryPatches.py --verbose --fix-types "+\
                                dirname+"/0/nuTilda"],shell=True)
                subprocess.run(["pyFoamCreateBoundaryPatches.py --verbose --clear-unused "+\
                                dirname+"/0/nuTilda"],shell=True)
            elif j == 3:
                prop.editTurb(dirname,"realizableKE")
                self.ui.epsilon_frame.setEnabled(True)
                self.ui.nut_frame.setEnabled(False)
                self.ui.nutilda_frame.setEnabled(False)
                self.ui.k_frame.setEnabled(True)
                self.ui.omega_frame.setEnabled(False)
                self.ui.Init_epsilon_frame.setEnabled(True)
                self.ui.Init_nut_frame.setEnabled(False)
                self.ui.Init_nuTilda_frame.setEnabled(False)
                self.ui.Init_k_frame.setEnabled(True)
                self.ui.Init_omega_frame.setEnabled(False)
                subprocess.run(["rm "+dirname+"/0/omega"],shell=True)
                subprocess.run(["rm "+dirname+"/0/nut"],shell=True)
                subprocess.run(["rm "+dirname+"/0/nuTilda"],shell=True)
                subprocess.run(["cp -f $FOAM_TUTORIALS/incompressible/simpleFoam/pitzDaily/0/k "\
                                +dirname+"/0"],shell=True)
                subprocess.run(["pyFoamCreateBoundaryPatches.py --verbose --fix-types "+\
                                dirname+"/0/k"],shell=True)
                subprocess.run(["pyFoamCreateBoundaryPatches.py --verbose --clear-unused "+\
                                dirname+"/0/k"],shell=True)
                subprocess.run(["cp -f $FOAM_TUTORIALS/incompressible/simpleFoam/pitzDaily/0/epsilon "+\
                                dirname+"/0"],shell=True)
                subprocess.run(["pyFoamCreateBoundaryPatches.py --verbose --fix-types "+\
                                dirname+"/0/epsilon"],shell=True)
                subprocess.run(["pyFoamCreateBoundaryPatches.py --verbose --clear-unused "+\
                                dirname+"/0/epsilon"],shell=True)
            elif j == 4:
                prop.editTurb(dirname,"RNGkEpsilon")
                self.ui.epsilon_frame.setEnabled(True)
                self.ui.nut_frame.setEnabled(False)
                self.ui.nutilda_frame.setEnabled(False)
                self.ui.k_frame.setEnabled(True)
                self.ui.omega_frame.setEnabled(False)
                self.ui.Init_epsilon_frame.setEnabled(True)
                self.ui.Init_nut_frame.setEnabled(False)
                self.ui.Init_nuTilda_frame.setEnabled(False)
                self.ui.Init_k_frame.setEnabled(True)
                self.ui.Init_omega_frame.setEnabled(False)
                subprocess.run(["rm "+dirname+"/0/omega"],shell=True)
                subprocess.run(["rm "+dirname+"/0/nut"],shell=True)
                subprocess.run(["rm "+dirname+"/0/nuTilda"],shell=True)
                subprocess.run(["cp -f $FOAM_TUTORIALS/incompressible/simpleFoam/pitzDaily/0/k "+\
                                dirname+"/0"],shell=True)
                subprocess.run(["pyFoamCreateBoundaryPatches.py --verbose --fix-types "+\
                                dirname+"/0/k"],shell=True)
                subprocess.run(["pyFoamCreateBoundaryPatches.py --verbose --clear-unused "+\
                                dirname+"/0/k"],shell=True)
                subprocess.run(["cp -f $FOAM_TUTORIALS/incompressible/simpleFoam/pitzDaily/0/epsilon "\
                                +dirname+"/0"],shell=True)
                subprocess.run(["pyFoamCreateBoundaryPatches.py --verbose --fix-types "+\
                                dirname+"/0/epsilon"],shell=True)
                subprocess.run(["pyFoamCreateBoundaryPatches.py --verbose --clear-unused "+\
                                dirname+"/0/epsilon"],shell=True)
            elif j == 5:
                prop.editTurb(dirname,"LienLeschziner")
                self.ui.epsilon_frame.setEnabled(True)
                self.ui.nut_frame.setEnabled(False)
                self.ui.nutilda_frame.setEnabled(False)
                self.ui.k_frame.setEnabled(True)
                self.ui.omega_frame.setEnabled(False)
                self.ui.Init_epsilon_frame.setEnabled(True)
                self.ui.Init_nut_frame.setEnabled(False)
                self.ui.Init_nuTilda_frame.setEnabled(False)
                self.ui.Init_k_frame.setEnabled(True)
                self.ui.Init_omega_frame.setEnabled(False)
                subprocess.run(["rm "+dirname+"/0/omega"],shell=True)
                subprocess.run(["rm "+dirname+"/0/nut"],shell=True)
                subprocess.run(["rm "+dirname+"/0/nuTilda"],shell=True)
                subprocess.run(["cp -f $FOAM_TUTORIALS/incompressible/simpleFoam/pitzDaily/0/k "+\
                                dirname+"/0"],shell=True)
                subprocess.run(["pyFoamCreateBoundaryPatches.py --verbose --fix-types "+\
                                dirname+"/0/k"],shell=True)
                subprocess.run(["pyFoamCreateBoundaryPatches.py --verbose --clear-unused "+\
                                dirname+"/0/k"],shell=True)
                subprocess.run(["cp -f $FOAM_TUTORIALS/incompressible/simpleFoam/pitzDaily/0/epsilon "+\
                                dirname+"/0"],shell=True)
                subprocess.run(["pyFoamCreateBoundaryPatches.py --verbose --fix-types "+\
                                dirname+"/0/epsilon"],shell=True)
                subprocess.run(["pyFoamCreateBoundaryPatches.py --verbose --clear-unused "+\
                                dirname+"/0/epsilon"],shell=True)
            elif j == 6:
                prop.editTurb(dirname,"laminar")
                self.ui.turb_tab.setEnabled(False)
                self.ui.Init_epsilon_frame.setEnabled(False)
                self.ui.Init_nut_frame.setEnabled(False)
                self.ui.Init_nuTilda_frame.setEnabled(False)
                self.ui.Init_k_frame.setEnabled(False)
                self.ui.Init_omega_frame.setEnabled(False)
        elif self.ui.LESDES_btn.isChecked() == True:
            if j == 5:
                prop.editTurb(dirname,"laminar")
                self.ui.turb_tab.setEnabled(False)
                self.ui.Init_epsilon_frame.setEnabled(False)
                self.ui.Init_nut_frame.setEnabled(False)
                self.ui.Init_nuTilda_frame.setEnabled(False)
                self.ui.Init_k_frame.setEnabled(False)
                self.ui.Init_omega_frame.setEnabled(False)
            else:
                print("feature not yet implemented in OpenFoam GUI")
                
    def transportModel (self):
        j=self.ui.comboBox_26.currentIndex()
        if j == 1:
            prop.editTransport(dirname,"Newtonian")
    
    #***********************FUNCTIONS MATERIALS TAB**************************#
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
          
    #****************FUNCTIONS FIELDS INITIALISATION TAB**********************#
    def selectTypePField (self):
        j=self.ui.comboBox_43.currentText()
        if j == "Potential Flow":
            self.ui.comboBox_44.setCurrentIndex(1)
            self.ui.lineEdit_25.setText("0")
        elif j ==  "Uniform fixed value":
            self.ui.comboBox_44.setCurrentIndex(2)
            self.ui.lineEdit_25.clear()
            
    def selectTypeUField (self):
        j=self.ui.comboBox_44.currentText()
        if j == "Potential Flow":
            self.ui.comboBox_43.setCurrentIndex(1)
            self.ui.lineEdit_26.setText("0")
            self.ui.lineEdit_27.setText("0")
            self.ui.lineEdit_28.setText("0")
        elif j == "Uniform fixed values":
            self.ui.comboBox_43.setCurrentIndex(2)
            self.ui.lineEdit_26.clear()
            self.ui.lineEdit_27.clear()
            self.ui.lineEdit_28.clear()
    
    def setDefaultPField (self):
        self.ui.lineEdit_25.setText("0")
        
    def setDefaultUField (self):
        self.ui.lineEdit_26.setText("0")
        self.ui.lineEdit_27.setText("0")
        self.ui.lineEdit_28.setText("0")
        
    def setPFieldInit (self):
        Pval=float(self.ui.lineEdit_25.text()/rho)
        f_init.writePFieldInit(dirname,Pval)
        
    def setUFieldInit (self):
        Uval=[float(self.ui.lineEdit_26.text()),\
              float(self.ui.lineEdit_27.text()),\
              float(self.ui.lineEdit_28.text())]
        f_init.writeUFieldInit(dirname,Uval)
        
    def setkFieldInit (self):
        kval=float(self.ui.lineEdit_29.text())
        f_init.writekFieldInit(dirname,kval)
        
    def setEpsilonFieldInit (self):
        epsilonval=float(self.ui.lineEdit_130.text())
        f_init.writeEpsilonFieldInit(dirname,epsilonval)
        
    def setOmegaFieldInit (self):
        omegaval=float(self.ui.lineEdit_131.text())
        f_init.writeOmegaFieldInit(dirname,omegaval)
        
    def setNutFieldInit (self):
        nutval=float(self.ui.lineEdit_132.text())
        f_init.writeNutFieldInit(dirname,nutval)
        
    def setNuTildaFieldInit (self):
        nuTildaval=float(self.ui.lineEdit_133.text())
        f_init.writeNuTildaFieldInit(dirname,nuTildaval)
    #**********************FUNCTIONS BOUNDARY CONDITIONS TAB******************#
    def seeBoundaries (self):
        for i in range(0,len(PatchInfo),2):
            self.ui.listWidget.addItem(PatchInfo[i]+"  "+chr(187)+"  "+PatchInfo[i+1])
        #Update field dictionaries p and U
        subprocess.run(["pyFoamCreateBoundaryPatches.py --verbose --fix-types "+\
                        dirname+"/0/p"],shell=True)
        subprocess.run(["pyFoamCreateBoundaryPatches.py --verbose --clear-unused "+\
                        dirname+"/0/p"],shell=True)
        subprocess.run(["pyFoamCreateBoundaryPatches.py --verbose --fix-types "+\
                        dirname+"/0/U"],shell=True)
        subprocess.run(["pyFoamCreateBoundaryPatches.py --verbose --clear-unused "+\
                        dirname+"/0/U"],shell=True)
        
    def clearList (self):
        self.ui.listWidget.clear()
            
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
            
    def pInletTypes (self):
        j=self.ui.comboBox_5.currentText()
        if j == "fixedValue" or j == "totalPressure":
            self.ui.label_22.setEnabled(True)
            self.ui.lineEdit_3.setEnabled(True)
        else:
            self.ui.label_22.setEnabled(False)
            self.ui.lineEdit_3.setEnabled(False)
            
    def pOutletTypes (self):
        j=self.ui.comboBox_6.currentText()
        if j == "fixedValue" or j == "totalPressure":
            self.ui.label_26.setEnabled(True)
            self.ui.lineEdit_4.setEnabled(True)
        else:
            self.ui.label_26.setEnabled(False)
            self.ui.lineEdit_4.setEnabled(False)
            
    def kTypes (self):
        j=self.ui.comboBox_38.currentText()
        if j == "fixedValue" or j == "kqRWallFunction" or j == "inletOutlet":
            self.ui.label_172.setEnabled(True)
            self.ui.lineEdit_121.setEnabled(True)
        else:
            self.ui.label_172.setEnabled(False)
            self.ui.lineEdit_121.setEnabled(False)
            
    def epsilonTypes(self):
        j=self.ui.comboBox_39.currentText()
        if j == "fixedValue" or j == "epsilonWallFunction" or j == "inletOutlet":
            self.ui.label_175.setEnabled(True)
            self.ui.lineEdit_123.setEnabled(True)
        else:
            self.ui.label_175.setEnabled(False)
            self.ui.lineEdit_123.setEnabled(False)
            
    def omegaTypes (self):
        j=self.ui.comboBox_40.currentText()
        if j == "fixedValue" or j == "omegaWallFunction" or j == "inletOutlet":
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
        P_BoundCond=[]
        Patch_name=self.ui.lineEdit.text()
        P_BoundCond.append(self.ui.comboBox_30.currentText())
        b_cond.writePdict(dirname,Patch_name, P_BoundCond)
        self.ui.listWidget_3.addItem("Pressure p: '"+Patch_name+"' "+chr(187)+\
                                     " "+P_BoundCond[0])
        
    def getPressureSymmetry (self):
        global P_BoundCond
        P_BoundCond=[]
        Patch_name=self.ui.lineEdit.text()
        P_BoundCond.append(self.ui.comboBox_28.currentText())
        b_cond.writePdict(dirname,Patch_name,P_BoundCond)
        self.ui.listWidget_3.addItem("Pressure p: '"+Patch_name+"' "+chr(187)+\
                                     " "+P_BoundCond[0])
        
    def getPressureOutlet (self):
        global P_BoundCond
        P_BoundCond=[]
        if self.ui.comboBox_5.currentText() == "freestreamPressure":
            Patch_name=self.ui.lineEdit.text()
            P_BoundCond.append(self.ui.comboBox_6.currentText())
            b_cond.writePdict(dirname,Patch_name,P_BoundCond)
            self.ui.listWidget_3.addItem("Pressure p: '"+Patch_name+"' "+chr(187)+\
                                         " "+P_BoundCond[0])
        else:
            Patch_name=self.ui.lineEdit.text()
            P_BoundCond.append(self.ui.comboBox_6.currentText())
            P_BoundCond.append(float(self.ui.lineEdit_4.text())/rho)
            self.ui.lineEdit_4.clear()
            b_cond.writePdict(dirname,Patch_name,P_BoundCond)
            self.ui.listWidget_3.addItem("Pressure p: '"+Patch_name+"' "+chr(187)+\
                                         " "+P_BoundCond[0]+" / value = "+\
                                         str(P_BoundCond[1]))
            
    def getPressureInlet (self):
        global P_BoundCond
        P_BoundCond=[]
        if self.ui.comboBox_5.currentText() == "freestreamPressure":    
            Patch_name=self.ui.lineEdit.text()
            P_BoundCond.append(self.ui.comboBox_5.currentText())
            b_cond.writePdict(dirname,Patch_name,P_BoundCond)
            self.ui.listWidget_3.addItem("Pressure p: '"+Patch_name+"' "+chr(187)+\
                                         " "+P_BoundCond[0])
        else:
            Patch_name=self.ui.lineEdit.text()
            P_BoundCond.append(self.ui.comboBox_5.currentText())
            P_BoundCond.append(float(self.ui.lineEdit_3.text())/rho)
            self.ui.lineEdit_3.clear()
            b_cond.writePdict(dirname,Patch_name,P_BoundCond)
            self.ui.listWidget_3.addItem("Pressure p: '"+Patch_name+"' "+chr(187)+\
                                         " "+P_BoundCond[0]+" / value = "+\
                                         str(P_BoundCond[1]))
            
    def getFlowInlet (self):
        global P_BoundCond
        P_BoundCond=[]
        Patch_name=self.ui.lineEdit.text()
        P_BoundCond.append(self.ui.comboBox_29.currentText())
        b_cond.writePdict(dirname,Patch_name,P_BoundCond)
        self.ui.listWidget_3.addItem("Pressure p: '"+Patch_name+"' "+chr(187)+\
                                     " "+P_BoundCond[0])
        
    def getPressureEmpty (self):
        global P_BoundCond
        P_BoundCond=[]
        Patch_name=self.ui.lineEdit.text()
        P_BoundCond.append(self.ui.comboBox_31.currentText())
        b_cond.writePdict(dirname,Patch_name,P_BoundCond)
        self.ui.listWidget_3.addItem("Pressure p: '"+Patch_name+"' "+chr(187)+\
                                     " "+P_BoundCond[0])
        
    def getVelocityInlet (self):
        global U_BoundCond
        U_BoundCond=[]
        Patch_name=self.ui.lineEdit_2.text()
        U_BoundCond.append(self.ui.comboBox_32.currentText())
        U_BoundCond.append(float(self.ui.lineEdit_5.text()))
        U_BoundCond.append(float(self.ui.lineEdit_6.text()))
        U_BoundCond.append(float(self.ui.lineEdit_7.text()))
        self.ui.lineEdit_5.clear()
        self.ui.lineEdit_6.clear()
        self.ui.lineEdit_7.clear()
        b_cond.writeUdict(dirname,Patch_name,U_BoundCond)
        self.ui.listWidget_3.addItem("Velocity U: '"+Patch_name+"' "+chr(187)+\
                                     " "+U_BoundCond[0]+" / value = ("+\
                                     str(U_BoundCond[1])+" "+\
                                     str(U_BoundCond[2])+" "+\
                                     str(U_BoundCond[3])+")")
        
    def getVelocityOutlet (self):
        global U_BoundCond
        U_BoundCond=[]
        Patch_name=self.ui.lineEdit_2.text()
        U_BoundCond.append(self.ui.comboBox_33.currentText())
        U_BoundCond.append(float(self.ui.lineEdit_8.text()))
        U_BoundCond.append(float(self.ui.lineEdit_9.text()))
        U_BoundCond.append(float(self.ui.lineEdit_10.text()))
        self.ui.lineEdit_8.clear()
        self.ui.lineEdit_9.clear()
        self.ui.lineEdit_10.clear()
        b_cond.writeUdict(dirname,Patch_name,U_BoundCond)
        self.ui.listWidget_3.addItem("Velocity U: '"+Patch_name+"' "+chr(187)+\
                                     " "+U_BoundCond[0]+" / value = ("+\
                                     str(U_BoundCond[1])+" "+\
                                     str(U_BoundCond[2])+" "+\
                                     str(U_BoundCond[3])+")")
        
    def getInletOutlet (self):
        global U_BoundCond
        U_BoundCond=[]
        Patch_name=self.ui.lineEdit_2.text()
        U_BoundCond.append(self.ui.comboBox_12.currentText())
        U_BoundCond.append(float(self.ui.lineEdit_11.text()))
        U_BoundCond.append(float(self.ui.lineEdit_12.text()))
        U_BoundCond.append(float(self.ui.lineEdit_13.text()))
        U_BoundCond.append(float(self.ui.lineEdit_117.text()))
        U_BoundCond.append(float(self.ui.lineEdit_118.text()))
        U_BoundCond.append(float(self.ui.lineEdit_119.text()))
        self.ui.lineEdit_11.clear()
        self.ui.lineEdit_12.clear()
        self.ui.lineEdit_13.clear()
        self.ui.lineEdit_117.clear()
        self.ui.lineEdit_118.clear()
        self.ui.lineEdit_119.clear()
        b_cond.writeUdict(dirname,Patch_name,U_BoundCond)
        self.ui.listWidget_3.addItem("Velocity U: '"+Patch_name+"' "+\
                                     chr(187)+" "+U_BoundCond[0]+\
                                     " / inlet value = ("+\
                                     str(U_BoundCond[1])+" "+\
                                     str(U_BoundCond[2])+" "+\
                                     str(U_BoundCond[3])+\
                                     ") / value = ("+\
                                     str(U_BoundCond[4])+" "+\
                                     str(U_BoundCond[5])+" "+\
                                     str(U_BoundCond[6])+")")
        
    def getOutflow (self):
        global U_BoundCond
        U_BoundCond=[]
        Patch_name=self.ui.lineEdit_2.text()
        U_BoundCond.append(self.ui.comboBox_34.currentText())
        b_cond.writeUdict(dirname,Patch_name,U_BoundCond)
        self.ui.listWidget_3.addItem("Velocity U: '"+Patch_name+"' "+chr(187)+\
                                     " "+U_BoundCond[0])
        
    def getVelocitySymmetry (self):
        global U_BoundCond
        U_BoundCond=[]
        Patch_name=self.ui.lineEdit_2.text()
        U_BoundCond.append(self.ui.comboBox_35.currentText())
        b_cond.writeUdict(dirname,Patch_name,U_BoundCond)
        self.ui.listWidget_3.addItem("Velocity U: '"+Patch_name+"' "+chr(187)+\
                                     " "+U_BoundCond[0])
        
    def getVelocityWall (self):
        global U_BoundCond
        U_BoundCond=[]
        Patch_name=self.ui.lineEdit_2.text()
        U_BoundCond.append(self.ui.comboBox_36.currentText())
        b_cond.writeUdict(dirname,Patch_name,U_BoundCond)
        self.ui.listWidget_3.addItem("Velocity U: '"+Patch_name+"' "+chr(187)+\
                                     " "+U_BoundCond[0])
        
    def getVelocityEmpty (self):
        global U_BoundCond
        U_BoundCond=[]
        Patch_name=self.ui.lineEdit_2.text()
        U_BoundCond.append(self.ui.comboBox_37.currentText())
        b_cond.writeUdict(dirname,Patch_name,U_BoundCond)
        self.ui.listWidget_3.addItem("Velocity U: '"+Patch_name+"' "+chr(187)+\
                                     " "+U_BoundCond[0])
        
    def getkBoundConds (self):
        global k_BoundCond
        k_BoundCond=[]
        if self.ui.comboBox_38.currentText() == "fixedValue" or \
        self.ui.comboBox_38.currentText() == "kqRWallFunction":
            Patch_name=self.ui.lineEdit_120.text()
            k_BoundCond.append(self.ui.comboBox_38.currentText())
            k_BoundCond.append(float(self.ui.lineEdit_121.text()))
            self.ui.lineEdit_121.clear()
            b_cond.write_k_dict(dirname,Patch_name,k_BoundCond)
            self.ui.listWidget_3.addItem("Parameter k: '"+Patch_name+"' "+\
                                         chr(187)+" "+k_BoundCond[0]+\
                                         " / value = "+str(k_BoundCond[1]))
            
        elif self.ui.comboBox_38.currentText() == "inletOutlet":
            Patch_name=self.ui.lineEdit_120.text()
            k_BoundCond.append(self.ui.comboBox_38.currentText())
            k_BoundCond.append(float(self.ui.lineEdit_121.text()))
            self.ui.lineEdit_121.clear()
            b_cond.write_k_dict(dirname,Patch_name,k_BoundCond)
            self.ui.listWidget_3.addItem("Parameter k: '"+Patch_name+"' "+\
                                         chr(187)+" "+k_BoundCond[0]+\
                                         " / inlet value (reverse flow) = uniform 0 / value = "+\
                                         str(k_BoundCond[1]))
            
        else:
            Patch_name=self.ui.lineEdit_120.text()
            k_BoundCond.append(self.ui.comboBox_38.currentText())
            b_cond.write_k_dict(dirname,Patch_name,k_BoundCond)
            self.ui.listWidget_3.addItem("Parameter k: '"+Patch_name+"' "+\
                                         chr(187)+" "+k_BoundCond[0])
        
        
        
    def getEpsilonBoundConds (self):
        global epsilon_BoundCond
        epsilon_BoundCond=[]
        if self.ui.comboBox_39.currentText() == "fixedValue" or \
        self.ui.comboBox_39.currentText() == "epsilonWallFunction":
            Patch_name=self.ui.lineEdit_122.text()
            epsilon_BoundCond.append(self.ui.comboBox_39.currentText())
            epsilon_BoundCond.append(float(self.ui.lineEdit_123.text()))
            self.ui.lineEdit_123.clear()
            b_cond.write_epsilon_dict(dirname,Patch_name,epsilon_BoundCond)
            self.ui.listWidget_3.addItem("Parameter epsilon: '"+Patch_name+"' "+\
                                         chr(187)+" "+epsilon_BoundCond[0]+\
                                         " / value = "+\
                                         str(epsilon_BoundCond[1]))
            
        elif self.ui.comboBox_39.currentText() == "inletOutlet":
            Patch_name=self.ui.lineEdit_122.text()
            epsilon_BoundCond.append(self.ui.comboBox_39.currentText())
            epsilon_BoundCond.append(float(self.ui.lineEdit_123.text()))
            self.ui.lineEdit_123.clear()
            b_cond.write_epsilon_dict(dirname,Patch_name,epsilon_BoundCond)
            self.ui.listWidget_3.addItem("Parameter epsilon: '"+Patch_name+"' "+\
                                         chr(187)+" "+epsilon_BoundCond[0]+\
                                         " / inlet value (reverse flow) = uniform 0 / value = "+\
                                         str(epsilon_BoundCond[1]))
            
        else:
            Patch_name=self.ui.lineEdit_122.text()
            epsilon_BoundCond.append(self.ui.comboBox_39.currentText())
            b_cond.write_epsilon_dict(dirname,Patch_name,epsilon_BoundCond)
            self.ui.listWidget_3.addItem("Parameter epsilon: '"+Patch_name+"' "+\
                                         chr(187)+" "+epsilon_BoundCond[0])
        
        
    def getOmegaBoundConds (self):
        global omega_BoundCond
        omega_BoundCond=[]
        if self.ui.comboBox_40.currentText() == "fixedValue" or \
        self.ui.comboBox_40.currentText() == "omegaWallFunction":
            Patch_name=self.ui.lineEdit_124.text()
            omega_BoundCond.append(self.ui.comboBox_40.currentText())
            omega_BoundCond.append(float(self.ui.lineEdit_125.text()))
            self.ui.lineEdit_125.clear()
            b_cond.write_omega_dict(dirname,Patch_name,omega_BoundCond)
            self.ui.listWidget_3.addItem("Parameter omega: '"+Patch_name+"' "+\
                                         chr(187)+" "+omega_BoundCond[0]+\
                                         " / value = "+str(omega_BoundCond[1]))
            
        elif self.ui.comboBox_40.currentText() == "inletOutlet":
            Patch_name=self.ui.lineEdit_124.text()
            omega_BoundCond.append(self.ui.comboBox_40.currentText())
            omega_BoundCond.append(float(self.ui.lineEdit_125.text()))
            self.ui.lineEdit_125.clear()
            b_cond.write_omega_dict(dirname,Patch_name,omega_BoundCond)
            self.ui.listWidget_3.addItem("Parameter omega: '"+Patch_name+"' "+\
                                         chr(187)+" "+omega_BoundCond[0]+\
                                         " / inlet value (reverse flow) = uniform 0 / value = "+\
                                         str(omega_BoundCond[1]))
            
        else:
            Patch_name=self.ui.lineEdit_124.text()
            omega_BoundCond.append(self.ui.comboBox_40.currentText())
            b_cond.write_omega_dict(dirname,Patch_name,omega_BoundCond)
            self.ui.listWidget_3.addItem("Parameter omega: '"+Patch_name+"' "+\
                                         chr(187)+" "+omega_BoundCond[0])
        
        
    def getNutBoundConds (self):
        global nut_BoundCond
        nut_BoundCond=[]
        if self.ui.comboBox_41.currentText() == "empty":
            Patch_name=self.ui.lineEdit_126.text()
            nut_BoundCond.append(self.ui.comboBox_41.currentText())
            b_cond.write_nut_dict(dirname,Patch_name,nut_BoundCond)
            self.ui.listWidget_3.addItem("Parameter nut: '"+Patch_name+"' "+\
                                         chr(187)+" "+nut_BoundCond[0])
            
        else:
            Patch_name=self.ui.lineEdit_126.text()
            nut_BoundCond.append(self.ui.comboBox_41.currentText())
            nut_BoundCond.append(float(self.ui.lineEdit_127.text()))
            self.ui.lineEdit_127.clear()
            b_cond.write_nut_dict(dirname,Patch_name,nut_BoundCond)
            self.ui.listWidget_3.addItem("Parameter nut: '"+Patch_name+"' "+\
                                         chr(187)+" "+nut_BoundCond[0]+\
                                         " / value = "+str(nut_BoundCond[1]))
        
        
    def getNuTildaBoundConds (self):
        global nuTilda_BoundCond
        nuTilda_BoundCond=[]
        if self.ui.comboBox_42.currentText() == "freestream" or \
        self.ui.comboBox_42.currentText() == "fixedValue":
            Patch_name=self.ui.lineEdit_128.text()
            nuTilda_BoundCond.append(self.ui.comboBox_42.currentText())
            nuTilda_BoundCond.append(float(self.ui.lineEdit_129.text()))
            self.ui.lineEdit_129.clear()
            b_cond.write_nuTilda_dict(dirname,Patch_name,nuTilda_BoundCond)
            self.ui.listWidget_3.addItem("Parameter nuTilda: '"+Patch_name+"' "+\
                                         chr(187)+" "+nuTilda_BoundCond[0]+\
                                         " / value = "+str(nuTilda_BoundCond[1]))
        else:
            Patch_name=self.ui.lineEdit_128.text()
            nuTilda_BoundCond.append(self.ui.comboBox_42.currentText())
            b_cond.write_nuTilda_dict(dirname,Patch_name,nuTilda_BoundCond)
            self.ui.listWidget_3.addItem("Parameter nuTilda: '"+Patch_name+"' "+\
                                         chr(187)+" "+nuTilda_BoundCond[0])
            
    #*********************FUNCTIONS NUMERICAL SCHEMES TAB*********************#
    def setDefaultNumSchemes (self):
        self.ui.comboBox_7.setCurrentIndex(1)
        self.ui.comboBox_9.setCurrentIndex(1)
        self.ui.comboBox_10.setCurrentIndex(1)
        self.ui.comboBox_11.setCurrentIndex(1)
        
    def setNumSchemes (self):
        ddtScheme=self.ui.comboBox_2.currentText()
        gradScheme=self.ui.comboBox_7.currentText()
        laplacianScheme=self.ui.comboBox_9.currentText()
        interpScheme=self.ui.comboBox_10.currentText()
        snGradScheme=self.ui.comboBox_11.currentText()
        subprocess.run(["cp -f $FOAM_TUTORIALS/incompressible/simpleFoam/pitzDaily/system/fvSchemes "+\
                        dirname+"/system"], shell=True)
        subprocess.run(["pyFoamWriteDictionary.py --strip-quotes-from-value "+\
                        dirname+"/system/fvSchemes "+'"'+"ddtSchemes['default']"+\
                        '" '+"'"+ddtScheme+"'"], shell=True)
        subprocess.run(["pyFoamWriteDictionary.py --strip-quotes-from-value "+\
                        dirname+"/system/fvSchemes "+'"'+"gradSchemes['default']"+\
                        '" '+"'"+gradScheme+"'"], shell=True)
        subprocess.run(["pyFoamWriteDictionary.py --strip-quotes-from-value "+\
                        dirname+"/system/fvSchemes "+'"'+"laplacianSchemes['default']"+\
                        '" '+"'"+laplacianScheme+"'"], shell=True)
        subprocess.run(["pyFoamWriteDictionary.py --strip-quotes-from-value "+\
                        dirname+"/system/fvSchemes "+'"'+"interpolationSchemes['default']"+\
                        '" '+"'"+interpScheme+"'"], shell=True)
        subprocess.run(["pyFoamWriteDictionary.py --strip-quotes-from-value "+\
                        dirname+"/system/fvSchemes "+'"'+"snGradSchemes['default']"+\
                        '" '+"'"+snGradScheme+"'"], shell=True)
    
    #**********************FUNCTIONS RUNTIME CONTROLS TAB*********************#
    def setDefaultRuntimeCtrls (self):
        #Default time settings
        self.ui.comboBox_13.setCurrentIndex(3)
        self.ui.lineEdit_14.setText("0")
        self.ui.comboBox_19.setCurrentIndex(1)
        self.ui.lineEdit_15.setText("500")
        self.ui.lineEdit_16.setText("1")
        #Default data writing settings
        self.ui.comboBox_14.setCurrentIndex(1)
        self.ui.lineEdit_21.setText("100")
        self.ui.lineEdit_22.setText("0")
        self.ui.comboBox_15.setCurrentIndex(2)
        self.ui.lineEdit_23.setText("6")
        self.ui.comboBox_16.setCurrentIndex(1)
        self.ui.comboBox_17.setCurrentIndex(3)
        self.ui.lineEdit_24.setText("6")
        self.ui.comboBox_18.setCurrentIndex(1)
        self.ui.comboBox_20.setCurrentIndex(1)
        
    def setRuntimeCtrls (self):
        TimeSettings=[self.ui.comboBox_13.currentText(),\
                      self.ui.lineEdit_14.text(),\
                      self.ui.comboBox_19.currentText(),\
                      self.ui.lineEdit_15.text(),\
                      self.ui.lineEdit_16.text()]
        WritingSettings=[self.ui.comboBox_14.currentText(),\
                         self.ui.lineEdit_21.text(),\
                         self.ui.lineEdit_22.text(),\
                         self.ui.comboBox_15.currentText(),\
                         self.ui.lineEdit_23.text(),\
                         self.ui.comboBox_16.currentText(),\
                         self.ui.comboBox_17.currentText(),\
                         self.ui.lineEdit_24.text(),\
                         self.ui.comboBox_18.currentText(),\
                         self.ui.comboBox_20.currentText()]
        R_ctrls.writeRCtrls(dirname,TimeSettings,WritingSettings)
        
    #***************************FUNCTIONS SOLVER TAB**************************#
    def setSolverApp (self):
        j=self.ui.comboBox_21.currentText()
        Pot_Init=self.ui.comboBox_43.currentText()
        if j == "potentialFoam":
            solver=j
            nonOrthogonal=self.ui.spinBox.value()
            solv.writeSolverApp(dirname,solver,Pot_Init,nonOrthogonal)
            self.ui.frame.setEnabled(True)
        elif j == "simpleFoam":
            solver=j
            nonOrthogonal=self.ui.spinBox.value()
            solv.writeSolverApp(dirname,solver,Pot_Init,nonOrthogonal)
            self.ui.frame.setEnabled(True)
            
    def loadListParam (self):
        j=self.ui.comboBox_21.currentText()
        global params
        params=[]
        if j == "potentialFoam":
            self.ui.listWidget_4.addItem("Pressure p")
            params.append("p")
            self.ui.listWidget_4.addItem("Velocity potential Phi")
            params.append("Phi")
            self.ui.checkBox.setEnabled(False)
        elif j == "simpleFoam":
            self.ui.listWidget_4.addItem("Pressure p")
            params.append("p")
            self.ui.listWidget_4.addItem("Velocity U")
            params.append("U")
            self.ui.checkBox.setEnabled(True)
        k=self.ui.comboBox.currentText()
        if k == "k-w SST":
            self.ui.listWidget_4.addItem("Turbulence param. k")
            params.append("k")
            self.ui.listWidget_4.addItem("Turbulence param. omega")
            params.append("omega")
        elif k == "Spalart-Allmaras":
            self.ui.listWidget_4.addItem("Turbulence param. nuTilda")
            params.append("nuTilda")
        elif k == "Realizable k-epsilon" or k == "RNG k-epsilon" or \
        k == "Lien-Leschziner":
            self.ui.listWidget_4.addItem("Turbulence param. k")
            params.append("k")
            self.ui.listWidget_4.addItem("Turbulence param. epsilon")
            params.append("epsilon")
            
    def ActivDefault (self):
        self.ui.pushButton_23.setEnabled(True)
        
    def ActivRelaxFact (self):
        j=self.ui.checkBox.isChecked()
        if j == True:
            self.ui.lineEdit_33.setEnabled(True)
        elif j == False:
            self.ui.lineEdit_33.setEnabled(False)
    
    def defaultSettingsParam (self):
        k=self.ui.comboBox_21.currentText()
        if k == "potentialFoam":
            j=self.ui.listWidget_4.currentItem().text()
            print(j)
            if j[0:10] == "Pressure p":
                self.ui.lineEdit_30.setText("1e-6")
                self.ui.lineEdit_17.setText("1e-4")
                if self.ui.checkBox.isChecked() == True:
                    self.ui.lineEdit_33.setText("0.3")
            elif j[0:22] == "Velocity potential Phi":
                self.ui.lineEdit_17.setText("1e-6")
                self.ui.lineEdit_17.setText("1e-4")
        else:
            j=self.ui.listWidget_4.currentItem().text()
            if j[0:10] == "Pressure p":
                self.ui.lineEdit_30.setText("1e-6")
                self.ui.lineEdit_17.setText("1e-4")
                if self.ui.checkBox.isChecked() == True:
                    self.ui.lineEdit_33.setText("0.3")
            elif j[0:10] == "Velocity U":
                self.ui.lineEdit_30.setText("1e-6")
                self.ui.lineEdit_17.setText("1e-4")
                if self.ui.checkBox.isChecked() == True:
                    self.ui.lineEdit_33.setText("0.7")
            elif j[0:19] == "Turbulence param. k":
                self.ui.lineEdit_30.setText("1e-6")
                self.ui.lineEdit_17.setText("1e-4")
                if self.ui.checkBox.isChecked() == True:
                    self.ui.lineEdit_33.setText("0.7")
            elif j[0:23] == "Turbulence param. omega":
                self.ui.lineEdit_30.setText("1e-6")
                self.ui.lineEdit_17.setText("1e-4")
                if self.ui.checkBox.isChecked() == True:
                    self.ui.lineEdit_33.setText("0.7")
            elif j[0:25] == "Turbulence param. epsilon":
                self.ui.lineEdit_30.setText("1e-6")
                self.ui.lineEdit_17.setText("1e-4")
                if self.ui.checkBox.isChecked() == True:
                    self.ui.lineEdit_33.setText("0.7")
            elif j[0:25] == "Turbulence param. nuTilda":
                self.ui.lineEdit_30.setText("1e-6")
                self.ui.lineEdit_17.setText("1e-4")
                if self.ui.checkBox.isChecked() == True:
                    self.ui.lineEdit_33.setText("0.7")
      
    def applySettingsParam (self):
        item=self.ui.listWidget_4.currentItem()
        Param=self.ui.listWidget_4.currentItem().text()
        global residuals
        global relaxFactors
        if Param[0:10] == "Pressure p":
            Param=Param[0:10]
            residuals['p']=self.ui.lineEdit_17.text()
            relaxFactors['p']=self.ui.lineEdit_33.text()
        elif Param[0:22] == "Velocity potential Phi":
            Param=Param[0:22]
        elif Param[0:10] == "Velocity U":
            Param=Param[0:10]
            residuals['U']=self.ui.lineEdit_17.text()
            relaxFactors['U']=self.ui.lineEdit_33.text()
        elif Param[0:19] == "Turbulence param. k":
            Param=Param[0:19]
            residuals['k']=self.ui.lineEdit_17.text()
            relaxFactors['k']=self.ui.lineEdit_33.text()
        elif Param[0:23] == "Turbulence param. omega":
            Param=Param[0:23]
            residuals['omega']=self.ui.lineEdit_17.text()
            relaxFactors['omega']=self.ui.lineEdit_33.text()
        elif Param[0:25] == "Turbulence param. epsilon":
            Param=Param[0:25]
            residuals['epsilon']=self.ui.lineEdit_17.text()
            relaxFactors['epsilon']=self.ui.lineEdit_33.text()
        elif Param[0:25] == "Turbulence param. nuTilda":
            Param=Param[0:25]
            residuals['nuTilda']=self.ui.lineEdit_17.text()
            relaxFactors['nuTilda']=self.ui.lineEdit_33.text()
        Tol=self.ui.lineEdit_30.text()
        Res=self.ui.lineEdit_17.text()
        if Res == None:
            Res="No"
        j=self.ui.checkBox.isChecked()
        if j == True:
            Relax=self.ui.lineEdit_33.text()
        elif j == False:
            Relax="No"
        
        solv.writeResidualsRelax(dirname,params,residuals,relaxFactors)
        solv.writeSettingsSolvers(dirname,Param,Tol,Relax)
        item.setText(Param+" | Tolerance: "+Tol+" | Residual Control: "+Res+\
                     " | Relax. Factor: "+Relax)
    
    def RUN (self):
        solver_name=self.ui.comboBox_21.currentText()
        logFile_name=self.ui.lineEdit_34.text()
        os.chdir(dirname)
        solv.RUN_function(solver_name,logFile_name)
        
    
    

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.setWindowTitle("OpenFOAM GUI")
    window.show()
    sys.exit(app.exec_())
