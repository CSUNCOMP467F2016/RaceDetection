from PyQt5 import QtGui, QtCore, QtWidgets # Import the PyQt5 module we'll need
import sys # We need sys so that we can pass argv to QApplication
import mainwindow # This file holds our MainWindow and all design related things
from Comp467Control import prototype
from PyQt5.QtCore import pyqtSignal, QMimeData, Qt
from PyQt5.QtGui import QPalette, QPixmap
from PyQt5.QtWidgets import (QAbstractItemView, QApplication, QDialogButtonBox,
        QFrame, QLabel, QPushButton, QTableWidget, QTableWidgetItem,
        QVBoxLayout, QWidget, QFileDialog, QMessageBox)


class RaceDetection(QtWidgets.QMainWindow, mainwindow.Ui_MainWindow):
    #initilization
    def __init__(self):
        self.filepath = ""

        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.dropBox = DropBox()
        self.verticalLayout.insertWidget(1, self.dropBox, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        #Define all connections to functions below:
        self.clearButton.clicked.connect(self.dropBox.clear)
        self.clearButton.clicked.connect(self.clearFilepath)
        self.dropBox.changed.connect(self.updateFilePath)
        self.analyzeButton.clicked.connect(self.run_race_detection)
        self.importImageButton.clicked.connect(self.selectFilepath)
    #run race detection tool
    def run_race_detection(self):
        detect = prototype.FaceDetect()
        if self.filepath is "":
            self.statusMessage("Please drop or import an image")
        else:
            race = detect.race_detect(self.filepath)
            self.statusMessage(race)
    #update filepath when new image is loaded
    def updateFilePath(self, mimeData=None):
        if mimeData is None:
            return
        if mimeData.hasUrls():
            self.filepath = str(mimeData.urls()[0].path())
    #remove filepath after clearing image
    def clearFilepath(self):
        self.filepath = ""
    #manually select filepath
    def selectFilepath(self):
        fname = QFileDialog.getOpenFileName(self, 'Select image', '/home')
        if fname[0]:
            if self.dropBox.setImage(fname[0]):
                self.filepath = str(fname[0])
    #stausMessage Pop-up to display info
    def statusMessage(self, text):
        choice = QMessageBox.information(self, 'Status Message',
                                            text,
                                            QMessageBox.Ok)

class DropBox(QtWidgets.QLabel):
    #marker for signal change
    changed = pyqtSignal(QMimeData)
    #initialize class
    def __init__(self, parent = None):
        super(DropBox, self).__init__(parent)

        self.setMinimumSize(200, 400)
        self.setFrameStyle(QFrame.Sunken | QFrame.StyledPanel)
        self.setAlignment(Qt.AlignCenter)
        self.setAcceptDrops(True)
        self.setScaledContents(True)
        self.setAutoFillBackground(True)
        self.clear()
    #defines drag actions
    def dragEnterEvent(self, event):
        self.setText("<drop image here and press analyze to see result>")
        self.setBackgroundRole(QPalette.Highlight)
        event.acceptProposedAction()
    #defines move event
    def dragMoveEvent(self, event):
        event.acceptProposedAction()

    #Method defines dropEvent actions. If image is dropped, calls setImage and triggers emit.
    def dropEvent(self, event):
        mimeData = event.mimeData()
        if mimeData.hasImage():
            self.setPixmap(QPixmap(mimeData.imageData()))

        elif mimeData.hasUrls():
            if self.setImage(mimeData.urls()[0].path()):
                self.changed.emit(event.mimeData())
        else:
            self.setText("Cannot display data")

        self.setBackgroundRole(QPalette.Dark)
        event.acceptProposedAction()
    #define actions for leaving event
    def dragLeaveEvent(self, event):
        self.clear()
        event.accept()
    #clear method when image wants to be removed
    def clear(self):
        self.setText("<drop image here and press analyze to see result>")
        self.setBackgroundRole(QPalette.Dark)
        self.changed.emit(None)
    #set image onto label
    def setImage(self, imageFile):
        imageSet = False
        for image in [".jpeg", ".png", ".jpg"]:
             if image in str(imageFile):
                 self.setPixmap(QPixmap(imageFile))
                 imageSet = True
                 break
             self.setText("Not an accepted image format")
        return imageSet


def main():
    app = QtWidgets.QApplication(sys.argv)  # A new instance of QApplication
    form = RaceDetection()                
    form.show()                         # Show the form
    app.exec_()                         # and execute the app


if __name__ == '__main__':              # if we're running file directly and not importing it
    main()  
