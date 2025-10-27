"""
Browser Preview Widget
Shows a small preview of the browser activity
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap
from pathlib import Path

class BrowserPreview(QWidget):
    """Mini browser preview"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        self.preview_label = QLabel("Browser Preview")
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setStyleSheet("""
            QLabel {
                border: 2px solid #ddd;
                background-color: #f5f5f5;
                min-height: 200px;
            }
        """)
        
        layout.addWidget(self.preview_label)
    
    def update_screenshot(self, image_path: Path):
        """Update with new screenshot"""
        pixmap = QPixmap(str(image_path))
        scaled = pixmap.scaled(400, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.preview_label.setPixmap(scaled)