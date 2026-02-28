import sys
import time
import os
from PyQt5.QtWidgets import QApplication, QDialog, QProgressBar, QVBoxLayout, QLabel, QWidget, QHBoxLayout
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QFont, QColor, QPalette

class MobileForensicSplashScreen(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.init_ui()
        
    def init_ui(self):
        # Set window size - increased width for full title visibility
        self.setFixedSize(1400, 800)  # Further increased width and height
        
        # Create main layout with adjusted margins
        layout = QVBoxLayout()
        layout.setContentsMargins(50, 50, 50, 50)  # Increased margins
        layout.setSpacing(30)  # Increased spacing
        self.setLayout(layout)
        
        # Create a container widget with white background
        container = QWidget()
        container.setObjectName("container")
        container.setStyleSheet("""
            QWidget#container {
                background-color: white;
                border-radius: 20px;
            }
        """)
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(50, 50, 50, 50)  # Increased margins
        container_layout.setSpacing(30)  # Increased spacing
        
        # Create horizontal layout for title and image with more spacing
        title_layout = QHBoxLayout()
        title_layout.setAlignment(Qt.AlignCenter)
        title_layout.setSpacing(40)  # Increased spacing between image and text
        
        # Add turtle image with increased size
        image_label = QLabel()
        image_path = os.path.join(os.path.dirname(__file__), "assets", "turtle_detective.png")
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            # Increased size to 450x450
            scaled_pixmap = pixmap.scaled(450, 450, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            image_label.setPixmap(scaled_pixmap)
            image_label.setAlignment(Qt.AlignCenter)
        else:
            print(f"Warning: Could not find splash screen image at {image_path}")
        
        # Create vertical layout for title text with more spacing
        text_layout = QVBoxLayout()
        text_layout.setAlignment(Qt.AlignCenter)
        text_layout.setSpacing(20)  # Increased spacing between titles
        
        # Add EUROPA title with larger font
        europa_label = QLabel("EUROPA")
        europa_font = QFont("Arial", 54, QFont.Bold)  # Increased font size
        europa_label.setFont(europa_font)
        europa_label.setAlignment(Qt.AlignCenter)
        europa_label.setStyleSheet("color: #f97316;")  # Orange color
        europa_label.setMinimumWidth(700)  # Increased minimum width
        text_layout.addWidget(europa_label)
        
        # Add FORENSICS TOOL as second title with larger font
        tool_label = QLabel("FORENSICS TOOL")
        tool_font = QFont("Arial", 46, QFont.Bold)  # Increased font size
        tool_label.setFont(tool_font)
        tool_label.setAlignment(Qt.AlignCenter)
        tool_label.setStyleSheet("color: #f97316;")  # Orange color
        tool_label.setMinimumWidth(700)  # Increased minimum width
        text_layout.addWidget(tool_label)
        
        # Add subtitle with adjusted width and larger font
        subtitle_label = QLabel("Advanced Mobile Device Analysis")
        subtitle_font = QFont("Arial", 28)  # Increased font size
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("color: #3b82f6;")  # Blue color
        subtitle_label.setMinimumWidth(700)  # Increased minimum width
        text_layout.addSpacing(15)
        text_layout.addWidget(subtitle_label)
        
        # Add image and text to horizontal layout
        title_layout.addStretch(1)  # Add stretch before image for centering
        title_layout.addWidget(image_label)
        title_layout.addLayout(text_layout)
        title_layout.addStretch(1)  # Add stretch after text for centering
        
        # Add title layout to container layout
        container_layout.addLayout(title_layout)
        
        # Add spacer
        container_layout.addSpacing(40)
        
        # Add status label
        self.status_label = QLabel("Initializing...")
        status_font = QFont("Arial", 12)
        self.status_label.setFont(status_font)
        self.status_label.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(self.status_label)
        
        # Add progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("%p%")
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #3b82f6;
                border-radius: 5px;
                text-align: center;
                height: 25px;
            }
            QProgressBar::chunk {
                background-color: #3b82f6;
            }
        """)
        container_layout.addWidget(self.progress_bar)
        
        # Add version info
        version_label = QLabel("Version 1.0.0")
        version_font = QFont("Arial", 10)
        version_label.setFont(version_font)
        version_label.setAlignment(Qt.AlignRight)
        container_layout.addWidget(version_label)
        
        # Add container to main layout
        layout.addWidget(container)
        
        # Initialize status messages
        self.status_messages = [
            "Initializing modules...",
            "Loading forensic tools...",
            "Preparing data extraction...",
            "Configuring device connection...",
            "Starting analysis engine...",
            "Almost ready...",
            "Ready to begin forensic analysis!"
        ]
        self.current_status_index = 0
        
        # Set up timer for status updates
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.update_status)
        
        # Set up timer for progress updates
        self.progress_timer = QTimer()
        self.progress_timer.timeout.connect(self.update_progress)
        
        # Center the splash screen on the screen
        screen = QApplication.primaryScreen().geometry()
        self.move(
            (screen.width() - self.width()) // 2,
            (screen.height() - self.height()) // 2
        )
    
    def start(self):
        """Start the splash screen animation"""
        self.status_timer.start(1000)  # Update status every second
        self.progress_timer.start(50)  # Update progress every 50ms
        self.show()
    
    def update_status(self):
        """Update the status message"""
        if self.current_status_index < len(self.status_messages):
            self.status_label.setText(self.status_messages[self.current_status_index])
            self.current_status_index += 1
        else:
            self.status_timer.stop()
    
    def update_progress(self):
        """Update the progress bar"""
        current_value = self.progress_bar.value()
        if current_value < 100:
            # Slow down progress as it approaches 100%
            if current_value < 30:
                increment = 2
            elif current_value < 70:
                increment = 1
            else:
                increment = 0.5
                
            # Convert to integer before setting value
            new_value = int(min(100, current_value + increment))
            self.progress_bar.setValue(new_value)
        else:
            self.progress_timer.stop()
    
    def finish(self, main_window):
        """Finish the splash screen and show the main window"""
        # Stop any running timers to avoid background updates
        try:
            self.status_timer.stop()
        except Exception:
            pass
        try:
            self.progress_timer.stop()
        except Exception:
            pass

        # Close the splash and bring the main window to the foreground
        self.close()
        # Ensure the main window is visible and not minimized
        main_window.show()
        main_window.showNormal()
        main_window.raise_()
        main_window.activateWindow()
        # Clear minimized state and request activation
        try:
            main_window.setWindowState((main_window.windowState() & ~Qt.WindowMinimized) | Qt.WindowActive)
        except Exception:
            pass