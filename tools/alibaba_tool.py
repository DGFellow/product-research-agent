from typing import List, Dict, Any
from playwright.async_api import Page
from tools.base_tool import BaseTool
from tools.web_navigator import WebNavigatorTool
from src.models import ProductInfo, SearchCriteria
import asyncio

class AlibabaScraperTool(BaseTool):
    BASE_URL = "https://www.alibaba.com"
    
    def __init__(self, page: Page):
        super().__init__(name="alibaba_scraper", description="Search Alibaba")
        self.page = page
        self.navigator = WebNavigatorTool(page)
    
    async def execute(self, criteria: SearchCriteria) -> Dict[str, Any]:
        self.log(f"Searching for: {criteria.search_term}", "🔍")
        
        try:
            # Add detailed logging
            self.log("  ├─ Setting up request headers...", "")
            
            await self.page.set_extra_http_headers({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept-Language': 'en-US,en;q=0.9',
            })
            
            search_url = f"{self.BASE_URL}/trade/search?SearchText={criteria.search_term.replace(' ', '+')}"
            
            self.log("  ├─ Navigating to Alibaba search...", "")
            await self.page.goto(search_url, timeout=60000)
            
            self.log("  ├─ Waiting for page to load...", "")
            await asyncio.sleep(5)
            
            self.log("  ├─ Looking for product listings...", "")
            
            # Try multiple selectors
            selectors = [
                '.organic-list-offer',
                '[class*="search-card"]',
                '[class*="product-card"]',
                '.gallery-offer-card'
            ]
            
            products = []
            for selector in selectors:
                try:
                    self.log(f"    ├─ Trying selector: {selector}", "")
                    await self.page.wait_for_selector(selector, timeout=10000)
                    products = await self._extract_products(selector, criteria.max_results)
                    if products:
                        self.log(f"    └─ ✅ Found products with selector!", "")
                        break
                except:
                    self.log(f"    ├─ Selector failed, trying next...", "")
                    continue
            
            if not products:
                self.log("  └─ ⚠️  No products found - may be blocked", "")
            else:
                self.log(f"  └─ ✅ Extracted {len(products)} products", "")
            
            return {"success": True, "products": products, "count": len(products)}
            
        except Exception as e:
            self.log(f"  └─ ❌ Search failed: {e}", "")
            return {"success": False, "error": str(e), "products": []}
    
    async def _extract_products(self, selector: str, max_results: int) -> List[ProductInfo]:
        products = []
        product_cards = await self.page.query_selector_all(selector)
        
        for i, card in enumerate(product_cards[:max_results]):
            try:
                # Get all text content from card
                text_content = await card.inner_text()
                
                # Try to extract title
                title_selectors = [
                    '.organic-list-offer-title',
                    '[class*="title"]',
                    'h2',
                    'h3'
                ]
                
                title = "N/A"
                for t_sel in title_selectors:
                    title_elem = await card.query_selector(t_sel)
                    if title_elem:
                        title = await title_elem.inner_text()
                        break
                
                # Try to extract price
                price_selectors = [
                    '.organic-list-offer-price',
                    '[class*="price"]',
                    '.price-original'
                ]
                
                price = "N/A"
                for p_sel in price_selectors:
                    price_elem = await card.query_selector(p_sel)
                    if price_elem:
                        price = await price_elem.inner_text()
                        break
                
                # URL
                link_elem = await card.query_selector('a')
                url = await link_elem.get_attribute('href') if link_elem else None
                if url and not url.startswith('http'):
                    url = f"{self.BASE_URL}{url}"
                
                if title != "N/A":  # Only add if we got a title
                    product = ProductInfo(
                        source='alibaba',
                        title=title.strip(),
                        price=price.strip(),
                        url=url,
                        moq="Contact supplier",
                        seller_years="Unknown"
                    )
                    products.append(product)
                    self.log(f"  → {title[:50]}...", "📦")
                
            except Exception as e:
                self.log(f"  → Error extracting product {i}: {e}", "⚠️")
                continue
        
        return products