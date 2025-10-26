from typing import List, Dict, Any
from playwright.async_api import Page
from tools.base_tool import BaseTool
from tools.web_navigator import WebNavigatorTool
from src.models import ProductInfo, SearchCriteria

class AmazonScraperTool(BaseTool):
    """Tool for scraping Amazon"""
    
    BASE_URL = "https://www.amazon.com"
    
    def __init__(self, page: Page):
        super().__init__(
            name="amazon_scraper",
            description="Search Amazon for products"
        )
        self.page = page
        self.navigator = WebNavigatorTool(page)
    
    async def execute(self, criteria: SearchCriteria) -> Dict[str, Any]:
        """Search Amazon"""
        self.log(f"Searching for: {criteria.search_term}", "🔍")
        
        try:
            search_url = f"{self.BASE_URL}/s?k={criteria.search_term.replace(' ', '+')}"
            await self.navigator.execute("goto", url=search_url)
            await self.navigator.execute("wait", 
                                        selector='[data-component-type="s-search-result"]',
                                        timeout=10000)
            
            products = await self._extract_products(criteria.max_results)
            
            self.log(f"Found {len(products)} products", "✅")
            return {"success": True, "products": products, "count": len(products)}
            
        except Exception as e:
            self.log(f"Search failed: {e}", "❌")
            return {"success": False, "error": str(e), "products": []}
    
    async def _extract_products(self, max_results: int) -> List[ProductInfo]:
        """Extract product information"""
        products = []
        product_cards = await self.page.query_selector_all('[data-component-type="s-search-result"]')
        
        for i, card in enumerate(product_cards[:max_results]):
            try:
                product = await self._extract_product_card(card)
                if product:
                    products.append(product)
                    self.log(f"  → {product.title[:50]}...", "📦")
            except Exception as e:
                self.log(f"  → Error extracting product {i}: {e}", "⚠️")
                continue
        
        return products
    
    async def _extract_product_card(self, card) -> ProductInfo:
        """Extract info from card"""
        title_elem = await card.query_selector('h2 a span')
        title = await title_elem.inner_text() if title_elem else "N/A"
        
        price_elem = await card.query_selector('.a-price-whole')
        price = await price_elem.inner_text() if price_elem else "N/A"
        if price != "N/A":
            price = f"${price.strip()}"
        
        link_elem = await card.query_selector('h2 a')
        url = await link_elem.get_attribute('href') if link_elem else None
        if url and not url.startswith('http'):
            url = f"{self.BASE_URL}{url}"
        
        return ProductInfo(
            source='amazon',
            title=title.strip(),
            price=price,
            url=url
        )
