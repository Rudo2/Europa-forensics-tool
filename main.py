import warnings
import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QPalette, QColor, QPixmap
from src.ui.device_manager import DeviceManagerWidget
from src.ui.data_extractor import DataExtractorWidget
from src.ui.report_generator import ReportGeneratorWidget
from src.ui.splash_screen import MobileForensicSplashScreen

# Suppress the deprecation warning
warnings.filterwarnings("ignore", category=DeprecationWarning)

class MobileForensicTool(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EUROPA FORENSICS TOOL")
        self.setGeometry(100, 100, 1200, 800)
        
        # Set the application style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e3a8a; /* Dark blue background */
            }
            QTabWidget::pane {
                border: 1px solid #3b82f6; /* Blue border */
                background-color: #f0f9ff; /* Light blue background */
            }
            QTabBar::tab {
                background-color: #3b82f6; /* Blue tabs */
                color: white;
                padding: 8px 16px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: #1e40af; /* Darker blue for selected tab */
            }
            QPushButton {
                background-color: #3b82f6; /* Blue buttons */
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #2563eb; /* Darker blue on hover */
            }
            QTableWidget {
                border: 1px solid #3b82f6; /* Blue border */
                gridline-color: #bfdbfe; /* Light blue grid lines */
            }
            QHeaderView::section {
                background-color: #3b82f6; /* Blue header */
                color: white;
                padding: 4px;
                border: 1px solid #1e40af; /* Darker blue border */
            }
        """)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(0)  # Remove spacing between widgets
        
        # Create header widget with dark blue background
        header_widget = QWidget()
        header_widget.setStyleSheet("background-color: #1e3a8a;")  # Dark blue background
        header_widget.setFixedHeight(180)  # Adjusted height for header
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(20, 10, 20, 10)
        
        # Create a container for mascot and titles to center them together
        center_container = QWidget()
        center_layout = QHBoxLayout(center_container)
        center_layout.setSpacing(20)  # Space between mascot and titles
        
        # Add mascot image
        mascot_label = QLabel()
        try:
            # Try multiple paths for the mascot image
            possible_paths = [
                os.path.join(os.path.dirname(os.path.abspath(__file__)), "src", "ui", "assets", "mascot.png"),
                os.path.join(os.path.dirname(os.path.abspath(__file__)), "src", "ui", "assets", "turtle_detective.png"),
                os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "mascot.png"),
                os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "turtle_detective.png")
            ]
            
            for mascot_path in possible_paths:
                print(f"Trying to load mascot from: {mascot_path}")
                if os.path.exists(mascot_path):
                    pixmap = QPixmap(mascot_path)
                    if not pixmap.isNull():
                        scaled_pixmap = pixmap.scaled(175, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                        mascot_label.setPixmap(scaled_pixmap)
                        mascot_label.setAlignment(Qt.AlignCenter)
                        print(f"Successfully loaded mascot from: {mascot_path}")
                        break
                    else:
                        print(f"Failed to load image from {mascot_path}: QPixmap is null")
                else:
                    print(f"Image not found at: {mascot_path}")
        except Exception as e:
            print(f"Error loading mascot image: {str(e)}")
        
        # Create text container for titles
        text_container = QWidget()
        text_layout = QVBoxLayout(text_container)
        text_layout.setSpacing(5)  # Reduced spacing between labels
        text_layout.setAlignment(Qt.AlignCenter)
        
        # EUROPA title
        europa_label = QLabel("EUROPA")
        europa_label.setAlignment(Qt.AlignCenter)
        europa_font = QFont("Arial", 44, QFont.Bold)
        europa_label.setFont(europa_font)
        europa_label.setStyleSheet("color: #f97316; font-weight: bold;")
        text_layout.addWidget(europa_label)
        
        # FORENSICS TOOL subtitle
        tool_label = QLabel("FORENSICS TOOL")
        tool_label.setAlignment(Qt.AlignCenter)
        tool_font = QFont("Arial", 36, QFont.Bold)
        tool_label.setFont(tool_font)
        tool_label.setStyleSheet("color: #f97316; font-weight: bold;")
        text_layout.addWidget(tool_label)
        
        # Add mascot and text to center container
        center_layout.addWidget(mascot_label)
        center_layout.addWidget(text_container)
        
        # Add stretches to center the container
        header_layout.addStretch(1)
        header_layout.addWidget(center_container)
        header_layout.addStretch(1)
        
        # Add header widget to main layout
        layout.addWidget(header_widget)
        
        # Add some spacing between header and tabs
        layout.addSpacing(10)
        
        # Create tab widget
        tabs = QTabWidget()
        layout.addWidget(tabs)
        
        # Add tabs
        self.device_manager = DeviceManagerWidget()
        self.data_extractor = DataExtractorWidget()
        self.report_generator = ReportGeneratorWidget()
        
        tabs.addTab(self.device_manager, "Device Manager")
        tabs.addTab(self.data_extractor, "Data Extractor")
        tabs.addTab(self.report_generator, "Report Generator")
        
        # Connect signals
        self.device_manager.device_connected.connect(self.data_extractor.on_device_connected)
        self.device_manager.device_disconnected.connect(self.data_extractor.on_device_disconnected)
        self.data_extractor.data_extracted.connect(self.report_generator.on_data_available)

def main():
    app = QApplication(sys.argv)
    
    # Create and show splash screen
    splash = MobileForensicSplashScreen()
    splash.start()
    
    # Create main window but don't show it yet
    window = MobileForensicTool()
    
    # Process events to ensure splash screen is shown
    app.processEvents()
    
    # Wait for 6 seconds before closing splash screen
    QTimer.singleShot(6000, lambda: splash.finish(window))
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 