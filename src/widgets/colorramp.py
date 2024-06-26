import sys
from PyQt6.QtCore import Qt, QRectF, QPointF, pyqtSignal
from PyQt6.QtGui import QPainter, QColor, QLinearGradient, QMouseEvent
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel

class ColorRampWidget(QWidget):
    
    valueChanged = pyqtSignal(float, float)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(50)
        self.black_position = 0.0
        self.white_position = 1.0
        self.slider_radius = 6
        self.selected_slider = None

    def paintEvent(self, event):
        painter = QPainter(self)
        gradient = QLinearGradient(0, 0, self.width(), 0)
        
        gradient.setColorAt(self.black_position, QColor(0, 0, 0))
        gradient.setColorAt(self.white_position, QColor(255, 255, 255))

        painter.fillRect(self.rect(), gradient)

        # Draw sliders
        self.draw_slider(painter, self.black_position, QColor(0, 0, 0), QColor(255, 255, 255))
        self.draw_slider(painter, self.white_position, QColor(255, 255, 255), QColor(0, 0, 0))

    def draw_slider(self, painter, position, color, invtColor):
        x = position * self.width()
        y = self.height() / 2
        painter.setBrush(color)
        #painter.setPen(Qt.GlobalColor.black)
        painter.setPen(invtColor)
        painter.drawEllipse(QPointF(x, y), self.slider_radius, self.slider_radius)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            pos = event.position().x() / self.width()
            if abs(pos - self.black_position) < abs(pos - self.white_position):
                self.selected_slider = 'black'
            else:
                self.selected_slider = 'white'
            self.update_slider_position(event.position().x())

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.selected_slider:
            self.update_slider_position(event.position().x())

    def mouseReleaseEvent(self, event: QMouseEvent):
        self.selected_slider = None

    def update_slider_position(self, x):
        position = x / self.width()
        position = max(0.0, min(position, 1.0))
        
        if self.selected_slider == 'black':
            self.black_position = min(position, self.white_position - 0.01)
        elif self.selected_slider == 'white':
            self.white_position = max(position, self.black_position + 0.01)
            
        self.valueChanged.emit(self.black_position, self.white_position)
        
        self.update()
        
    def get_slider_position(self):
        """get the slider position

        Returns:
            tuple: black position, white position
        """
        return self.black_position, self.white_position

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Black and White Color Ramp Widget')
        
        self.color_ramp = ColorRampWidget()
        self.label = QLabel('Drag the sliders to change the color ramp range')

        layout = QVBoxLayout()
        layout.addWidget(self.color_ramp)
        layout.addWidget(self.label)

        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
