import json
import re
from typing import Dict, Any, List
from src.llm_client import LLMClient

class ReasoningAgent:
    """Agent that uses local LLM for decision-making"""
    
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client
        self.decision_history = []
    
    def plan_research(self, search_term: str) -> Dict[str, Any]:
        """Create a research plan using LLM"""
        prompt = f"""Create a research plan for: "{search_term}"

Available tools:
- alibaba_scraper: Search Alibaba for wholesale
- amazon_scraper: Search Amazon for retail

Respond in JSON:
{{
    "goal": "research objective",
    "steps": [
        {{"action": "tool_name", "reason": "why"}},
        ...
    ]
}}"""
        
        response = self.llm.query(prompt, 
                                 system="You are a research planner. Always respond with valid JSON.",
                                 temperature=0.3,
                                 max_tokens=500)
        
        try:
            plan = self._parse_json(response)
            self.decision_history.append({"type": "plan", "data": plan})
            return plan
        except Exception as e:
            print(f"❌ Plan parsing failed: {e}")
            return {
                "goal": f"Research {search_term}",
                "steps": [
                    {"action": "alibaba_scraper", "reason": "Find wholesale"},
                    {"action": "amazon_scraper", "reason": "Find retail"}
                ]
            }
    
    def analyze_results(self, alibaba_count: int, amazon_count: int, search_term: str) -> str:
        """Generate insights"""
        prompt = f"""Analyze these results:

Search: {search_term}
Alibaba: {alibaba_count} products
Amazon: {amazon_count} products

Provide 2-3 sentence analysis with one key insight."""
        
        response = self.llm.query(prompt,
                                 system="You are a product analyst. Be concise.",
                                 temperature=0.7,
                                 max_tokens=200)
        
        self.decision_history.append({"type": "analysis", "data": {"summary": response}})
        return response
    
    def _parse_json(self, response: str) -> Dict[str, Any]:
        """Extract JSON from response"""
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        return json.loads(response)
