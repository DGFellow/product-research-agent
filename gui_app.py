"""
PySide6 GUI for Product Research Agent
"""
import sys
import asyncio
from pathlib import Path
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit, QSpinBox, QCheckBox,
    QProgressBar, QGroupBox, QFileDialog, QMessageBox
)
from PySide6.QtCore import QThread, Signal, Qt
from PySide6.QtGui import QFont, QTextCursor

from src.llm_client import LLMClient
from src.agents.product_agent import ProductResearchAgent
from src.analysis.analyzer import ProductAnalyzer
from src.config import Config


class ResearchWorker(QThread):
    """Background thread for running research"""
    progress = Signal(str)  # Progress messages
    finished = Signal(list)  # Final products list
    error = Signal(str)     # Error messages
    
    def __init__(self, search_term, max_products, headless):
        super().__init__()
        self.search_term = search_term
        self.max_products = max_products
        self.headless = headless
        self.agent = None
    
    def run(self):
        """Run the research in background thread"""
        try:
            # Run async code in this thread
            asyncio.run(self._run_research())
        except Exception as e:
            self.error.emit(f"Error: {str(e)}")
    
    async def _run_research(self):
        """Actual research logic"""
        try:
            # Setup
            Config.HEADLESS = self.headless
            Config.MAX_PRODUCTS_PER_SITE = self.max_products
            
            self.progress.emit("🤖 Connecting to local LLM...")
            llm = LLMClient()
            
            if not llm.is_available():
                self.progress.emit("⚠️  Warning: LLM not available. Continuing with basic functionality.")
            else:
                self.progress.emit("✅ LLM connected")
            
            # Initialize agent
            self.agent = ProductResearchAgent(llm)
            self.progress.emit("🚀 Initializing browser...")
            await self.agent.initialize()
            self.progress.emit("✅ Browser ready")
            
            # Run research
            self.progress.emit(f"\n{'='*60}")
            self.progress.emit(f"🔬 Researching: {self.search_term}")
            self.progress.emit(f"{'='*60}\n")
            
            products = await self.agent.research_product(self.search_term)
            
            if not products:
                self.progress.emit("⚠️  No products found")
                self.finished.emit([])
                return
            
            # Analyze
            self.progress.emit(f"\n{'='*60}")
            self.progress.emit("📊 Generating Analysis...")
            self.progress.emit(f"{'='*60}\n")
            
            analyzer = ProductAnalyzer(products)
            analyzer.export_csv()
            analyzer.create_visualizations()
            
            stats = analyzer.get_summary_stats()
            
            self.progress.emit(f"\n{'='*60}")
            self.progress.emit("✅ Research Complete!")
            self.progress.emit(f"{'='*60}")
            self.progress.emit(f"\n📊 Summary:")
            self.progress.emit(f"  Total: {stats['total_products']} products")
            if 'by_source' in stats:
                self.progress.emit(f"  By source: {stats['by_source']}")
            if stats.get('price_stats'):
                ps = stats['price_stats']
                self.progress.emit(f"  Avg price: ${ps['mean']:.2f}")
                self.progress.emit(f"  Range: ${ps['min']:.2f} - ${ps['max']:.2f}")
            
            self.progress.emit(f"\n📁 Files:")
            self.progress.emit(f"   📄 {Config.OUTPUT_DIR}/product_research.csv")
            self.progress.emit(f"   📊 {Config.OUTPUT_DIR}/product_analysis.png\n")
            
            # Return results
            self.finished.emit(products)
            
        except Exception as e:
            self.error.emit(str(e))
            import traceback
            self.error.emit(traceback.format_exc())
        finally:
            if self.agent:
                await self.agent.close()


