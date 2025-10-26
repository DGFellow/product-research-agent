import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
from typing import List
from src.models import ProductInfo
from src.config import Config

class ProductAnalyzer:
    """Analyze and visualize product data"""
    
    def __init__(self, products: List[ProductInfo]):
        self.products = products
        self.df = self._create_dataframe()
        
    def _create_dataframe(self) -> pd.DataFrame:
        """Convert to DataFrame"""
        if not self.products:
            return pd.DataFrame()
        
        data = [p.to_dict() for p in self.products]
        df = pd.DataFrame(data)
        df['price_numeric'] = df['price'].apply(self._extract_price)
        return df
    
    @staticmethod
    def _extract_price(price_str) -> float:
        """Extract numeric price"""
        if pd.isna(price_str) or price_str == "N/A":
            return None
        match = re.search(r'[\d,]+\.?\d*', str(price_str))
        if match:
            return float(match.group().replace(',', ''))
        return None
    
    def export_csv(self, filename: str = "product_research.csv"):
        """Export to CSV"""
        if self.df.empty:
            print("⚠️  No data to export")
            return None
        
        output_path = Config.OUTPUT_DIR / filename
        self.df.to_csv(output_path, index=False)
        print(f"✅ Exported to {output_path}")
        return output_path
    
    def create_visualizations(self, filename: str = "product_analysis.png"):
        """Create visualizations"""
        if self.df.empty:
            print("⚠️  No data to visualize")
            return None
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Product Research Analysis', fontsize=16, fontweight='bold')
        sns.set_style("whitegrid")
        
        valid_prices = self.df[self.df['price_numeric'].notna()]
        
        # 1. Price distribution
        if not valid_prices.empty and len(valid_prices['source'].unique()) > 1:
            valid_prices.boxplot(column='price_numeric', by='source', ax=axes[0, 0])
            axes[0, 0].set_title('Price Distribution')
            axes[0, 0].set_ylabel('Price ($)')
        else:
            axes[0, 0].text(0.5, 0.5, 'Insufficient data', 
                           ha='center', va='center', transform=axes[0, 0].transAxes)
        
        # 2. Product counts
        source_counts = self.df['source'].value_counts()
        colors = ['#ff9900' if s == 'alibaba' else '#00a8e1' for s in source_counts.index]
        axes[0, 1].bar(source_counts.index, source_counts.values, color=colors)
        axes[0, 1].set_title('Products Found')
        axes[0, 1].set_ylabel('Count')
        
        # 3. Average prices
        if not valid_prices.empty:
            avg_prices = valid_prices.groupby('source')['price_numeric'].mean()
            colors = ['#ff9900' if s == 'alibaba' else '#00a8e1' for s in avg_prices.index]
            axes[1, 0].bar(avg_prices.index, avg_prices.values, color=colors)
            axes[1, 0].set_title('Average Price')
            axes[1, 0].set_ylabel('Price ($)')
            for i, (idx, val) in enumerate(avg_prices.items()):
                axes[1, 0].text(i, val, f'${val:.2f}', ha='center', va='bottom')
        
        # 4. Top products
        if not valid_prices.empty:
            top = valid_prices.nlargest(min(10, len(valid_prices)), 'price_numeric')
            colors = ['#ff9900' if s == 'alibaba' else '#00a8e1' for s in top['source']]
            axes[1, 1].barh(range(len(top)), top['price_numeric'], color=colors)
            axes[1, 1].set_yticks(range(len(top)))
            axes[1, 1].set_yticklabels([t[:30]+'...' if len(t)>30 else t for t in top['title']], fontsize=8)
            axes[1, 1].set_title(f'Top {len(top)} Products')
            axes[1, 1].set_xlabel('Price ($)')
            axes[1, 1].invert_yaxis()
        
        plt.tight_layout()
        output_path = Config.OUTPUT_DIR / filename
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"✅ Saved visualization to {output_path}")
        plt.close()
        return output_path
    
    def get_summary_stats(self) -> dict:
        """Get summary statistics"""
        if self.df.empty:
            return {"total_products": 0}
        
        valid_prices = self.df[self.df['price_numeric'].notna()]
        stats = {
            "total_products": len(self.df),
            "by_source": self.df['source'].value_counts().to_dict(),
            "price_stats": {}
        }
        
        if not valid_prices.empty:
            stats["price_stats"] = {
                "mean": valid_prices['price_numeric'].mean(),
                "median": valid_prices['price_numeric'].median(),
                "min": valid_prices['price_numeric'].min(),
                "max": valid_prices['price_numeric'].max(),
            }
        
        return stats
