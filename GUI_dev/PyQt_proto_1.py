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
	self.ui.widget_from_file.hide()
	self.ui.widget_userdefined.hide()
	self.ui.sel_mesh_source.currentIndexChanged.connect(self.SelectionMesh)
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
	text, ok = QInputDialog.getText(self, 'Case Name', 'Enter name for the new case:')
	if ok:
		fopt.NewCase(text)
		fopt.ShowDialog()

    def closeEvent(self, event):
    	print "Closing"
    	self.deleteLater() 
  
    def SelectionMesh (self):
	i=self.ui.sel_mesh_source.currentText()
	if i == "From File" :
		self.ui.widget_userdefined.hide()        	
		self.ui.widget_from_file.show()
    	else:
		self.ui.widget_from_file.hide()        	
		self.ui.widget_userdefined.show()

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
	window.show()
	sys.exit(app.exec_())
