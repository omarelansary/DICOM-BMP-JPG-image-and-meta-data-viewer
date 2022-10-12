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
import os
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
        #self.allModes= {'1':1, 'L':8, 'P':8, 'RGB':24, 'RGBA':32, 'CMYK':32, 'YCbCr':24, 'I':32, 'F':32}
        self.allModes={"1": 1, "L": 8, "P": 8, "RGB": 24, "RGBA": 32, "CMYK": 32, "YCbCr": 24, "LAB": 24, "HSV": 24, "I": 32, "F": 32}

        #triggers and connections
        self.ui.actionBrowse_Image.triggered.connect(self.Browsefile)

    def Browsefile(self):
        self.path = QFileDialog.getOpenFileName(self, 'Open a file', '') #open browse window
        if self.path != ('', ''):
            self.data = self.path[0]
            print("File path: " + self.data)
 
            if self.data.find(".dcm") !=-1:
                try:
                    self.readdatadicom()
                except:
                    print("This Image is Corrupted, Upload another image")
                    self.ui.ImageDisplay_label.setText("Not Available") 
            else:
                try:
                    self.readmetadata()
                except:
                    print("This Image is Corrupted, Upload another image")
                    self.ui.ImageDisplay_label.setText("Not Available")   
                else:
                    self.displaymetadata()
            #self.displaymetadatajpg()  

    def readmetadata(self):
        self.ui.ImageDisplay_label.setPixmap(QPixmap(self.data))
        self.ui.ImageDisplay_label.setScaledContents(1)
        image = Image.open(self.data)
        self.imgheight=image.height
        self.imgwidth=image.width
        self.imgmode=image.mode
        self.filesizeinbit=image.height*image.width*self.allModes[image.mode]
        #self.filesizeinbit=os.path.getsize(self.data)*8
        #file_size = os.stat(str(self.data))
        #print("Size of file :", file_size.st_size*8, "bits")
        self.bitsperpixel=self.allModes[image.mode]
        

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
        #self.datafordicom=self.data[self.data.rfind('/')+1:]
        #print(self.datafordicom)
        #fpath = get_testdata_file(str(self.data))
        #print(fpath)
        self.ds = dcmread(self.data)
        #print(self.ds)
        imageio.imwrite('outfile.jpg',self.ds.pixel_array)
        self.ui.ImageDisplay_label.setPixmap(QPixmap('outfile.jpg'))
        self.ui.ImageDisplay_label.setScaledContents(1)
        
        try:
            self.imgheight=self.ds.Columns
        except:
            self.ui.IHdisplay_label.setText(str("Columns Not Found")) 
        else:
            self.ui.IHdisplay_label.setText(str(self.imgheight))   

        try:
            self.imgwidth=self.ds.Rows
        except:
            self.ui.IWdisplay_label.setText(str("Rows Not Found"))
        else:
            self.ui.IWdisplay_label.setText(str(self.imgwidth))

        try:
            self.imgmode=self.ds.PhotometricInterpretation
        except:
            self.ui.ICdisplay_label.setText(str("Image Mode Not Found"))  
        else:
            self.ui.ICdisplay_label.setText(str(self.imgmode))

        try:
            self.bitsperpixel=self.ds.BitsStored
        except:
            self.ui.BDdisplay_label.setText(str("Bit depth Not Found"))
        else:
            self.ui.BDdisplay_label.setText(str(self.bitsperpixel))
        

        try:
            self.filesizeinbit=self.imgheight*self.imgwidth*self.ds.BitsStored
        except:
            self.ui.ISdisplay_label.setText(str("File Size Not Found"))
        else:
            self.ui.ISdisplay_label.setText(str(self.filesizeinbit))
        
        
        try:
            self.imgModalitity=self.ds.Modality
        except:
            self.ui.MUdisplay_label.setText(str("Modality Not Found"))
        else:
            self.ui.MUdisplay_label.setText(str(self.imgModalitity))        
        
        try:
            self.patientAge=self.ds.PatientAge
        except:
            self.ui.PAdisplay_label.setText(str("Age Not Found")) 
        else:
            self.ui.PAdisplay_label.setText(str(self.patientAge)) 

        try:
            self.patientName=self.ds.PatientName
        except:
            self.ui.PNdisplay_label.setText(str("Patient Name Not Found"))
        else:
            self.ui.PNdisplay_label.setText(str(self.patientName))                   

        try:
            self.bodypartexamineted=self.ds.BodyPartExamined
        except:
            self.study_description()
        else:
            self.ui.BPdisplay_label.setText(str(self.bodypartexamineted))


    def  study_description(self):
        try:
            self.bodypartexamineted=self.ds.StudyDescription
        except:
            self.ui.BPdisplay_label.setText(str("Bodypart Examineted Not Found"))
        else:
            self.ui.BPdisplay_label.setText(str(self.bodypartexamineted)) 

        #self.bodypartexamineted=self.ds.StudyDescription
        #self.bodypartexamineted=self.ds.BodyPartExamined

    #def displaymetadatadicom(self):
        #self.ui.IWdisplay_label.setText(str(self.imgwidth))    
        #self.ui.IHdisplay_label.setText(str(self.imgheight))
        #self.ui.ICdisplay_label.setText(str(self.imgmode))
        #self.ui.ISdisplay_label.setText(str(self.filesizeinbit))
        #self.ui.BDdisplay_label.setText(str(self.bitsperpixel))
        #self.ui.MUdisplay_label.setText(str(self.imgModalitity))
        #self.ui.PAdisplay_label.setText(str(self.patientAge))
        #self.ui.PNdisplay_label.setText(str(self.patientName))
        #self.ui.BPdisplay_label.setText(str(self.bodypartexamineted))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet())
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())        