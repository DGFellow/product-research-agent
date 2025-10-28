from typing import List, Dict, Any
from playwright.async_api import Page
from tools.base_tool import BaseTool
from tools.web_navigator import WebNavigatorTool
from src.models import ProductInfo, SearchCriteria
import asyncio

class AmazonScraperTool(BaseTool):
    BASE_URL = "https://www.amazon.com"
    
    def __init__(self, page: Page):
        super().__init__(name="amazon_scraper", description="Search Amazon")
        self.page = page
        self.navigator = WebNavigatorTool(page)
    
    async def execute(self, criteria: SearchCriteria) -> Dict[str, Any]:
        self.log(f"Searching for: {criteria.search_term}", "🔍")
        
        try:
            self.log("  ├─ Building search URL...", "")
            search_url = f"{self.BASE_URL}/s?k={criteria.search_term.replace(' ', '+')}"
            
            self.log("  ├─ Navigating to Amazon...", "")
            await self.page.goto(search_url, timeout=60000)
            
            self.log("  ├─ Waiting for page load...", "")
            await asyncio.sleep(3)
            
            self.log("  ├─ Looking for search results...", "")
            await self.page.wait_for_selector('[data-component-type="s-search-result"]', timeout=15000)
            
            self.log("  ├─ Extracting product data...", "")
            products = await self._extract_products(criteria.max_results)
            
            self.log(f"  └─ ✅ Found {len(products)} products", "")
            return {"success": True, "products": products, "count": len(products)}
            
        except Exception as e:
            self.log(f"  └─ ❌ Search failed: {e}", "")
            return {"success": False, "error": str(e), "products": []}
    
    async def _extract_products(self, max_results: int) -> List[ProductInfo]:
        products = []
        product_cards = await self.page.query_selector_all('[data-component-type="s-search-result"]')
        
        for i, card in enumerate(product_cards[:max_results]):
            try:
                # Multiple title selectors (Amazon uses different ones)
                title_selectors = [
                    'h2 a span',
                    'h2 span',
                    '.a-size-medium',
                    '.a-size-base-plus'
                ]
                
                title = None
                for selector in title_selectors:
                    title_elem = await card.query_selector(selector)
                    if title_elem:
                        title = await title_elem.inner_text()
                        if title and title.strip():
                            break
                
                if not title or not title.strip():
                    continue  # Skip if no title found
                
                # Multiple price selectors
                price_selectors = [
                    '.a-price .a-offscreen',
                    '.a-price-whole',
                    '.a-price span',
                ]
                
                price = "N/A"
                for selector in price_selectors:
                    price_elem = await card.query_selector(selector)
                    if price_elem:
                        price_text = await price_elem.inner_text()
                        if price_text and price_text.strip():
                            price = price_text.strip()
                            break
                
                # URL
                link_elem = await card.query_selector('h2 a')
                url = await link_elem.get_attribute('href') if link_elem else None
                if url and not url.startswith('http'):
                    url = f"{self.BASE_URL}{url}"
                
                product = ProductInfo(
                    source='amazon',
                    title=title.strip(),
                    price=price,
                    url=url
                )
                products.append(product)
                self.log(f"  → {title[:50]}...", "📦")
                
            except Exception as e:
                self.log(f"  → Error extracting product {i}: {e}", "⚠️")
                continue
        
        return products