from playwright.async_api import async_playwright, Browser, Page
from typing import List, Optional
from src.llm_client import LLMClient
from src.agents.reasoning_agent import ReasoningAgent
from tools.alibaba_tool import AlibabaScraperTool
from tools.amazon_tool import AmazonScraperTool
from src.models import ProductInfo, SearchCriteria
from src.config import Config

class ProductResearchAgent:
    """Main orchestrator"""
    
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client
        self.reasoning_agent = ReasoningAgent(llm_client)
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        self.products: List[ProductInfo] = []
        self.config = Config()
    
    async def initialize(self):
        """Initialize browser"""
        print("🚀 Initializing browser...")
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(headless=self.config.HEADLESS)
        self.page = await self.browser.new_page()
        await self.page.set_viewport_size({
            "width": self.config.VIEWPORT_WIDTH,
            "height": self.config.VIEWPORT_HEIGHT
        })
        print("✅ Browser ready")
    
    async def close(self):
        """Close browser"""
        if self.browser:
            await self.browser.close()
            print("👋 Browser closed")
    
    async def research_product(self, search_term: str) -> List[ProductInfo]:
        """Main research workflow"""
        print(f"\n{'='*60}")
        print(f"🔬 Researching: {search_term}")
        print(f"{'='*60}\n")
        
        criteria = SearchCriteria(
            search_term=search_term,
            min_moq=self.config.MIN_MOQ,
            min_seller_years=self.config.MIN_SELLER_YEARS,
            max_results=self.config.MAX_PRODUCTS_PER_SITE
        )
        
        # Phase 1: AI Planning
        print("🧠 Phase 1: AI Planning")
        plan = self.reasoning_agent.plan_research(search_term)
        print(f"   Goal: {plan.get('goal', 'Research products')}")
        print(f"   Steps: {len(plan.get('steps', []))} actions\n")
        
        # Phase 2: Execute
        print("📍 Phase 2: Data Collection")
        
        alibaba_tool = AlibabaScraperTool(self.page)
        alibaba_result = await alibaba_tool.execute(criteria)
        alibaba_products = alibaba_result.get('products', [])
        self.products.extend(alibaba_products)
        
        print()
        amazon_tool = AmazonScraperTool(self.page)
        amazon_result = await amazon_tool.execute(criteria)
        amazon_products = amazon_result.get('products', [])
        self.products.extend(amazon_products)
        
        # Phase 3: AI Analysis
        print(f"\n🧠 Phase 3: AI Analysis")
        if self.products:
            analysis = self.reasoning_agent.analyze_results(
                len(alibaba_products),
                len(amazon_products),
                search_term
            )
            print(f"\n💡 Insights:\n{analysis}\n")
        
        return self.products
