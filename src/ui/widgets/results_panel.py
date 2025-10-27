"""
Results Panel
Right panel showing live research results
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget,
    QTableWidgetItem, QPushButton, QHeaderView, QComboBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

class ResultsPanel(QWidget):
    """Right panel for displaying live results"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """Initialize the results panel UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Title and controls
        header_layout = QHBoxLayout()
        
        title = QLabel("📊 Live Results")
        title.setStyleSheet("font-size: 14px; font-weight: bold;")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Sort dropdown
        header_layout.addWidget(QLabel("Sort by:"))
        self.sort_combo = QComboBox()
        self.sort_combo.addItems([
            "Margin (High to Low)",
            "Margin (Low to High)",
            "Price (Low to High)",
            "Price (High to Low)",
            "Source"
        ])
        self.sort_combo.currentTextChanged.connect(self.on_sort_changed)
        header_layout.addWidget(self.sort_combo)
        
        layout.addLayout(header_layout)
        
        # Results table
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(7)
        self.results_table.setHorizontalHeaderLabels([
            "Source", "Product", "Supplier Cost", "Amazon Price", 
            "Profit", "Margin %", "Status"
        ])
        
        # Style the table
        self.results_table.setStyleSheet("""
            QTableWidget {
                border: 2px solid #ddd;
                border-radius: 5px;
                background-color: white;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QHeaderView::section {
                background-color: #f0f0f0;
                padding: 5px;
                border: 1px solid #ddd;
                font-weight: bold;
            }
        """)
        
        # Make columns resize nicely
        header = self.results_table.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)  # Product name stretches
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)
        
        self.results_table.setAlternatingRowColors(True)
        self.results_table.setSelectionBehavior(QTableWidget.SelectRows)
        
        layout.addWidget(self.results_table)
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        self.export_button = QPushButton("📥 Export Results")
        self.export_button.clicked.connect(self.on_export_clicked)
        button_layout.addWidget(self.export_button)
        
        self.clear_button = QPushButton("🗑️ Clear")
        self.clear_button.clicked.connect(self.clear_results)
        button_layout.addWidget(self.clear_button)
        
        button_layout.addStretch()
        
        # Results count label
        self.count_label = QLabel("0 products")
        self.count_label.setStyleSheet("color: #666; font-size: 12px;")
        button_layout.addWidget(self.count_label)
        
        layout.addLayout(button_layout)
    
    def add_result(self, source: str, product: str, supplier_cost: float, 
                   amazon_price: float, profit: float, margin: float):
        """Add a result row to the table"""
        row = self.results_table.rowCount()
        self.results_table.insertRow(row)
        
        # Source
        self.results_table.setItem(row, 0, QTableWidgetItem(source.capitalize()))
        
        # Product (truncate if too long)
        product_item = QTableWidgetItem(product[:50] + "..." if len(product) > 50 else product)
        product_item.setToolTip(product)  # Full name on hover
        self.results_table.setItem(row, 1, product_item)
        
        # Supplier Cost
        cost_item = QTableWidgetItem(f"${supplier_cost:.2f}" if supplier_cost else "N/A")
        cost_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.results_table.setItem(row, 2, cost_item)
        
        # Amazon Price
        price_item = QTableWidgetItem(f"${amazon_price:.2f}" if amazon_price else "N/A")
        price_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.results_table.setItem(row, 3, price_item)
        
        # Profit
        profit_item = QTableWidgetItem(f"${profit:.2f}" if profit else "N/A")
        profit_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        if profit and profit > 0:
            profit_item.setForeground(QColor(0, 128, 0))  # Green for profit
        self.results_table.setItem(row, 4, profit_item)
        
        # Margin %
        margin_item = QTableWidgetItem(f"{margin:.1f}%" if margin else "N/A")
        margin_item.setTextAlignment(Qt.AlignCenter)
        
        # Color code margin
        if margin:
            if margin >= 50:
                margin_item.setBackground(QColor(200, 255, 200))  # Light green
            elif margin >= 30:
                margin_item.setBackground(QColor(255, 255, 200))  # Light yellow
            else:
                margin_item.setBackground(QColor(255, 220, 220))  # Light red
        
        self.results_table.setItem(row, 5, margin_item)
        
        # Status
        if margin and margin >= 30:
            status_item = QTableWidgetItem("✅ Good")
            status_item.setForeground(QColor(0, 128, 0))
        elif margin:
            status_item = QTableWidgetItem("⚠️ Low")
            status_item.setForeground(QColor(200, 100, 0))
        else:
            status_item = QTableWidgetItem("❓ Unknown")
        
        status_item.setTextAlignment(Qt.AlignCenter)
        self.results_table.setItem(row, 6, status_item)
        
        # Update count
        self.update_count()
    
    def clear_results(self):
        """Clear all results"""
        self.results_table.setRowCount(0)
        self.update_count()
    
    def update_count(self):
        """Update the results count label"""
        count = self.results_table.rowCount()
        self.count_label.setText(f"{count} product{'s' if count != 1 else ''}")
    
    def on_sort_changed(self, sort_option: str):
        """Handle sort option change"""
        # TODO: Implement sorting logic
        pass
    
    def on_export_clicked(self):
        """Handle export button click"""
        # TODO: Implement export dialog
        pass
    
    def get_all_results(self):
        """Get all results as list of dicts"""
        results = []
        for row in range(self.results_table.rowCount()):
            result = {
                'source': self.results_table.item(row, 0).text(),
                'product': self.results_table.item(row, 1).text(),
                'supplier_cost': self.results_table.item(row, 2).text(),
                'amazon_price': self.results_table.item(row, 3).text(),
                'profit': self.results_table.item(row, 4).text(),
                'margin': self.results_table.item(row, 5).text(),
                'status': self.results_table.item(row, 6).text(),
            }
            results.append(result)
        return results