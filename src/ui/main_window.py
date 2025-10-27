"""
Main Window
Orchestrates all UI panels with conversational interface
"""
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QMessageBox, QFileDialog
)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QIcon
import asyncio
import re
from pathlib import Path

from src.ui.widgets.chat_panel import ChatPanel
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
    progress = Signal(str)
    log = Signal(str)
    phase_changed = Signal(str)
    progress_percent = Signal(int)
    result_added = Signal(dict)
    finished = Signal(list)
    error = Signal(str)
    
    def __init__(self, search_params):
        super().__init__()
        self.search_params = search_params
        self.agent = None
        self._is_running = True
    
    def stop(self):
        self._is_running = False
    
    def run(self):
        try:
            asyncio.run(self._run_research())
        except Exception as e:
            self.error.emit(f"Error: {str(e)}")
            import traceback
            self.error.emit(traceback.format_exc())
    
    async def _run_research(self):
        try:
            search_term = self.search_params['search_term']
            platforms = self.search_params['platforms']
            max_products = self.search_params['max_products']
            headless = self.search_params['headless']
            
            Config.HEADLESS = headless
            Config.MAX_PRODUCTS_PER_SITE = max_products
            
            self.phase_changed.emit("Initialization")
            self.progress_percent.emit(5)
            
            self.log.emit("🤖 Connecting to local LLM...")
            llm = LLMClient()
            
            if not llm.is_available():
                self.log.emit("⚠️  Warning: LLM not available. Continuing with basic functionality.")
            else:
                self.log.emit("✅ LLM connected")
            
            self.progress_percent.emit(10)
            
            self.agent = ProductResearchAgent(llm)
            self.agent.set_platforms(platforms)
            
            self.log.emit("🚀 Initializing browser...")
            await self.agent.initialize()
            self.log.emit("✅ Browser ready")
            
            self.progress_percent.emit(20)
            
            if platforms['google_trends']:
                self.phase_changed.emit("Market Research")
                self.log.emit("\n" + "="*60)
                self.log.emit("📊 Phase 1: Market Research (Google Trends)")
                self.log.emit("="*60)
                self.log.emit("⚠️  Google Trends: Coming soon!")
                self.progress_percent.emit(30)
            
            self.phase_changed.emit("Product Research")
            self.log.emit("\n" + "="*60)
            self.log.emit(f"🔬 Researching: {search_term}")
            self.log.emit("="*60 + "\n")
            
            self.progress_percent.emit(40)
            
            products = await self.agent.research_product(search_term)
            
            for product in products:
                if not self._is_running:
                    break
                
                result_data = {
                    'source': product.source,
                    'product': product.title,
                    'supplier_cost': self._extract_price(product.price) if product.source == 'alibaba' else None,
                    'amazon_price': self._extract_price(product.price) if product.source == 'amazon' else None,
                    'profit': 0.0,
                    'margin': 0.0
                }
                
                self.result_added.emit(result_data)
            
            self.progress_percent.emit(80)
            
            if not products:
                self.log.emit("⚠️  No products found")
                self.finished.emit([])
                return
            
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
        if not price_str or price_str == "N/A":
            return 0.0
        
        match = re.search(r'[\d,]+\.?\d*', str(price_str))
        if match:
            return float(match.group().replace(',', ''))
        return 0.0


