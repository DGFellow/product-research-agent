import requests
import json
from typing import Optional, Iterator
from src.config import Config

class LLMClient:
    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url or Config.LLM_BASE_URL
        self.timeout = Config.LLM_TIMEOUT
        
    def query(self, prompt: str, system: str = "", temperature: float = 0.7, max_tokens: int = 500) -> str:
        """Standard query (non-streaming)"""
        try:
            messages = []
            if system:
                messages.append({"role": "system", "content": system})
            messages.append({"role": "user", "content": prompt})
            
            response = requests.post(
                f"{self.base_url}/v1/chat/completions",
                json={"messages": messages, "temperature": temperature, "max_tokens": max_tokens},
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
    
    def query_stream(self, prompt: str, system: str = "", temperature: float = 0.7, max_tokens: int = 500) -> Iterator[str]:
        """Streaming query - yields tokens one by one"""
        try:
            messages = []
            if system:
                messages.append({"role": "system", "content": system})
            messages.append({"role": "user", "content": prompt})
            
            # Note: Your local-llm API needs to support streaming
            # For now, we'll simulate streaming by splitting the response
            response = requests.post(
                f"{self.base_url}/v1/chat/completions",
                json={"messages": messages, "temperature": temperature, "max_tokens": max_tokens},
                timeout=self.timeout
            )
            response.raise_for_status()
            full_response = response.json()['choices'][0]['message']['content']
            
            # Simulate streaming by yielding word by word
            words = full_response.split()
            for i, word in enumerate(words):
                if i == 0:
                    yield word
                else:
                    yield " " + word
            
        except Exception as e:
            yield f"Error: {str(e)}"
    
    def is_available(self) -> bool:
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            return response.status_code == 200
        except:
            return False