import sys
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QApplication, QCheckBox, QGridLayout, QGroupBox,
                             QMenu, QPushButton, QRadioButton, QVBoxLayout, QWidget, QSlider)
import serial


class Ui_Dialog(object):
    def setupUi(self, Dialog):

        grid = QGridLayout()

        self.ser = ""

        self.centralwidget = QtWidgets.QWidget(Dialog)
        self.centralwidget.setObjectName("centralwidget")

        self.slider = QtWidgets.QSlider()
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setTickInterval(1)
        self.slider.setRange(-500, 500)
        self.slider.setValue(0)

        self.slider2 = QtWidgets.QSlider()
        self.slider2.setOrientation(QtCore.Qt.Horizontal)
        self.slider2.setTickInterval(1)
        self.slider2.setRange(-500, 500)
        self.slider2.setValue(0)

        self.slider2.valueChanged.connect(self.getSliderValue)
        self.slider.valueChanged.connect(self.getVerticalSliderValue)

        self.modeButton = QtWidgets.QPushButton()
        self.modeButton.setText("Send")


        self.serialButton = QtWidgets.QPushButton()
        self.serialButton.setText("Connect Serial")
        self.serialButton.setStyleSheet("""
            QPushButton {
                border: #007bff 2px solid;
                background-color: white;
                color: #007bff;
                font-family: Arial;
                border-radius: 5px;
                font-size: 15px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: gray;
            }
        """)

        # Connecting the button click signal to the toggleButton method
        self.modeButton.clicked.connect(self.sendSteps)
        self.serialButton.clicked.connect(self.connectSerial)

        self.modeButton.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                font-family: Arial;
                border-radius: 5px;
                font-size: 15px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)

        self.titleLabel = QtWidgets.QLabel()
        self.titleLabel.setText("Manual Control")

        self.hStepsLabel = QtWidgets.QLabel()
        self.hStepsLabel.setText("0")

        self.vStepsLabel = QtWidgets.QLabel()
        self.vStepsLabel.setText("0")

        self.serialLabel = QtWidgets.QLabel("Not Connected")
        self.serialLabel.setStyleSheet("""
            QLabel {
                
                color: #007bff;
                font-family: Arial;
                border-radius: 5px;
                font-size: 15px;
                padding: 10px;
                text-align: center;
                
            }
            
        """)

        self.slider2Label = QtWidgets.QLabel()
        self.slider2Label.setText("Horizontal")
        self.sliderLabel = QtWidgets.QLabel()
        self.sliderLabel.setText("Vertical")

        Dialog.setCentralWidget(self.centralwidget)
        self.centralwidget.setLayout(grid)

        Dialog.setWindowTitle("Camera Tracker Controller")
        Dialog.resize(400, 300)
        Dialog.setObjectName("Dialog")

        # Adding widgets to the layout
        grid.addWidget(self.serialButton, 0, 1)
        grid.addWidget(self.modeButton, 0, 0)
        grid.addWidget(self.serialLabel,0,2)
        grid.addWidget(self.slider, 1, 1)
        grid.addWidget(self.sliderLabel, 1, 0)
        grid.addWidget(self.vStepsLabel, 1, 2)
        grid.addWidget(self.slider2, 3, 1)
        grid.addWidget(self.slider2Label, 3, 0)
        grid.addWidget(self.hStepsLabel, 3, 2)
    
    
    def getSliderValue(self, value):
        self.hStepsLabel.setText(str(value))
        global horizontal_steps
        horizontal_steps = value
    
    def getVerticalSliderValue(self, value):
        self.vStepsLabel.setText(str(value))
        global vertical_steps
        vertical_steps = value


    def sendSteps(self):
        
        self.sendSerialData(horizontal_steps)
        self.sendSerialData(vertical_steps)
        
    
    def connectSerial(self):
        try:
            global ser
            ser = serial.Serial('COM4', 9600)
            self.serialLabel.setText("Connected")
            self.serialButton.setEnabled(False)
            self.serialLabel.setStyleSheet("""
            QLabel {
                
                color: green;
                font-family: Arial;
                border-radius: 5px;
                font-size: 15px;
                padding: 10px;
                text-align: center;
                
            }
            
        """)
            return(ser)
        except:
            self.serialLabel.setText("Error Connecting")
            return
        

    def sendSerialData(self, data):
        
        ser.write(f"{data}\n".encode())
        print("Sent "+str(data))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_Dialog()
    ui.setupUi(MainWindow)
    
    MainWindow.show()  # Fixed typo here
    sys.exit(app.exec_())
