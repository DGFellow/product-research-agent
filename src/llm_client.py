import requests
import json
from typing import Optional
from src.config import Config

class LLMClient:
    """Client for interacting with local-llm Flask API"""
    
    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url or Config.LLM_BASE_URL
        self.timeout = Config.LLM_TIMEOUT
        
    def query(self, 
              prompt: str, 
              system: str = "",
              temperature: float = 0.7,
              max_tokens: int = 500) -> str:
        """Query the local LLM via Flask API"""
        try:
            messages = []
            if system:
                messages.append({"role": "system", "content": system})
            messages.append({"role": "user", "content": prompt})
            
            response = requests.post(
                f"{self.base_url}/v1/chat/completions",
                json={
                    "messages": messages,
                    "temperature": temperature,
                    "max_tokens": max_tokens
                },
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content']
            
        except requests.exceptions.RequestException as e:
            print(f"❌ LLM request failed: {e}")
            return ""
        except (KeyError, json.JSONDecodeError) as e:
            print(f"❌ LLM response parsing failed: {e}")
            return ""
    
    def is_available(self) -> bool:
        """Check if LLM service is available"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            return response.status_code == 200
        except:
            return False