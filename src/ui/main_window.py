"""
Main Window
Orchestrates all UI panels and coordinates the research workflow
"""
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QMessageBox, QFileDialog
)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QIcon
import asyncio
from pathlib import Path

from src.ui.widgets.search_panel import SearchPanel
from src.ui.widgets.progress_panel import ProgressPanel
from src.ui.widgets.results_panel import ResultsPanel
from src.ui.widgets.analysis_panel import AnalysisPanel
from src.llm_client import LLMClient
from src.agents.product_agent import ProductResearchAgent
from src.analysis.analyzer import ProductAnalyzer
from src.config import Config
from src.models import ProductInfo


class ResearchWorker(QThread):
    """Background thread for running research"""
    progress = Signal(str)           # Progress messages
    log = Signal(str)                # Log messages
    phase_changed = Signal(str)      # Current phase
    progress_percent = Signal(int)   # Progress percentage
    result_added = Signal(dict)      # New result to add
    finished = Signal(list)          # Final products list
    error = Signal(str)              # Error messages
    
    def __init__(self, search_params):
        super().__init__()
        self.search_params = search_params
        self.agent = None
        self._is_running = True
    
    def stop(self):
        """Request worker to stop"""
        self._is_running = False
    
    def run(self):
        """Run the research in background thread"""
        try:
            asyncio.run(self._run_research())
        except Exception as e:
            self.error.emit(f"Error: {str(e)}")
            import traceback
            self.error.emit(traceback.format_exc())
    
    async def _run_research(self):
        """Actual research logic with enhanced progress tracking"""
        try:
            search_term = self.search_params['search_term']
            platforms = self.search_params['platforms']  # ← This exists
            max_products = self.search_params['max_products']
            headless = self.search_params['headless']
            
            # Setup
            Config.HEADLESS = headless
            Config.MAX_PRODUCTS_PER_SITE = max_products
            
            self.phase_changed.emit("Initialization")
            self.progress_percent.emit(5)
            
            # Connect to LLM
            self.log.emit("🤖 Connecting to local LLM...")
            llm = LLMClient()
            
            if not llm.is_available():
                self.log.emit("⚠️  Warning: LLM not available. Continuing with basic functionality.")
            else:
                self.log.emit("✅ LLM connected")
            
            self.progress_percent.emit(10)
            
            # Initialize agent
            self.agent = ProductResearchAgent(llm)
            self.agent.set_platforms(platforms)  # ← ADD THIS LINE!
            
            self.log.emit("🚀 Initializing browser...")
            await self.agent.initialize()
            self.log.emit("✅ Browser ready")
            
            self.progress_percent.emit(20)
            
            # Phase 1: Market Research (if enabled)
            if platforms['google_trends']:
                self.phase_changed.emit("Market Research")
                self.log.emit("\n" + "="*60)
                self.log.emit("📊 Phase 1: Market Research (Google Trends)")
                self.log.emit("="*60)
                # TODO: Implement Google Trends
                self.log.emit("⚠️  Google Trends: Coming soon!")
                self.progress_percent.emit(30)
            
            # Phase 2: Product Research
            self.phase_changed.emit("Product Research")
            self.log.emit("\n" + "="*60)
            self.log.emit(f"🔬 Researching: {search_term}")
            self.log.emit("="*60 + "\n")
            
            self.progress_percent.emit(40)
            
            products = await self.agent.research_product(search_term)
            
            # Emit results as they come in
            for product in products:
                if not self._is_running:
                    break
                
                # Calculate basic metrics (will be enhanced later)
                result_data = {
                    'source': product.source,
                    'product': product.title,
                    'supplier_cost': self._extract_price(product.price) if product.source == 'alibaba' else None,
                    'amazon_price': self._extract_price(product.price) if product.source == 'amazon' else None,
                    'profit': 0.0,  # Will calculate when we have both prices
                    'margin': 0.0
                }
                
                self.result_added.emit(result_data)
            
            self.progress_percent.emit(80)
            
            if not products:
                self.log.emit("⚠️  No products found")
                self.finished.emit([])
                return
            
            # Phase 3: Analysis
            self.phase_changed.emit("Analysis")
            self.log.emit(f"\n{'='*60}")
            self.log.emit("📊 Generating Analysis...")
            self.log.emit(f"{'='*60}\n")
            
            analyzer = ProductAnalyzer(products)
            analyzer.export_csv()
            analyzer.create_visualizations()
            
            stats = analyzer.get_summary_stats()
            
            self.progress_percent.emit(95)
            
            self.log.emit(f"\n{'='*60}")
            self.log.emit("✅ Research Complete!")
            self.log.emit(f"{'='*60}")
            self.log.emit(f"\n📊 Summary:")
            self.log.emit(f"  Total: {stats['total_products']} products")
            if 'by_source' in stats:
                self.log.emit(f"  By source: {stats['by_source']}")
            if stats.get('price_stats'):
                ps = stats['price_stats']
                self.log.emit(f"  Avg price: ${ps['mean']:.2f}")
                self.log.emit(f"  Range: ${ps['min']:.2f} - ${ps['max']:.2f}")
            
            self.log.emit(f"\n📁 Files:")
            self.log.emit(f"   📄 {Config.OUTPUT_DIR}/product_research.csv")
            self.log.emit(f"   📊 {Config.OUTPUT_DIR}/product_analysis.png\n")
            
            self.progress_percent.emit(100)
            self.finished.emit(products)
            
        except Exception as e:
            self.error.emit(str(e))
            import traceback
            self.error.emit(traceback.format_exc())
        finally:
            if self.agent:
                await self.agent.close()
    
    def _extract_price(self, price_str: str) -> float:
        """Extract numeric price from string"""
        if not price_str or price_str == "N/A":
            return 0.0
        
        import re
        match = re.search(r'[\d,]+\.?\d*', str(price_str))
        if match:
            return float(match.group().replace(',', ''))
        return 0.0


