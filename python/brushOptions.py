
class brushOptions():

    def createSLider(self):
 
        self.slider = QSlider()
        self.slider.setOrientation(Qt.Horizontal)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(10)
        self.slider.setMinimum(0.01)
        self.slider.setMaximum(10000.00)
        self.slider.setGeometry(30, 40, 100, 30)
 
        self.slider.valueChanged.connect(self.changedValue)
 
        self.sliderLabel = QLabel("0.1")
        self.sliderLabel.setFont(QtGui.QFont("Sanserif", 10))
        self.sliderLabel.setGeometry(140, 40, 30, 30)

        # sliderLayout = QtWidgets.QHBoxLayout()

        self.gridLayout.addWidget(self.sliderLabel)
        self.gridLayout.addWidget(self.slider)