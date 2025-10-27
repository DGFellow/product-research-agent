"""
Search Configuration Panel
Left sidebar with all search options
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QGroupBox, QLabel, QLineEdit,
    QSpinBox, QCheckBox, QPushButton, QComboBox, QDoubleSpinBox
)
from PySide6.QtCore import Signal
from src.models import SearchCriteria

class SearchPanel(QWidget):
    """Left panel for search configuration"""
    
    search_requested = Signal(dict)  # Emits search parameters
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """Initialize the search panel UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Title
        title = QLabel("🔍 Search Configuration")
        title.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(title)
        
        # Product Search Group
        search_group = QGroupBox("Product")
        search_layout = QVBoxLayout()
        
        search_layout.addWidget(QLabel("Search Term:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("e.g., wireless earbuds")
        search_layout.addWidget(self.search_input)
        
        search_group.setLayout(search_layout)
        layout.addWidget(search_group)
        
        # Platforms Group
        platforms_group = QGroupBox("Platforms")
        platforms_layout = QVBoxLayout()
        
        self.google_trends_check = QCheckBox("Google Trends (Market Research)")
        self.google_trends_check.setChecked(True)
        platforms_layout.addWidget(self.google_trends_check)
        
        self.alibaba_check = QCheckBox("Alibaba (Suppliers)")
        self.alibaba_check.setChecked(True)
        platforms_layout.addWidget(self.alibaba_check)
        
        self.amazon_check = QCheckBox("Amazon (Competition)")
        self.amazon_check.setChecked(True)
        platforms_layout.addWidget(self.amazon_check)
        
        platforms_group.setLayout(platforms_layout)
        layout.addWidget(platforms_group)
        
        # Criteria Group
        criteria_group = QGroupBox("Search Criteria")
        criteria_layout = QVBoxLayout()
        
        # Max products
        criteria_layout.addWidget(QLabel("Max Products per Site:"))
        self.max_products_spin = QSpinBox()
        self.max_products_spin.setRange(1, 50)
        self.max_products_spin.setValue(10)
        criteria_layout.addWidget(self.max_products_spin)
        
        # Min MOQ
        criteria_layout.addWidget(QLabel("Min MOQ (Alibaba):"))
        self.min_moq_spin = QSpinBox()
        self.min_moq_spin.setRange(1, 10000)
        self.min_moq_spin.setValue(100)
        self.min_moq_spin.setSuffix(" units")
        criteria_layout.addWidget(self.min_moq_spin)
        
        # Min Margin
        criteria_layout.addWidget(QLabel("Target Profit Margin:"))
        self.min_margin_spin = QDoubleSpinBox()
        self.min_margin_spin.setRange(0, 100)
        self.min_margin_spin.setValue(30)
        self.min_margin_spin.setSuffix("%")
        criteria_layout.addWidget(self.min_margin_spin)
        
        criteria_group.setLayout(criteria_layout)
        layout.addWidget(criteria_group)
        
        # Options Group
        options_group = QGroupBox("Options")
        options_layout = QVBoxLayout()
        
        self.headless_check = QCheckBox("Headless Mode (faster)")
        self.headless_check.setChecked(False)
        options_layout.addWidget(self.headless_check)
        
        self.detailed_check = QCheckBox("Detailed Analysis")
        self.detailed_check.setChecked(True)
        options_layout.addWidget(self.detailed_check)
        
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)
        
        # Start Button
        self.start_button = QPushButton("🚀 Start Research")
        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 12px;
                border-radius: 5px;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        self.start_button.clicked.connect(self.on_start_clicked)
        layout.addWidget(self.start_button)
        
        # Stop Button
        self.stop_button = QPushButton("⏹ Stop Research")
        self.stop_button.setEnabled(False)
        self.stop_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                font-size: 12px;
                font-weight: bold;
                padding: 8px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)
        layout.addWidget(self.stop_button)
        
        layout.addStretch()
    
    def on_start_clicked(self):
        """Emit search parameters when start is clicked"""
        search_term = self.search_input.text().strip()
        
        if not search_term:
            return
        
        params = {
            'search_term': search_term,
            'platforms': {
                'google_trends': self.google_trends_check.isChecked(),
                'alibaba': self.alibaba_check.isChecked(),
                'amazon': self.amazon_check.isChecked(),
            },
            'max_products': self.max_products_spin.value(),
            'min_moq': self.min_moq_spin.value(),
            'min_margin': self.min_margin_spin.value(),
            'headless': self.headless_check.isChecked(),
            'detailed': self.detailed_check.isChecked(),
        }
        
        self.search_requested.emit(params)
    
    def set_research_state(self, is_running: bool):
        """Enable/disable controls based on research state"""
        self.start_button.setEnabled(not is_running)
        self.stop_button.setEnabled(is_running)
        self.search_input.setEnabled(not is_running)
        self.max_products_spin.setEnabled(not is_running)
        self.min_moq_spin.setEnabled(not is_running)
        self.min_margin_spin.setEnabled(not is_running)
        self.google_trends_check.setEnabled(not is_running)
        self.alibaba_check.setEnabled(not is_running)
        self.amazon_check.setEnabled(not is_running)
        self.headless_check.setEnabled(not is_running)
        self.detailed_check.setEnabled(not is_running)