
import sys
import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QMessageBox
from PyFoam.Applications.CloneCase import CloneCase

def NewCase (name):
    os.system("pyFoamCloneCase.py $FOAM_TUTORIALS/incompressible/simpleFoam/motorBike $FOAM_RUN/" + name)

def ShowDialog ():
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