class ProductResearchGUI(QMainWindow):
    """Main GUI window"""
    
    def __init__(self):
        super().__init__()
        self.worker = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Product Research Agent")
        self.setGeometry(100, 100, 1000, 700)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Title
        title = QLabel("🤖 AI Product Research Agent")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)
        
        # Search section
        search_group = QGroupBox("Search Parameters")
        search_layout = QVBoxLayout()
        
        # Search term
        search_term_layout = QHBoxLayout()
        search_term_layout.addWidget(QLabel("Product:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter product to research (e.g., 'wireless earbuds')")
        search_term_layout.addWidget(self.search_input)
        search_layout.addLayout(search_term_layout)
        
        # Settings row
        settings_layout = QHBoxLayout()
        
        # Max products
        settings_layout.addWidget(QLabel("Max Products per Site:"))
        self.max_products_spin = QSpinBox()
        self.max_products_spin.setRange(1, 50)
        self.max_products_spin.setValue(10)
        settings_layout.addWidget(self.max_products_spin)
        
        # Headless mode
        self.headless_check = QCheckBox("Headless Mode (faster)")
        settings_layout.addWidget(self.headless_check)
        
        settings_layout.addStretch()
        search_layout.addLayout(settings_layout)
        
        search_group.setLayout(search_layout)
        main_layout.addWidget(search_group)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        self.start_button = QPushButton("🚀 Start Research")
        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        self.start_button.clicked.connect(self.start_research)
        button_layout.addWidget(self.start_button)
        
        self.stop_button = QPushButton("⏹ Stop")
        self.stop_button.setEnabled(False)
        self.stop_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)
        self.stop_button.clicked.connect(self.stop_research)
        button_layout.addWidget(self.stop_button)
        
        self.open_outputs_button = QPushButton("📁 Open Output Folder")
        self.open_outputs_button.clicked.connect(self.open_outputs)
        button_layout.addWidget(self.open_outputs_button)
        
        main_layout.addLayout(button_layout)
        
        # Progress section
        progress_group = QGroupBox("Progress")
        progress_layout = QVBoxLayout()
        
        self.progress_text = QTextEdit()
        self.progress_text.setReadOnly(True)
        self.progress_text.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                font-family: 'Courier New', monospace;
                font-size: 11px;
            }
        """)
        progress_layout.addWidget(self.progress_text)
        
        progress_group.setLayout(progress_layout)
        main_layout.addWidget(progress_group)
        
        # Status bar
        self.statusBar().showMessage("Ready")
    
    def start_research(self):
        """Start the research process"""
        search_term = self.search_input.text().strip()
        
        if not search_term:
            QMessageBox.warning(self, "Input Required", "Please enter a product to research!")
            return
        
        # Check if LLM is running
        llm = LLMClient()
        if not llm.is_available():
            reply = QMessageBox.question(
                self,
                "LLM Not Available",
                "Local LLM API is not running. The agent will work with limited functionality.\n\n"
                "Start local-llm API server first for full AI features.\n\n"
                "Continue anyway?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.No:
                return
        
        # Disable controls
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.search_input.setEnabled(False)
        self.max_products_spin.setEnabled(False)
        self.headless_check.setEnabled(False)
        
        # Clear previous output
        self.progress_text.clear()
        
        # Start worker thread
        self.worker = ResearchWorker(
            search_term,
            self.max_products_spin.value(),
            self.headless_check.isChecked()
        )
        self.worker.progress.connect(self.on_progress)
        self.worker.finished.connect(self.on_finished)
        self.worker.error.connect(self.on_error)
        self.worker.start()
        
        self.statusBar().showMessage(f"Researching: {search_term}...")
    
    def stop_research(self):
        """Stop the research process"""
        if self.worker and self.worker.isRunning():
            self.worker.terminate()
            self.worker.wait()
            self.append_progress("\n❌ Research stopped by user")
            self.reset_controls()
            self.statusBar().showMessage("Stopped")
    
    def on_progress(self, message):
        """Handle progress updates"""
        self.append_progress(message)
    
    def on_finished(self, products):
        """Handle research completion"""
        self.append_progress(f"\n✅ Found {len(products)} total products!")
        self.reset_controls()
        self.statusBar().showMessage(f"Complete! Found {len(products)} products")
        
        QMessageBox.information(
            self,
            "Research Complete",
            f"Successfully researched {len(products)} products!\n\n"
            f"Check outputs folder for results."
        )
    
    def on_error(self, error_msg):
        """Handle errors"""
        self.append_progress(f"\n❌ Error: {error_msg}")
        self.reset_controls()
        self.statusBar().showMessage("Error occurred")
        
        QMessageBox.critical(self, "Error", f"An error occurred:\n\n{error_msg}")
    
    def append_progress(self, message):
        """Append message to progress text"""
        self.progress_text.append(message)
        # Auto-scroll to bottom
        cursor = self.progress_text.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.progress_text.setTextCursor(cursor)
    
    def reset_controls(self):
        """Re-enable controls after research"""
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.search_input.setEnabled(True)
        self.max_products_spin.setEnabled(True)
        self.headless_check.setEnabled(True)
    
    def open_outputs(self):
        """Open the outputs folder"""
        import os
        import subprocess
        import platform
        
        output_path = Config.OUTPUT_DIR
        
        if platform.system() == "Windows":
            os.startfile(output_path)
        elif platform.system() == "Darwin":  # macOS
            subprocess.run(["open", output_path])
        else:  # Linux
            subprocess.run(["xdg-open", output_path])


def main():
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle("Fusion")
    
    window = ProductResearchGUI()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
