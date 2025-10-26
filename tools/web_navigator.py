from playwright.async_api import Page
import asyncio
from tools.base_tool import BaseTool
from typing import Dict, Any
from src.config import Config

class WebNavigatorTool(BaseTool):
    """Tool for navigating web pages"""
    
    def __init__(self, page: Page):
        super().__init__(
            name="web_navigator",
            description="Navigate to URLs and interact with web pages"
        )
        self.page = page
        self.config = Config()
    
    async def execute(self, action: str, **kwargs) -> Dict[str, Any]:
        """Execute navigation action"""
        try:
            if action == "goto":
                url = kwargs.get('url')
                self.log(f"Navigating to {url}", "🌐")
                await self.page.goto(url)
                await self.page.wait_for_load_state('networkidle')
                await asyncio.sleep(self.config.REQUEST_DELAY)
                return {"success": True, "url": self.page.url}
                
            elif action == "wait":
                selector = kwargs.get('selector')
                timeout = kwargs.get('timeout', 10000)
                await self.page.wait_for_selector(selector, timeout=timeout)
                return {"success": True}
                
            elif action == "get_content":
                title = await self.page.title()
                url = self.page.url
                return {"success": True, "title": title, "url": url}
            
            return {"success": False, "error": f"Unknown action: {action}"}
                
        except Exception as e:
            self.log(f"Error: {e}", "❌")
            return {"success": False, "error": str(e)}
