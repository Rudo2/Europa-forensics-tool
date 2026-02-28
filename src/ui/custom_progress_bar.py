from PyQt5.QtWidgets import QProgressBar, QLabel, QHBoxLayout, QWidget
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QPainter, QColor, QPen, QBrush, QFont

class DetectiveTortoiseProgressBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        # Create layout
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("%p%")
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #3498db;
                border-radius: 5px;
                text-align: center;
                background-color: #f0f0f0;
                height: 25px;
            }
            QProgressBar::chunk {
                background-color: #2ecc71;
                width: 10px;
                margin: 0.5px;
            }
        """)
        
        # Create detective tortoise label
        self.tortoise_label = QLabel()
        self.tortoise_label.setFixedSize(30, 30)
        self.tortoise_label.setStyleSheet("background-color: transparent;")
        
        # Draw the detective tortoise
        self.draw_detective_tortoise()
        
        # Add widgets to layout
        layout.addWidget(self.tortoise_label)
        layout.addWidget(self.progress_bar)
        
        self.setLayout(layout)
        
        # Connect progress bar value changed signal
        self.progress_bar.valueChanged.connect(self.update_tortoise_position)
        
    def draw_detective_tortoise(self):
        # Create a pixmap for the tortoise
        pixmap = QPixmap(30, 30)
        pixmap.fill(Qt.transparent)
        
        # Create a painter to draw on the pixmap
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw tortoise body (brown oval)
        painter.setPen(QPen(QColor(139, 69, 19), 1))
        painter.setBrush(QBrush(QColor(139, 69, 19)))
        painter.drawEllipse(5, 10, 20, 15)
        
        # Draw tortoise head (brown circle)
        painter.setPen(QPen(QColor(139, 69, 19), 1))
        painter.setBrush(QBrush(QColor(139, 69, 19)))
        painter.drawEllipse(20, 12, 8, 8)
        
        # Draw detective hat (black)
        painter.setPen(QPen(QColor(0, 0, 0), 1))
        painter.setBrush(QBrush(QColor(0, 0, 0)))
        painter.drawEllipse(18, 5, 12, 8)
        
        # Draw magnifying glass (black)
        painter.setPen(QPen(QColor(0, 0, 0), 2))
        painter.drawLine(25, 18, 28, 21)
        painter.drawEllipse(26, 20, 6, 6)
        
        # End painting
        painter.end()
        
        # Set the pixmap to the label
        self.tortoise_label.setPixmap(pixmap)
        
    def update_tortoise_position(self, value):
        # Calculate the position based on the progress value
        progress_width = self.progress_bar.width()
        position = int((value / 100.0) * progress_width) - 15
        
        # Ensure the tortoise stays within the progress bar
        position = max(0, min(position, progress_width - 30))
        
        # Update the tortoise position
        self.tortoise_label.move(position, 0)
        
    def setValue(self, value):
        self.progress_bar.setValue(value)
        
    def value(self):
        return self.progress_bar.value()
        
    def setFormat(self, format_str):
        self.progress_bar.setFormat(format_str) 