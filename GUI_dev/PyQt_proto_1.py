#!/usr/bin/python

import sys
import File_options as fopt
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QInputDialog, QMessageBox

qtCreatorFile = "proto_1.ui" # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtWidgets.QTabWidget):
    def __init__(self):
        super(MyApp,self).__init__()
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        #FILE TAB
        self.ui.New_case.clicked.connect(self.NameDialog)
        self.ui.Exit.clicked.connect(self.closeEvent)
        # MESH TAB
        #Vertices definition:
        global VertList,NumVerts
        VertList=[]
        NumVerts=0
        self.ui.Add_vert.clicked.connect(self.AddVertex)
        self.ui.Reset_vert.clicked.connect(self.ResetVertex)
        #Curved edges definition:
        global EdgeType,EdgeVertNum,InterpolPoints
        self.ui.comboBox_22.currentIndexChanged.connect(self.GetEdgeType)
        EdgeVertNum=[]
        self.ui.Add_edgevert.clicked.connect(self.AddEdgeVert)
        InterpolPoints=[]
        self.ui.Add_interp.clicked.connect(self.AddInterpPoints)
        self.ui.Reset_curvedg.clicked.connect(self.ResetCurvEdges)
        #Simple grading or Edge grading -> enabled / disabled:
        self.ui.checkBox_2.stateChanged.connect(self.SimplGrad)
        self.ui.checkBox_3.stateChanged.connect(self.EdgeGrad)
        #Blocks definition:
        Nblock=self.ui.Nblock_btn.clicked.connect(self.GetNBlock)
        global DataBlock, BlockCounter, gradType
        DataBlock=[[Nblock] for i in range(23)]
        BlockCounter=0
        self.ui.Create_block.clicked.connect(self.CreateBlock)
        self.ui.Reset_block.clicked.connect(self.ResetBlock)
        #Get boundaries:
        global VfacesBound,PatchInfo,NumBounds
        VfacesBound=[]
        PatchInfo=[]
        NumBounds=0
        self.ui.Set_bound.clicked.connect(self.SetBoundary)
        self.ui.Reset_bound.clicked.connect(self.ResetBoundary)
        # BOUND COND TAB
        self.ui.widget_patch.hide()
        self.ui.widget_wall.hide()
        self.ui.widget_empty.hide()
        self.ui.patch_type.currentIndexChanged.connect(self.SelectionPatch)
        # INIT PROPERTIES TAB
        self.ui.label_53.setEnabled(False)
        self.ui.lineEdit_25.setEnabled(False)
        self.ui.lineEdit_26.setEnabled(False)
        self.ui.lineEdit_27.setEnabled(False)    
        self.ui.label_54.setEnabled(False)
        self.ui.checkBox.setEnabled(False)
        self.ui.label_57.setEnabled(False)
        self.ui.lineEdit_29.setEnabled(False)
        self.ui.label_56.setEnabled(False)
        self.ui.lineEdit_28.setEnabled(False)
        self.ui.comboBox_19.currentIndexChanged.connect(self.InitTypeU)
        self.ui.comboBox_20.currentIndexChanged.connect(self.InitTypeP)
        # SOLVER TAB
        self.ui.residualsbtn.setEnabled(False)

    def NameDialog (self):
       text,ok = QInputDialog.getText(self, 'Case Name', 'Enter name for the new case:')
       if ok:
          fopt.NewCase(text)
          fopt.ShowSuccesDialog()

    def closeEvent(self, event):
        print("Closing")
        self.deleteLater()

    def AddVertex (self):
        VertAdd=[int(self.ui.lineEdit_35.text()),int(self.ui.lineEdit_36.text()), int(self.ui.lineEdit_37.text())];
        VertList.append(VertAdd)
        self.ui.lineEdit_35.clear()
        self.ui.lineEdit_36.clear()
        self.ui.lineEdit_37.clear()
        global NumVerts
        NumVerts=len(VertList)
        self.ui.listWidget_2.addItem("Vertex #"+str(NumVerts)+": ["+str(VertAdd[0])+"] ["+str(VertAdd[1])+"] ["+str(VertAdd[2])+"]")
        print(NumVerts)
        print(VertList)
        
    def ResetVertex (self):
        VertList=[]
        global NumVerts
        NumVerts=0
        print(VertList)
        
    def GetEdgeType (self):
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
        
    def AddEdgeVert (self):
        VertEdgeAdd=[int(self.ui.lineEdit_38.text()),int(self.ui.lineEdit_39.text())]
        EdgeVertNum.append(VertEdgeAdd)
        self.ui.lineEdit_38.clear()
        self.ui.lineEdit_39.clear()
        print(EdgeVertNum)
        
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
            
    def GetNBlock (self):
        Nblock=self.ui.lineEdit_102.text()
        return Nblock
    
    def CreateBlock (self):
        FacesVerts=[int(self.ui.lineEdit_43.text()),int(self.ui.lineEdit_44.text()) \
                    ,int(self.ui.lineEdit_45.text()),int(self.ui.lineEdit_46.text()) \
                    ,int(self.ui.lineEdit_47.text()),int(self.ui.lineEdit_48.text()) \
                    ,int(self.ui.lineEdit_49.text()),int(self.ui.lineEdit_50.text())]
        nNodesAxis=[int(self.ui.lineEdit_51.text()),int(self.ui.lineEdit_52.text()) \
                    ,int(self.ui.lineEdit_53.text())]
        if self.ui.checkBox_2.isChecked() == True:
            gradType="simpleGrading"
            gradRatio=[int(self.ui.lineEdit_54.text()),int(self.ui.lineEdit_55.text()) \
                       ,int(self.ui.lineEdit_56.text())]
        elif self.ui.checkBox_3.isChecked() == True:
            gradType="edgeGrading"
            gradRatio=[int(self.ui.lineEdit_57.text()),int(self.ui.lineEdit_58.text()) \
                       ,int(self.ui.lineEdit_59.text()),int(self.ui.lineEdit_60.text()) \
                       ,int(self.ui.lineEdit_61.text()),int(self.ui.lineEdit_62.text()) \
                       ,int(self.ui.lineEdit_63.text()),int(self.ui.lineEdit_64.text()) \
                       ,int(self.ui.lineEdit_65.text()),int(self.ui.lineEdit_66.text()) \
                       ,int(self.ui.lineEdit_67.text()),int(self.ui.lineEdit_68.text())]
        global BlockCounter
        DataBlock[BlockCounter][:]=FacesVerts+nNodesAxis+gradRatio
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
        print(DataBlock[1][:])
        
    def ResetBlock (self):
        DataBlock=[]
        gradType=[]
        global BlockCounter
        BlockCounter=0
        print(gradType)
        print(DataBlock)

    def SetBoundary (self):
        VfacesBound.append([int(self.ui.lineEdit_69.text()),int(self.ui.lineEdit_70.text()), \
                            int(self.ui.lineEdit_71.text()),int(self.ui.lineEdit_72.text())])
        PatchInfo.append(self.ui.lineEdit_73.text())
        PatchInfo.append(self.ui.comboBox_23.currentText())
        self.ui.lineEdit_69.clear()
        self.ui.lineEdit_70.clear()
        self.ui.lineEdit_71.clear()
        self.ui.lineEdit_72.clear()
        self.ui.lineEdit_73.clear()
        global NumBounds
        NumBounds=NumBounds+1
        self.ui.listWidget_2.addItem("'"+PatchInfo[-2]+"' -> "+PatchInfo[-1])
        print(VfacesBound)
        print(PatchInfo)
        
    def ResetBoundary (self):
        global VfacesBound,PatchInfo
        VfacesBound=[]
        PatchInfo=[]
        print(VfacesBound)
        print(PatchInfo)

    def SelectionPatch (self):
        j=self.ui.patch_type.currentText()
        if j == "Patch" :
           self.ui.widget_wall.hide()
           self.ui.widget_empty.hide()        
           self.ui.widget_patch.show()
        elif j == "Wall" :
           self.ui.widget_patch.hide()
           self.ui.widget_empty.hide()
           self.ui.widget_wall.show()
        else:
           self.ui.widget_wall.hide()
           self.ui.widget_patch.hide()
           self.ui.widget_empty.show()

    def InitTypeU (self):
       k=self.ui.comboBox_19.currentText()
       if k == "Default" :
          self.ui.label_53.setEnabled(False)
          self.ui.lineEdit_25.setEnabled(False)
          self.ui.lineEdit_26.setEnabled(False)
          self.ui.lineEdit_27.setEnabled(False)    
          self.ui.label_54.setEnabled(False)
          self.ui.checkBox.setEnabled(False)
          self.ui.label_57.setEnabled(False)
          self.ui.lineEdit_29.setEnabled(False)
          self.ui.label_56.setEnabled(False)
          self.ui.lineEdit_28.setEnabled(False)
          self.ui.comboBox_20.model().item(0).setEnabled(True)
          self.ui.comboBox_20.model().item(1).setEnabled(True)
          self.ui.comboBox_20.model().item(2).setEnabled(False)
       elif k == "Fixed Value" :
          self.ui.label_53.setEnabled(True)
          self.ui.lineEdit_25.setEnabled(True)
          self.ui.lineEdit_26.setEnabled(True)
          self.ui.lineEdit_27.setEnabled(True)
          self.ui.label_54.setEnabled(False)
          self.ui.checkBox.setEnabled(False)
          self.ui.label_57.setEnabled(False)
          self.ui.lineEdit_29.setEnabled(False)
          self.ui.label_56.setEnabled(False)
          self.ui.lineEdit_28.setEnabled(False)
          self.ui.comboBox_20.model().item(0).setEnabled(True)
          self.ui.comboBox_20.model().item(1).setEnabled(True)
          self.ui.comboBox_20.model().item(2).setEnabled(False)
       else:
          self.ui.label_53.setEnabled(False)
          self.ui.lineEdit_25.setEnabled(False)
          self.ui.lineEdit_26.setEnabled(False)
          self.ui.lineEdit_27.setEnabled(False)
          self.ui.label_54.setEnabled(True)
          self.ui.checkBox.setEnabled(True)
          self.ui.label_57.setEnabled(True)
          self.ui.lineEdit_29.setEnabled(True)
          self.ui.comboBox_20.model().item(0).setEnabled(False)
          self.ui.comboBox_20.model().item(1).setEnabled(False)
          self.ui.comboBox_20.model().item(2).setEnabled(True)

    def InitTypeP (self):
       l=self.ui.comboBox_20.currentText()
       if l == "Fixed Value":
          self.ui.label_56.setEnabled(True)
          self.ui.lineEdit_28.setEnabled(True)    
       else:
          self.ui.label_56.setEnabled(False)
          self.ui.lineEdit_28.setEnabled(False)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.setWindowTitle("OpenFOAM GUI")
    window.show()
    sys.exit(app.exec_())