class MainWindow(QMainWindow):
    """Main application window with modular panel layout"""
    
    def __init__(self):
        super().__init__()
        self.worker = None
        self.results_data = []
        self.init_ui()
    
    def init_ui(self):
        """Initialize the main window UI"""
        self.setWindowTitle("🤖 AI Product Research Agent - Professional Edition")
        self.setGeometry(100, 50, 1600, 900)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create main horizontal splitter (3 panels)
        main_splitter = QSplitter(Qt.Horizontal)
        
        # Left Panel: Search Configuration
        self.search_panel = SearchPanel()
        self.search_panel.search_requested.connect(self.on_search_requested)
        self.search_panel.stop_button.clicked.connect(self.stop_research)
        main_splitter.addWidget(self.search_panel)
        
        # Center Panel: Progress & Activity
        self.progress_panel = ProgressPanel()
        main_splitter.addWidget(self.progress_panel)
        
        # Right Panel: Results
        self.results_panel = ResultsPanel()
        main_splitter.addWidget(self.results_panel)
        
        # Set initial sizes (left: 300px, center: flexible, right: 500px)
        main_splitter.setSizes([300, 600, 500])
        
        main_layout.addWidget(main_splitter, 3)  # Takes 75% of height
        
        # Bottom Panel: Analysis
        self.analysis_panel = AnalysisPanel()
        main_layout.addWidget(self.analysis_panel, 1)  # Takes 25% of height
        
        # Status bar
        self.statusBar().showMessage("Ready to start research")
        
        # Style the main window
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QSplitter::handle {
                background-color: #ddd;
                width: 2px;
            }
            QSplitter::handle:hover {
                background-color: #4CAF50;
            }
        """)
    
    def on_search_requested(self, search_params: dict):
        """Handle search request from search panel"""
        search_term = search_params['search_term']
        
        # Validate platforms
        if not any(search_params['platforms'].values()):
            QMessageBox.warning(
                self,
                "No Platforms Selected",
                "Please select at least one platform to search!"
            )
            return
        
        # Check if LLM is running (if Google Trends or detailed analysis requested)
        if search_params['platforms']['google_trends'] or search_params['detailed']:
            llm = LLMClient()
            if not llm.is_available():
                reply = QMessageBox.question(
                    self,
                    "LLM Not Available",
                    "Local LLM API is not running. Some features will be limited.\n\n"
                    "Start local-llm API server first for full AI features.\n\n"
                    "Continue anyway?",
                    QMessageBox.Yes | QMessageBox.No
                )
                if reply == QMessageBox.No:
                    return
        
        # Clear previous results
        self.results_panel.clear_results()
        self.progress_panel.clear_log()
        self.progress_panel.set_progress(0)
        self.results_data = []
        
        # Update UI state
        self.search_panel.set_research_state(True)
        self.statusBar().showMessage(f"Researching: {search_term}...")
        
        # Start worker thread
        self.worker = ResearchWorker(search_params)
        self.worker.log.connect(self.progress_panel.append_log)
        self.worker.phase_changed.connect(self.progress_panel.set_phase)
        self.worker.progress_percent.connect(self.progress_panel.set_progress)
        self.worker.result_added.connect(self.on_result_added)
        self.worker.finished.connect(self.on_research_finished)
        self.worker.error.connect(self.on_error)
        self.worker.start()
    
    def on_result_added(self, result_data: dict):
        """Handle new result from worker"""
        self.results_data.append(result_data)
        
        # Add to results table
        self.results_panel.add_result(
            source=result_data['source'],
            product=result_data['product'],
            supplier_cost=result_data.get('supplier_cost', 0.0),
            amazon_price=result_data.get('amazon_price', 0.0),
            profit=result_data.get('profit', 0.0),
            margin=result_data.get('margin', 0.0)
        )
        
        # Update analysis panel
        self.update_analysis()
    
    def on_research_finished(self, products: list):
        """Handle research completion"""
        self.search_panel.set_research_state(False)
        self.statusBar().showMessage(f"Complete! Found {len(products)} products")
        
        # Calculate final profit analysis
        self.calculate_profit_analysis()
        
        QMessageBox.information(
            self,
            "Research Complete",
            f"Successfully researched {len(products)} products!\n\n"
            f"Results exported to outputs folder."
        )
    
    def on_error(self, error_msg: str):
        """Handle errors"""
        self.progress_panel.append_log(f"\n❌ Error: {error_msg}")
        self.search_panel.set_research_state(False)
        self.statusBar().showMessage("Error occurred")
        
        if "Traceback" not in error_msg:  # Don't show full traceback in dialog
            QMessageBox.critical(self, "Error", f"An error occurred:\n\n{error_msg}")
    
    def stop_research(self):
        """Stop the research process"""
        if self.worker and self.worker.isRunning():
            self.worker.stop()
            self.worker.terminate()
            self.worker.wait()
            self.progress_panel.append_log("\n❌ Research stopped by user")
            self.search_panel.set_research_state(False)
            self.statusBar().showMessage("Stopped")
    
    def update_analysis(self):
        """Update analysis panel with current results"""
        if not self.results_data:
            return
        
        # Calculate stats
        margins = [r['margin'] for r in self.results_data if r.get('margin', 0) > 0]
        
        if margins:
            avg_margin = sum(margins) / len(margins)
            best_margin = max(margins)
            viable = sum(1 for m in margins if m >= 30)
        else:
            avg_margin = 0
            best_margin = 0
            viable = 0
        
        total = len(self.results_data)
        
        self.analysis_panel.update_stats(avg_margin, best_margin, total, viable)
        
        # Update opportunities (top 3 by margin)
        sorted_results = sorted(
            [r for r in self.results_data if r.get('margin', 0) > 0],
            key=lambda x: x.get('margin', 0),
            reverse=True
        )
        self.analysis_panel.update_opportunities(sorted_results[:3])
    
    def calculate_profit_analysis(self):
        """Calculate detailed profit analysis"""
        # TODO: Implement sophisticated profit calculation
        # For now, just use basic margin calculation
        self.update_analysis()
    
    def closeEvent(self, event):
        """Handle window close event"""
        if self.worker and self.worker.isRunning():
            reply = QMessageBox.question(
                self,
                "Research in Progress",
                "Research is still running. Are you sure you want to quit?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                self.worker.stop()
                self.worker.terminate()
                self.worker.wait()
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()