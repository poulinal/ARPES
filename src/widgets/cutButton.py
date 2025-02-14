### 2024 Alex Poulin
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtCore import QSize

###create a pyqt widget button that has a diagonal line across the button.
###it also has a hover event that changes the color of the button
###when toggled the diagonal line turns yellow but when toggled off, the diagonal line turns white
class cutButton(QPushButton):
    def __init__(self, parent=None):
        super(cutButton, self).__init__(parent)
        self.setFixedSize(100, 25)
        self.setStyleSheet("color : rgba(0, 0, 0, 0); background-color : rgba(0, 0, 0, 0); border : 0px solid rgba(0, 0, 0, 0);")
        self.toggled.connect(self._on_toggled)
        self.hovered = False

    def _on_toggled(self, checked):
        if checked:
            self.setStyleSheet("color : rgba(0, 0, 0, 0); background-color : rgba(0, 0, 0, 0); border : 0px solid rgba(0, 0, 0, 0);")
        else:
            self.setStyleSheet("color : rgba(0, 0, 0, 0); background-color : rgba(0, 0, 0, 0); border : 0px solid rgba(0, 0, 0, 0);")

    def enterEvent(self, event):
        self.hovered = True
        self.update()

    def leaveEvent(self, event):
        self.hovered = False
        self.update()

    def paintEvent(self, event):
        super(cutButton, self).paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(QPen(QColor(255, 255, 255), 2))
        painter.drawLine(0, 0, self.width(), self.height())

        if self.hovered:
            painter.setPen(QPen(QColor(255, 255, 0), 2))
            painter.drawLine(0, 0, self.width(), self.height())
        painter.end()
        
    def sizeHint(self):
        return QSize(100, 25)
    
    def minimumSizeHint(self):
        
        return QSize(100, 25)
    
    def setFixedSize(self, width, height):
        self.width = width
        self.height = height
        self.update()
        
    def setStyleSheet(self, style):
        self.style = style
        self.update()
        
    def setChecked(self, checked):
        self.checked = checked
        self.update()
        
    def update(self):
        self.repaint()
        
    def repaint(self):
        self.paintEvent(None)

    def setAttribute(self, attribute):
        self.attribute = attribute
        self.update()