class MainWindow(QMainWindow):
    """Main application window with conversational interface"""
    
    def __init__(self):
        super().__init__()
        self.worker = None
        self.results_data = []
        self.llm_client = None
        self.init_ui()
        self.init_llm()
    
    def init_llm(self):
        """Initialize LLM client for chat"""
        self.llm_client = LLMClient()
        if not self.llm_client.is_available():
            self.chat_panel.add_system_message("⚠️ LLM API not running. Chat features limited.")
    
    def init_ui(self):
        self.setWindowTitle("🤖 AI Product Research Agent - Professional Edition v2.0")
        self.setGeometry(50, 50, 1800, 900)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create main horizontal splitter (4 panels)
        main_splitter = QSplitter(Qt.Horizontal)
        
        # Panel 1: Chat Agent (NEW!)
        self.chat_panel = ChatPanel()
        self.chat_panel.message_sent.connect(self.on_chat_message)
        main_splitter.addWidget(self.chat_panel)
        
        # Panel 2: Search Configuration
        self.search_panel = SearchPanel()
        self.search_panel.search_requested.connect(self.on_search_requested)
        self.search_panel.stop_button.clicked.connect(self.stop_research)
        main_splitter.addWidget(self.search_panel)
        
        # Panel 3: Progress & Activity
        self.progress_panel = ProgressPanel()
        main_splitter.addWidget(self.progress_panel)
        
        # Panel 4: Results
        self.results_panel = ResultsPanel()
        main_splitter.addWidget(self.results_panel)
        
        # Set initial sizes (chat: 350px, search: 300px, progress: 550px, results: 600px)
        main_splitter.setSizes([350, 300, 550, 600])
        
        main_layout.addWidget(main_splitter, 3)
        
        # Bottom Panel: Analysis
        self.analysis_panel = AnalysisPanel()
        main_layout.addWidget(self.analysis_panel, 1)
        
        self.statusBar().showMessage("Ready - Chat with the agent or configure search")
        
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
    
    def on_chat_message(self, message: str):
        """Handle chat message from user"""
        # Parse message for commands
        command = self.parse_user_command(message)
        
        if command['action'] == 'search':
            # Agent understood search request
            self.chat_panel.add_agent_message(
                f"I'll search for '{command['search_term']}' on the selected platforms. Starting now!"
            )
            
            # Update search field
            self.search_panel.search_input.setText(command['search_term'])
            
            # Apply platform preferences if specified
            if 'platforms' in command:
                self.search_panel.alibaba_check.setChecked(command['platforms'].get('alibaba', True))
                self.search_panel.amazon_check.setChecked(command['platforms'].get('amazon', True))
                self.search_panel.google_trends_check.setChecked(command['platforms'].get('google_trends', False))
            
            # Trigger search
            self.search_panel.on_start_clicked()
            
        elif command['action'] == 'settings':
            self.chat_panel.add_agent_message(
                f"I've updated the settings:\n{command['message']}"
            )
            
            # Apply settings
            if 'max_products' in command:
                self.search_panel.max_products_spin.setValue(command['max_products'])
            if 'min_margin' in command:
                self.search_panel.min_margin_spin.setValue(command['min_margin'])
            
        elif command['action'] == 'help':
            self.chat_panel.add_agent_message(
                "I can help you with:\n"
                "• Searching for products\n"
                "• Adjusting search settings\n"
                "• Analyzing profit margins\n"
                "• Comparing platforms\n\n"
                "Try: 'Search for wireless earbuds on Amazon' or 'Set minimum margin to 40%'"
            )
        
        elif command['action'] == 'unknown':
            # Use LLM to generate response
            if self.llm_client and self.llm_client.is_available():
                response = self.llm_client.query(
                    prompt=f"User said: '{message}'. Respond helpfully as a product research assistant.",
                    system="You are a helpful product research assistant. Be brief and actionable.",
                    temperature=0.7,
                    max_tokens=150
                )
                self.chat_panel.add_agent_message(response)
            else:
                self.chat_panel.add_agent_message(
                    "I'm not sure I understand. Try:\n"
                    "• 'Search for [product]'\n"
                    "• 'Skip Alibaba'\n"
                    "• 'Set max products to 20'"
                )
    
    def parse_user_command(self, message: str) -> dict:
        """Parse user message into actionable command"""
        message_lower = message.lower()
        
        # Search commands
        search_patterns = [
            r'search for (.+?)(?:\s+on\s+(.+?))?$',
            r'find (.+?)(?:\s+on\s+(.+?))?$',
            r'look for (.+?)(?:\s+on\s+(.+?))?$',
        ]
        
        for pattern in search_patterns:
            match = re.search(pattern, message_lower)
            if match:
                search_term = match.group(1).strip()
                platforms_str = match.group(2) if match.lastindex > 1 else None
                
                # Parse platform preferences
                platforms = {'alibaba': True, 'amazon': True, 'google_trends': False}
                
                if platforms_str:
                    if 'amazon' in platforms_str and 'alibaba' not in platforms_str:
                        platforms = {'alibaba': False, 'amazon': True, 'google_trends': False}
                    elif 'alibaba' in platforms_str and 'amazon' not in platforms_str:
                        platforms = {'alibaba': True, 'amazon': False, 'google_trends': False}
                
                # Handle "only" keyword
                if 'only amazon' in message_lower or 'just amazon' in message_lower:
                    platforms = {'alibaba': False, 'amazon': True, 'google_trends': False}
                elif 'only alibaba' in message_lower or 'just alibaba' in message_lower:
                    platforms = {'alibaba': True, 'amazon': False, 'google_trends': False}
                
                # Handle skip commands
                if 'skip alibaba' in message_lower or 'no alibaba' in message_lower:
                    platforms['alibaba'] = False
                if 'skip amazon' in message_lower or 'no amazon' in message_lower:
                    platforms['amazon'] = False
                
                return {
                    'action': 'search',
                    'search_term': search_term,
                    'platforms': platforms
                }
        
        # Settings commands
        if 'set max' in message_lower or 'maximum' in message_lower:
            match = re.search(r'(\d+)', message)
            if match:
                return {
                    'action': 'settings',
                    'max_products': int(match.group(1)),
                    'message': f"Max products set to {match.group(1)}"
                }
        
        if 'margin' in message_lower and any(word in message_lower for word in ['set', 'minimum', 'target']):
            match = re.search(r'(\d+)', message)
            if match:
                return {
                    'action': 'settings',
                    'min_margin': float(match.group(1)),
                    'message': f"Target margin set to {match.group(1)}%"
                }
        
        # Help command
        if any(word in message_lower for word in ['help', 'what can you do', 'how', 'commands']):
            return {'action': 'help'}
        
        # Unknown
        return {'action': 'unknown'}
    
    def on_search_requested(self, search_params: dict):
        """Handle search request from search panel"""
        search_term = search_params['search_term']
        
        if not any(search_params['platforms'].values()):
            QMessageBox.warning(self, "No Platforms Selected", "Please select at least one platform!")
            return
        
        # Add agent message
        enabled_platforms = [k for k, v in search_params['platforms'].items() if v]
        self.chat_panel.add_agent_message(
            f"Starting research for '{search_term}' on: {', '.join(enabled_platforms)}"
        )
        
        self.results_panel.clear_results()
        self.progress_panel.clear_log()
        self.progress_panel.set_progress(0)
        self.results_data = []
        
        self.search_panel.set_research_state(True)
        self.chat_panel.set_input_enabled(False)
        self.statusBar().showMessage(f"Researching: {search_term}...")
        
        self.worker = ResearchWorker(search_params)
        self.worker.log.connect(self.progress_panel.append_log)
        self.worker.phase_changed.connect(self.progress_panel.set_phase)
        self.worker.progress_percent.connect(self.progress_panel.set_progress)
        self.worker.result_added.connect(self.on_result_added)
        self.worker.finished.connect(self.on_research_finished)
        self.worker.error.connect(self.on_error)
        self.worker.start()
    
    def on_result_added(self, result_data: dict):
        self.results_data.append(result_data)
        
        self.results_panel.add_result(
            source=result_data['source'],
            product=result_data['product'],
            supplier_cost=result_data.get('supplier_cost', 0.0),
            amazon_price=result_data.get('amazon_price', 0.0),
            profit=result_data.get('profit', 0.0),
            margin=result_data.get('margin', 0.0)
        )
        
        self.update_analysis()
    
    def on_research_finished(self, products: list):
        self.search_panel.set_research_state(False)
        self.chat_panel.set_input_enabled(True)
        self.statusBar().showMessage(f"Complete! Found {len(products)} products")
        
        # Agent summary
        self.chat_panel.add_agent_message(
            f"✅ Research complete! Found {len(products)} products. "
            f"Check the results panel for details."
        )
        
        self.calculate_profit_analysis()
        
        QMessageBox.information(
            self,
            "Research Complete",
            f"Successfully researched {len(products)} products!\n\n"
            f"Results exported to outputs folder."
        )
    
    def on_error(self, error_msg: str):
        self.progress_panel.append_log(f"\n❌ Error: {error_msg}")
        self.search_panel.set_research_state(False)
        self.chat_panel.set_input_enabled(True)
        self.statusBar().showMessage("Error occurred")
        
        # Notify in chat
        self.chat_panel.add_agent_message(
            f"❌ An error occurred: {error_msg[:100]}... Check the progress log for details."
        )
        
        if "Traceback" not in error_msg:
            QMessageBox.critical(self, "Error", f"An error occurred:\n\n{error_msg}")
    
    def stop_research(self):
        if self.worker and self.worker.isRunning():
            self.worker.stop()
            self.worker.terminate()
            self.worker.wait()
            self.progress_panel.append_log("\n❌ Research stopped by user")
            self.search_panel.set_research_state(False)
            self.chat_panel.set_input_enabled(True)
            self.statusBar().showMessage("Stopped")
            
            self.chat_panel.add_agent_message("Research stopped. Ready for new commands.")
    
    def update_analysis(self):
        if not self.results_data:
            return
        
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
        
        sorted_results = sorted(
            [r for r in self.results_data if r.get('margin', 0) > 0],
            key=lambda x: x.get('margin', 0),
            reverse=True
        )
        self.analysis_panel.update_opportunities(sorted_results[:3])
    
    def calculate_profit_analysis(self):
        self.update_analysis()
    
    def closeEvent(self, event):
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
