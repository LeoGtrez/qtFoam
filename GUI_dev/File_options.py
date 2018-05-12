
import sys
import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from PyFoam.Applications.CloneCase import CloneCase

def NewCase (name):
    dlg = QFileDialog()
    dlg.setWindowTitle("Select directory")
    dlg.setFileMode(QFileDialog.Directory)
    global dirname
    if dlg.exec_():
      dirname = dlg.selectedFiles()
    print(dirname[0])
    os.system("pyFoamCloneCase.py $FOAM_TUTORIALS/incompressible/simpleFoam/motorBike "+ dirname[0]+"/"+name)

def ShowSuccesDialog ():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText("File structure for the new case has been created!")
    #msg.setInformativeText("This is additional information")
    msg.setWindowTitle("New Case")
    msg.setDetailedText("Directory created in OpenFOAM home directory: $FOAM_RUN")
    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    retval = msg.exec_()
    print("value of pressed message box button:", retval)
        
def msgbtn(i):
    print("Button pressed is:",i.text())
