from dataclasses import dataclass, asdict
from typing import Optional
from datetime import datetime

@dataclass
class ProductInfo:
    """Product information data model"""
    source: str  # 'alibaba' or 'amazon'
    title: str
    price: str
    url: Optional[str] = None
    
    # Alibaba specific
    moq: Optional[str] = None
    seller_name: Optional[str] = None
    seller_years: Optional[str] = None
    
    # Additional info
    category: Optional[str] = None
    description: Optional[str] = None
    
    # Metadata
    scraped_at: str = None
    
    def __post_init__(self):
        if self.scraped_at is None:
            self.scraped_at = datetime.now().isoformat()
    
    def to_dict(self):
        """Convert to dictionary"""
        return asdict(self)

@dataclass
class SearchCriteria:
    """Search parameters"""
    search_term: str
    min_moq: int = 100
    min_seller_years: int = 2
    max_results: int = 10
    
    def __str__(self):
        return f"SearchCriteria(term='{self.search_term}', moq>={self.min_moq})"
