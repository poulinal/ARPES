### 2025 Alexander Poulin
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy, QHBoxLayout
from PyQt6.QtWidgets import QLineEdit, QLabel
from PyQt6.QtGui import QIntValidator
from PyQt6.QtCore import pyqtSignal

class lineCoordsWidget(QWidget):
    lineCoordsEdited = pyqtSignal(float, float, float, float)
    
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        row1Layout = QHBoxLayout()
        layout.addLayout(row1Layout)
        self.setLayout(layout)
        self.setup_widget()
        
        #setup lineCoords
        self.textLineX = QLineEdit()
        self.textLineY = QLineEdit()
        self.textLineFinalX = QLineEdit()
        self.textLineFinalY = QLineEdit()
        coordWidgetList = [self.textLineX, self.textLineY, self.textLineFinalX, self.textLineFinalY]
        self.textLineX.textEdited.connect(self.text_edited)
        self.textLineY.textEdited.connect(self.text_edited)
        
        
        #its properties
        onlyInt = QIntValidator()
        onlyInt.setRange(0, 9)
        for w in coordWidgetList:
            #w.setFixedWidth(15)
            w.setValidator(onlyInt)
            w.setMaxLength(4)
            if w == self.textLineX or w == self.textLineY:
                w.setPlaceholderText("Enter Starting X")
            else:
                w.setPlaceholderText("Enter Ending X")
        parenLabel = QLabel("(")
        paren2Label = QLabel(")")
        commaLabel = QLabel(",")
        parenLabel2 = QLabel("(")
        paren2Label2 = QLabel(")")
        commaLabel2 = QLabel(",")
        #add it to layout
        controlWidgetList = [parenLabel, self.textLineX, commaLabel, self.textLineY, paren2Label]
        controlWidgetList2 = [parenLabel2, self.textLineFinalX, commaLabel2, self.textLineFinalY, paren2Label2]
        for w in controlWidgetList:
            row1Layout.addWidget(w)
        for w in controlWidgetList2:
            row1Layout.addWidget(w)
        
    def setup_widget(self):
        pass
    
    
        #on text change, update the line
    def text_edited(self):
        if (self.textLineFinalX.text() is not None and self.textLineFinalY.text() is not None and self.textLineX.text() is not None and self.textLineY.text() is not None):
            self.lineCoordsEdited.emit(self.textLineX.text(), self.textLineY.text(), self.textLineFinalX.text(), self.textLineFinalY.text())
            
    def setTexts(self, startX = None, startY = None, lastX = None, lastY = None):
        if startX is not None:
            self.textLineX.setText(str(startX))
        if startY is not None:
            self.textLineY.setText(str(startY))
        if lastX is not None:
            self.textLineFinalX.setText(str(lastX))
        if lastY is not None:
            self.textLineFinalY.setText(str(lastY))
        
    def setLastTexts(self, lastX = "", lastY = ""):
        self.textLineFinalX.setText(str(lastX))
        self.textLineFinalY.setText(str(lastY))
            
    def getPos(self):
        """Gets the current positions based on the line coords widget's data

        Returns:
            tuple: startx: str, starty: str, lastx: str, lasty: str
        """
        return self.textLineX.text(), self.textLineY.text(), self.textLineFinalX.text(), self.textLineFinalY.text()