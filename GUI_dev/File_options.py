

import subprocess
import os
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile

def NewCase ():
    dlg = QFileDialog()
    dlg.setWindowTitle("Select directory")
    #dlg.setFileMode(QFileDialog.AnyFile)
    global dirname
    dirname = dlg.getSaveFileName()
    #print(dirname[0])
    try:
        subprocess.run(["pyFoamCloneCase.py $FOAM_TUTORIALS/incompressible/simpleFoam/motorBike "+ \
                       dirname[0]], shell=True, check=True)
    except subprocess.CalledProcessError:
        print("Case not created")
        dirname=[]
        return dirname
    else:
        subprocess.call(["rm "+dirname[0]+"/system/cuttingPlane"], shell=True)
        subprocess.call(["rm "+dirname[0]+"/system/streamLines"], shell=True)
        subprocess.call(["rm "+dirname[0]+"/system/forceCoeffs"], shell=True)
        os.chdir(dirname[0]+"/system")
        file=ParsedParameterFile("controlDict")
        del file["functions"]
        file.writeFile()
        subprocess.call(["mkdir "+dirname[0]+"/0"],shell=True)
        NewSuccessDialog(dirname[0])
        return dirname[0]
    
    
def NewSuccessDialog (dirname):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText("File structure for the new case has been created!")
    #msg.setInformativeText("This is additional information")
    msg.setWindowTitle("New Case")
    msg.setDetailedText("Case created in : "+ dirname)
    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    retval = msg.exec_()
    print("value of pressed message box button:", retval)
    
def LoadCase ():
    dlg = QFileDialog()
    dlg.setWindowTitle("Select existing case folder")
    dlg.setFileMode(QFileDialog.Directory)
    if dlg.exec_():
        global dirname
        dirname = dlg.selectedFiles()
    return dirname[0]

def LoadSuccessDialog (dirname):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText("Existing File structure has been loaded with success!")
    msg.setWindowTitle("Load Case")
    msg.setDetailedText("Case loaded from: "+dirname)
    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    retval = msg.exec_()
    print("value of pressed message box button: ", retval)
        
def msgbtn(i):
    print("Button pressed is:",i.text())
