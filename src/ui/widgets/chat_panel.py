"""
Chat Agent Panel
Conversational interface for interacting with the AI agent
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit,
    QLineEdit, QPushButton
)
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QTextCursor
from datetime import datetime

class ChatPanel(QWidget):
    """Left panel for conversational agent interaction"""
    
    message_sent = Signal(str)
    command_detected = Signal(dict)
    
    def __init__(self):
        super().__init__()
        self.chat_history = []
        self.init_ui()
        # Your updated welcome messages go here
        self.add_system_message("👋 Hello! I'm your AI Product Research Assistant.")
        self.add_system_message("\n📚 What I can do:")
        self.add_system_message("• Search products with natural language")
        self.add_system_message("• Control which platforms to search")
        self.add_system_message("• Adjust settings on the fly")
        self.add_system_message("\n💡 Try these:")
        self.add_system_message("🔹 'Search for wireless earbuds on Amazon only'")
        self.add_system_message("🔹 'Find phone cases but skip Alibaba'")
        self.add_system_message("🔹 'Set max products to 20'")
    
    def init_ui(self):
        """Initialize the chat panel UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Title
        title = QLabel("💬 Chat with Agent")
        title.setStyleSheet("font-size: 14px; font-weight: bold; margin-bottom: 5px;")
        layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Guide the research with natural language")
        subtitle.setStyleSheet("font-size: 10px; color: #666; margin-bottom: 10px;")
        layout.addWidget(subtitle)
        
        # Chat display area
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setStyleSheet("""
            QTextEdit {
                background-color: #f9f9f9;
                border: 2px solid #ddd;
                border-radius: 8px;
                padding: 10px;
                font-size: 12px;
                line-height: 1.4;
            }
        """)
        layout.addWidget(self.chat_display)
        
        # Input area
        input_layout = QVBoxLayout()
        
        # Input field
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Type your message or command...")
        self.input_field.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #4CAF50;
                border-radius: 5px;
                font-size: 12px;
                background-color: white;
            }
            QLineEdit:focus {
                border: 2px solid #2E7D32;
            }
        """)
        self.input_field.returnPressed.connect(self.on_send_clicked)
        input_layout.addWidget(self.input_field)
        
        # Send button row
        button_layout = QHBoxLayout()
        
        self.send_button = QPushButton("📤 Send")
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
                padding: 10px 20px;
                border-radius: 5px;
                border: none;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #2E7D32;
            }
        """)
        self.send_button.clicked.connect(self.on_send_clicked)
        button_layout.addWidget(self.send_button)
        
        self.clear_button = QPushButton("🗑️")
        self.clear_button.setToolTip("Clear chat history")
        self.clear_button.setFixedWidth(45)
        self.clear_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
                border: none;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)
        self.clear_button.clicked.connect(self.clear_chat)
        button_layout.addWidget(self.clear_button)
        
        input_layout.addLayout(button_layout)
        layout.addLayout(input_layout)
    
    def on_send_clicked(self):
        """Handle send button click"""
        message = self.input_field.text().strip()
        
        if not message:
            return
        
        self.add_user_message(message)
        self.input_field.clear()
        self.message_sent.emit(message)
        
        self.chat_history.append({
            'role': 'user',
            'content': message,
            'timestamp': datetime.now()
        })
    
    def add_user_message(self, message: str):
        """Add user message to chat display"""
        timestamp = datetime.now().strftime("%H:%M")
        
        html = f"""
        <div style='margin-bottom: 10px;'>
            <div style='background-color: #4CAF50; color: white; padding: 8px 12px; 
                        border-radius: 12px 12px 0 12px; display: inline-block; 
                        max-width: 80%; float: right; margin-left: 20%;'>
                <strong>You</strong> <span style='font-size: 9px; opacity: 0.8;'>{timestamp}</span><br>
                {message}
            </div>
            <div style='clear: both;'></div>
        </div>
        """
        
        self.chat_display.append(html)
        self._scroll_to_bottom()
    
    def add_agent_message(self, message: str):
        """Add agent response to chat display"""
        timestamp = datetime.now().strftime("%H:%M")
        
        html = f"""
        <div style='margin-bottom: 10px;'>
            <div style='background-color: #e3f2fd; color: #333; padding: 8px 12px; 
                        border-radius: 12px 12px 12px 0; display: inline-block; 
                        max-width: 80%; float: left; margin-right: 20%;'>
                <strong>🤖 Agent</strong> <span style='font-size: 9px; opacity: 0.6;'>{timestamp}</span><br>
                {message}
            </div>
            <div style='clear: both;'></div>
        </div>
        """
        
        self.chat_display.append(html)
        self._scroll_to_bottom()
        
        self.chat_history.append({
            'role': 'agent',
            'content': message,
            'timestamp': datetime.now()
        })
    
    def add_agent_message_streaming(self, message: str):
        """Add/update agent message with streaming effect"""
        # Remove the last message if it's a partial agent message
        cursor = self.chat_display.textCursor()
        cursor.movePosition(QTextCursor.End)
        
        timestamp = datetime.now().strftime("%H:%M")
        
        html = f"""
        <div style='margin-bottom: 10px;' id='streaming-message'>
            <div style='background-color: #e3f2fd; color: #333; padding: 8px 12px; 
                        border-radius: 12px 12px 12px 0; display: inline-block; 
                        max-width: 80%; float: left; margin-right: 20%;'>
                <strong>🤖 Agent</strong> <span style='font-size: 9px; opacity: 0.6;'>{timestamp}</span><br>
                {message}
            </div>
            <div style='clear: both;'></div>
        </div>
        """
        
        self.chat_display.append(html)
        self._scroll_to_bottom()
    
    def add_system_message(self, message: str):
        """Add system message to chat display"""
        html = f"""
        <div style='margin-bottom: 8px; text-align: center;'>
            <div style='background-color: #f0f0f0; color: #666; padding: 5px 10px; 
                        border-radius: 5px; display: inline-block; font-size: 11px;'>
                {message}
            </div>
        </div>
        """
        
        self.chat_display.append(html)
        self._scroll_to_bottom()
    
    def add_loading_message(self):
        """Add a loading indicator"""
        html = """
        <div style='margin-bottom: 10px;' id='loading-message'>
            <div style='background-color: #e3f2fd; color: #333; padding: 8px 12px; 
                        border-radius: 12px 12px 12px 0; display: inline-block; 
                        max-width: 80%; float: left; margin-right: 20%;'>
                <strong>🤖 Agent</strong><br>
                <span style='color: #666;'>●●● Thinking...</span>
            </div>
            <div style='clear: both;'></div>
        </div>
        """
        
        self.chat_display.append(html)
        self._scroll_to_bottom()
    
    def clear_chat(self):
        """Clear chat history"""
        self.chat_display.clear()
        self.chat_history = []
        self.add_system_message("Chat cleared. How can I help you?")
    
    def _scroll_to_bottom(self):
        """Scroll chat display to bottom"""
        cursor = self.chat_display.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.chat_display.setTextCursor(cursor)
    
    def set_input_enabled(self, enabled: bool):
        """Enable/disable input during research"""
        self.input_field.setEnabled(enabled)
        self.send_button.setEnabled(enabled)