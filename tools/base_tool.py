from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseTool(ABC):
    """Abstract base class for agent tools"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    @abstractmethod
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute the tool"""
        pass
    
    def log(self, message: str, emoji: str = "ℹ️"):
        """Consistent logging"""
        print(f"{emoji} [{self.name}] {message}")
    
    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}')"
