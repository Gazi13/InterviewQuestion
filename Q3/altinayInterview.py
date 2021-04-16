# 16/04/2021
# Ahmet Gazi Cifci
# Altinay Robotik - Mulakat
#
# pip install PyQt5
# pip install opencv-python==4.3.0

import cv2
import os, sys
import numpy as np
from PIL.ImageQt import ImageQt
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QTransform, QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QWidget, QTextEdit, QPushButton, QLabel,QMessageBox

class Ui_MainWindow(QWidget):
    
    # Parameters & Initialization
    filePath = ""
    fileList = ""
    window_height = 900
    window_width = 1200
    frame_w,frame_h = 900, 1100 
    frame_x,frame_y = 200, 20

    # Her resim için ayrı bir Pixmap kullanmak yerine
    # 10 resmi birleştirip gostermek için bir frame kullanıyoruz
    frame = np.zeros((int(frame_h),int(frame_w),3),dtype=np.uint8)
    # Resimler uzerinde gezerken kullanmak için index
    index = 0;

    # Arayuz ayarları
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(self.window_width, self.window_height)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.pixmap = QPixmap("")
        self.photo = QtWidgets.QLabel(self.centralwidget)
        self.photo.setGeometry(QtCore.QRect(self.frame_x, self.frame_y, self.frame_w, self.frame_h))
        self.photo.setText("")
        self.photo.setPixmap(self.pixmap)
        self.photo.setScaledContents(True)
        self.photo.setObjectName("photo")

        # Buttons 
        self.start_b = QtWidgets.QPushButton(self.centralwidget)
        self.start_b.setGeometry(QtCore.QRect(50, 50, 120, 40))
        self.start_b.setObjectName("start")

        self.examine_b = QtWidgets.QPushButton(self.centralwidget)
        self.examine_b.setGeometry(QtCore.QRect(50, 150, 120, 40))
        self.examine_b.setObjectName("examine")

        self.record_b = QtWidgets.QPushButton(self.centralwidget)
        self.record_b.setGeometry(QtCore.QRect(50, 250, 120, 40))
        self.record_b.setObjectName("record")

        self.next_b = QtWidgets.QPushButton(self.centralwidget)
        self.next_b.setGeometry(QtCore.QRect(50, 350, 120, 40))
        self.next_b.setObjectName("next_b")


        # Menubar        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")        
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuFormat = QtWidgets.QMenu(self.menubar)
        self.menuFormat.setObjectName("menuFormat")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")

        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # Actions
        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.actionInvert = QtWidgets.QAction(MainWindow)
        self.actionInvert.setObjectName("actionInvert")
        self.actionMirror = QtWidgets.QAction(MainWindow)
        self.actionMirror.setObjectName("actionMirror")
        self.actionHelp = QtWidgets.QAction(MainWindow)
        self.actionHelp.setObjectName("actionHelp")
        self.actionVersion = QtWidgets.QAction(MainWindow)
        self.actionVersion.setObjectName("actionVersion")

        self.menuFile.addAction(self.actionNew)
        self.menuFormat.addAction(self.actionInvert)
        self.menuFormat.addAction(self.actionMirror)
        self.menuHelp.addAction(self.actionHelp)
        self.menuHelp.addAction(self.actionVersion)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuFormat.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Connect actions to functions
        self.actionNew.triggered.connect(self.openFolder)
        self.actionInvert.triggered.connect(self.invert)
        self.actionMirror.triggered.connect(self.mirror)
        self.actionHelp.triggered.connect(self.help)
        self.actionVersion.triggered.connect(self.version)

        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.examine_b.clicked.connect(self.examine)
        self.start_b.clicked.connect(self.start)
        self.record_b.clicked.connect(self.record)
        self.next_b.clicked.connect(self.next)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        
        self.start_b.setText(_translate("MainWindow", "Start"))
        self.examine_b.setText(_translate("MainWindow", "Examine"))
        self.record_b.setText(_translate("MainWindow", "Record"))
        self.next_b.setText(_translate("MainWindow", "Next"))

        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuFormat.setTitle(_translate("MainWindow", "Format"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        
        self.actionNew.setText(_translate("MainWindow", "New"))
        self.actionNew.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.actionInvert.setText(_translate("MainWindow", "Invert"))
        self.actionInvert.setShortcut(_translate("MainWindow", "Ctrl+I"))
        self.actionMirror.setText(_translate("MainWindow", "Mirros"))
        self.actionMirror.setShortcut(_translate("MainWindow", "Ctrl+M"))
        self.actionHelp.setText(_translate("MainWindow", "Help"))
        self.actionHelp.setShortcut(_translate("MainWindow", "Ctrl+H"))
        self.actionVersion.setText(_translate("MainWindow", "Version"))
        self.actionVersion.setShortcut(_translate("MainWindow", "Ctrl+V"))

##--------------------------------------------------------------------------------
## Functions
##--------------------------------------------------------------------------------

    def start(self):
        """
        Resim icindeki kose noktalarını bulur ve 1sn aralıklar gosterir
        :param --:
        :return: --:
        """
        for image_name in self.fileList:
            filename = self.filePath+"/"+image_name
            image = cv2.imread(filename)
            gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
            gray = np.float32(gray)
            
            """
            dst = cv2.cornerHarris(gray,2,3,0.05)
            dst = cv2.dilate(dst,None)
            image[dst>0.01*dst.max()]=[0,0,255]
            """
            kernel = np.ones((3,3),np.uint8)
            opening = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel)
            # Shi-Tomasi Corner Detector
            corners = cv2.goodFeaturesToTrack(opening,5,0.05,20)
            corners = np.int0(corners)

            for i in corners:
                x,y = i.ravel()
                cv2.circle(image,(x,y),3,(0,0,255),-1)
            
            # Resmi guncelle ve 1sn bekle
            image = QtGui.QImage(image.data, image.shape[1], image.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
            self.pixmap = QtGui.QPixmap.fromImage(image)
            self.photo.setPixmap(self.pixmap)
            cv2.waitKey(1000)

    def cropInfo(self, file_path, j):
        """
        Resim icindeki bilgi iceren kısımları bulur ve keser.
        :param file_path: dosya yolu
        :param j        : 10 resimden hangisi oldugunu gosteren index
        :return: --:
        """

        image = cv2.imread(file_path)
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        mask = gray>80
        cropted_image = image[np.ix_(mask.any(1),mask.any(0))]
        h, w, c = cropted_image.shape

        profil_start = int(((self.frame_h/10)*j)-h)-10
        profil_end = int((self.frame_h/10)*j)-10

        # Add to frame
        self.frame[profil_start:profil_end,100:100+w,:3] = cropted_image
        self.frame[profil_end+5,:,:3] = [255,0,255]



    def examine(self):
        """
        Resim icindeki bilgi iceren kısımları kesip 10'ar gruplar halinde gosterir.
        :param --:  
        :return: --:
        """
        if not self.fileList:
            self.index -= 10
            return 0;
        i = self.index
        for j in range(1,11):
            if ((i+j-1)==76): self.index,i = 0,0
                
            file_name = self.filePath+"/"+self.fileList[(i+j-1)]
            self.cropInfo(file_name,j)

        # Update Images
        profile_img = QtGui.QImage(self.frame.data, self.frame.shape[1], self.frame.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
        self.pixmap = QtGui.QPixmap.fromImage(profile_img)
        self.photo.setPixmap(self.pixmap)
        self.rotate()


    def record(self):
        """
        Resmi seçilen konuma kaydeder.
        :param --:  
        :return: --:
        """
        name, _ = QFileDialog.getSaveFileName(self, 'Save File', r"recorded_img.png", "Image files (*.jpg *.jpeg *.png)")
        image = self.pixmap.toImage()
        image.save(name)


    def next(self):
        """
        Bir sonraki 10'lu resme gecis yapar
        :param --:  
        :return: --:
        """
        self.index += 10
        self.examine()

    def openFolder(self):
        """
        Secilen dosyadaki resimleri okur. Resim path'lerini saklar
        :param --:  
        :return: --:
        """
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open Image File', r"<Default dir>", "Image files (*.jpg *.jpeg *.png)")
        
        if (file_name):

            # Update Images
            self.pixmap = QPixmap(file_name)
            self.photo.setPixmap(self.pixmap)
            # Get folder information
            head, tail = os.path.split(file_name)
            self.filePath = head
            self.fileList = sorted(os.listdir(self.filePath))
    
    def invert(self):
        image = self.pixmap.toImage()
        image.invertPixels()
        self.pixmap = QtGui.QPixmap.fromImage(image)
        self.photo.setPixmap(self.pixmap)

    def mirror(self):
        self.photo.setPixmap(self.pixmap.transformed(QTransform().scale(1, -1)))

    def rotate(self):
        transform = QtGui.QTransform().rotate(90)
        self.pixmap = self.pixmap.transformed(transform, QtCore.Qt.SmoothTransformation)
        self.photo.setPixmap(self.pixmap)

    def help(self):
        msg = QMessageBox()
        msg.setText("This is Help Message")
        msg.setWindowTitle("Help")
        msg.setDetailedText("The details are as follows:")
        retval = msg.exec_()
    
    def version(self):
        msg = QMessageBox()
        msg.setText("Version INFO : 15/04/2021")
        msg.setWindowTitle("Version")
        msg.setDetailedText("Version INFO : 15/04/2021 Altinay Interview Question ")
        retval = msg.exec_()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
