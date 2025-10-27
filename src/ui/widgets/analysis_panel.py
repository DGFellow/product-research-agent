"""
Analysis Panel
Bottom panel showing profit analysis and opportunities
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGroupBox, QTextEdit
)
from PySide6.QtCore import Qt

class AnalysisPanel(QWidget):
    """Bottom panel for profit analysis"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """Initialize the analysis panel UI"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        
        # Top Opportunities
        opportunities_group = QGroupBox("🎯 Top Opportunities")
        opportunities_layout = QVBoxLayout()
        
        self.opportunities_text = QTextEdit()
        self.opportunities_text.setReadOnly(True)
        self.opportunities_text.setMaximumHeight(100)
        self.opportunities_text.setStyleSheet("""
            QTextEdit {
                background-color: #f9f9f9;
                border: 1px solid #ddd;
                border-radius: 3px;
                font-size: 11px;
                padding: 5px;
            }
        """)
        self.opportunities_text.setPlaceholderText("Top opportunities will appear here after analysis...")
        opportunities_layout.addWidget(self.opportunities_text)
        
        opportunities_group.setLayout(opportunities_layout)
        layout.addWidget(opportunities_group, 2)
        
        # Summary Stats
        stats_group = QGroupBox("📈 Summary Statistics")
        stats_layout = QVBoxLayout()
        
        self.avg_margin_label = QLabel("Avg Margin: --")
        self.avg_margin_label.setStyleSheet("font-size: 12px; padding: 3px;")
        stats_layout.addWidget(self.avg_margin_label)
        
        self.best_margin_label = QLabel("Best Margin: --")
        self.best_margin_label.setStyleSheet("font-size: 12px; padding: 3px;")
        stats_layout.addWidget(self.best_margin_label)
        
        self.total_products_label = QLabel("Total Products: 0")
        self.total_products_label.setStyleSheet("font-size: 12px; padding: 3px;")
        stats_layout.addWidget(self.total_products_label)
        
        self.viable_products_label = QLabel("Viable (>30%): 0")
        self.viable_products_label.setStyleSheet("font-size: 12px; padding: 3px; color: green;")
        stats_layout.addWidget(self.viable_products_label)
        
        stats_group.setLayout(stats_layout)
        layout.addWidget(stats_group, 1)
    
    def update_opportunities(self, opportunities: list):
        """Update top opportunities display"""
        if not opportunities:
            self.opportunities_text.setText("No opportunities found yet...")
            return
        
        text = ""
        for i, opp in enumerate(opportunities[:3], 1):
            text += f"{i}. {opp['product'][:40]}... - "
            text += f"{opp['margin']:.1f}% margin "
            text += f"(${opp['supplier_cost']:.2f} → ${opp['amazon_price']:.2f})\n"
        
        self.opportunities_text.setText(text)
    
    def update_stats(self, avg_margin: float, best_margin: float, 
                     total: int, viable: int):
        """Update summary statistics"""
        self.avg_margin_label.setText(f"Avg Margin: {avg_margin:.1f}%")
        self.best_margin_label.setText(f"Best Margin: {best_margin:.1f}%")
        self.total_products_label.setText(f"Total Products: {total}")
        self.viable_products_label.setText(f"Viable (>30%): {viable}")