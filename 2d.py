####code by Hossein Roosta###
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QMainWindow
from PyQt5 import QtCore, QtWidgets, QtGui
import matplotlib
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import pandas as pd
import seaborn
import sys
matplotlib.use("Qt5Agg")

#define a class can create figure & add subplot, based on Canvas Backend(no created)
class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.getFile()
        #create subplot widget, by the class we defined above
        sc = MplCanvas(self, width=5, height=4, dpi=100)
        #create DF
        #df = pd.read_csv('data3.csv', index_col=0).loc[:, "Sensor1":"Sensor20"].transpose()
        #plot the DF, passing in the matplotlib Canvas axes.
        seaborn.heatmap(ax=sc.axes, data=self.df).invert_yaxis()
        #create toolbar widget, by passing the subplot as a arg
        toolbar = NavigationToolbar(sc, self)
        #create pushbutton widget, open csv file
        pushButton = QtWidgets.QPushButton('Open File')
        pushButton.setObjectName("pushButton")
        #define a layout and add widgets to it
        layout = QtWidgets.QVBoxLayout()
        top_layout = QtWidgets.QHBoxLayout()
        top_layout.addWidget(toolbar)
        top_layout.addWidget(pushButton)
        layout.addLayout(top_layout)
        layout.addWidget(sc)
        # Create a placeholder widget to hold our layout.
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        #signals and slots
        pushButton.clicked.connect(self.getFile)
        self.setCentralWidget(widget)
        self.show()

    def getFile(self):
        """ This function will get the address of the csv file location
            also calls a readData function
        """
        global filename
        filename = QFileDialog.getOpenFileName(filter="csv (*.csv)")[0]
        print("File :", filename)
        self.readData()

    def readData(self):
        """ This function will read the data using pandas and call the update
            function to plot
        """
        import os
        base_name = os.path.basename(filename)
        self.Title = os.path.splitext(base_name)[0]
        print('FILE', self.Title)
        self.df = pd.read_csv(filename, encoding='utf-8', index_col=0).iloc[:, 3:22].transpose()

app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec_()
