"""
Progress Panel
Center panel showing LLM activity and research progress
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QProgressBar
from PySide6.QtCore import Qt
from PySide6.QtGui import QTextCursor

class ProgressPanel(QWidget):
    """Center panel for progress tracking and LLM activity"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """Initialize the progress panel UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Title
        title = QLabel("🧠 Research Progress & AI Activity")
        title.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(title)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #ddd;
                border-radius: 5px;
                text-align: center;
                height: 25px;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
            }
        """)
        layout.addWidget(self.progress_bar)
        
        # Activity log
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 11px;
                border: 2px solid #333;
                border-radius: 5px;
                padding: 5px;
            }
        """)
        layout.addWidget(self.log_text)
        
        # Current phase label
        self.phase_label = QLabel("Ready to start research")
        self.phase_label.setStyleSheet("""
            QLabel {
                color: #666;
                font-size: 12px;
                padding: 5px;
            }
        """)
        layout.addWidget(self.phase_label)
    
    def append_log(self, message: str):
        """Append message to activity log"""
        self.log_text.append(message)
        # Auto-scroll to bottom
        cursor = self.log_text.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.log_text.setTextCursor(cursor)
    
    def clear_log(self):
        """Clear the activity log"""
        self.log_text.clear()
    
    def set_progress(self, value: int, message: str = ""):
        """Update progress bar"""
        self.progress_bar.setValue(value)
        if message:
            self.progress_bar.setFormat(f"{value}% - {message}")
    
    def set_phase(self, phase: str):
        """Update current phase label"""
        self.phase_label.setText(f"Current Phase: {phase}")