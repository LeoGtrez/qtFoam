#!/usr/bin/python

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic

qtCreatorFile = "Tax_calc.ui" # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QMainWindow):
    def __init__(self):
        super(MyApp,self).__init__()
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.calc_tax_button.clicked.connect(self.CalculateTax)
       
    
    def CalculateTax(self):
        price = int(self.ui.price_box.toPlainText())
        tax = (self.ui.tax_rate.value())
        total_price = price  + ((tax / 100.0) * price)
        total_price_string = "Tax is: " + str(tax)+\
   		" The total price with tax is: " + str(total_price)
        self.ui.results_window.setText(total_price_string)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
