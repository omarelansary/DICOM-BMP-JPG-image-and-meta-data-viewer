from importlib.metadata import metadata
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow,QFileDialog
from MyTask1Ui import Ui_MainWindow
import qdarkstyle
from PyQt5.QtGui import QPixmap
from PIL import Image
from PIL.ExifTags import TAGS
import os.path
#import scipy.misc
import imageio
from pydicom import dcmread
from pydicom.data import get_testdata_file


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #Variables
        self.data=[]
        #triggers and connections
        self.ui.actionBrowse_Image.triggered.connect(self.Browsefile)

    def Browsefile(self):
        self.path = QFileDialog.getOpenFileName(self, 'Open a file', '') #open browse window
        if self.path != ('', ''):
            self.data = self.path[0]
            print("File path: " + self.data)
            if self.data.find(".dcm") !=-1:
                self.readdatadicom()
                self.displaymetadatadicom()
            else:
                self.ui.ImageDisplay_label.setPixmap(QPixmap(self.data))
                self.ui.ImageDisplay_label.setScaledContents(1)
                self.readmetadata()
                self.displaymetadata()
            #self.displaymetadatajpg()  

    def readmetadata(self):
        image = Image.open(self.data)
        self.imgheight=image.height
        self.imgwidth=image.width
        self.imgmode=image.mode
        self.filesizeinbit=os.path.getsize(self.data)*8
        self.bitsperpixel=round(self.filesizeinbit/(self.imgwidth*self.imgheight),3)
        

    def displaymetadata(self):
        self.ui.IWdisplay_label.setText(str(self.imgwidth))    
        self.ui.IHdisplay_label.setText(str(self.imgheight))
        self.ui.ICdisplay_label.setText(str(self.imgmode))
        self.ui.ISdisplay_label.setText(str(self.filesizeinbit))
        self.ui.BDdisplay_label.setText(str(self.bitsperpixel))
        self.ui.MUdisplay_label.setText("Not Available")
        self.ui.PNdisplay_label.setText("Not Available")
        self.ui.PAdisplay_label.setText("Not Available")
        self.ui.BPdisplay_label.setText("Not Available")

    def readdatadicom(self):
        self.datafordicom=self.data[self.data.rfind('/')+1:]
        fpath = get_testdata_file(self.datafordicom)
        self.ds = dcmread(fpath)
        print(self.ds)
        imageio.imwrite('outfile.jpg',self.ds.pixel_array)
        self.ui.ImageDisplay_label.setPixmap(QPixmap('outfile.jpg'))
        self.ui.ImageDisplay_label.setScaledContents(1)
        self.imgheight=self.ds.Columns
        self.imgwidth=self.ds.Rows
        self.imgmode=self.ds.PhotometricInterpretation
        self.filesizeinbit=self.ds.BitsStored
        self.bitsperpixel=round(self.filesizeinbit/(self.imgwidth*self.imgheight),3)
        self.patientAge=self.ds.PatientAge
        self.patientName=self.ds.PatientName
        self.imgModalitity=self.ds.Modality
        self.bodypartexamineted=self.ds.StudyDescription

    def displaymetadatadicom(self):
        self.ui.IWdisplay_label.setText(str(self.imgwidth))    
        self.ui.IHdisplay_label.setText(str(self.imgheight))
        self.ui.ICdisplay_label.setText(str(self.imgmode))
        self.ui.ISdisplay_label.setText(str(self.filesizeinbit))
        self.ui.BDdisplay_label.setText(str(self.bitsperpixel))
        self.ui.MUdisplay_label.setText(str(self.imgModalitity))
        self.ui.PAdisplay_label.setText(str(self.patientAge))
        self.ui.PNdisplay_label.setText(str(self.patientName))
        self.ui.BPdisplay_label.setText(str(self.bodypartexamineted))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet())
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())        