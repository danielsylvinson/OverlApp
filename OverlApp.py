from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, pyqtSlot
from mainwindow import Ui_MainWindow
import sys
from model import Model
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QIcon, QPixmap
import random
import os

filein = ""
x = 0
class MainWindowUIClass( Ui_MainWindow ):
    def __init__( self ):
        super().__init__()
        self.model = Model()



    def setupUi( self, MW ):
        super().setupUi( MW )


    def refreshAll( self ):
        try:
            self.lineEdit.setText( self.model.getFileName() )
        except:
            self.lineEdit.setText( "" )



    def calculateSlot( self ):
        filein = self.lineEdit.text()
        x = filein.count(',')
        v = self.doubleSpinBox.value()
        self.progressBar.setValue(15)
        printed2 = self.model.calculate(filein,v,x)
        self.progressBar.setValue(90)
        for h in printed2:
            self.textBrowser.append(h)
        self.progressBar.setValue(100)







    # slot
    def browseSlot( self ):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileNames, _ = QtWidgets.QFileDialog.getOpenFileNames(
                        None,
                        "Browse",
                        "",
                        "All Files (*);;molden Files (*.molden)",
                        options=options)

        print(fileNames)
        print(len(fileNames))
        self.progressBar.setValue(0)
        self.model.setFileName( fileNames )
        self.refreshAll()

def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    MainWindow = QtWidgets.QMainWindow()
    ui = MainWindowUIClass()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

main()
