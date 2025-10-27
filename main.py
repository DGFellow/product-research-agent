import asyncio
import argparse
from src.llm_client import LLMClient
from src.agents.product_agent import ProductResearchAgent
from src.analysis.analyzer import ProductAnalyzer
from src.config import Config

def parse_args():
    parser = argparse.ArgumentParser(description="AI product research agent")
    parser.add_argument("search_term", nargs="?", help="Product to research")
    parser.add_argument("--headless", action="store_true", help="Headless mode")
    parser.add_argument("--max-products", type=int, default=10, help="Max products per site")
    return parser.parse_args()

async def main():
    args = parse_args()
    
    search_term = args.search_term
    if not search_term:
        search_term = input("🔍 Enter product to research: ").strip()
        if not search_term:
            print("❌ Search term required")
            return
    
    if args.headless:
        Config.HEADLESS = True
    if args.max_products:
        Config.MAX_PRODUCTS_PER_SITE = args.max_products
    
    print("\n🤖 Connecting to local LLM...")
    llm = LLMClient()
    
    if not llm.is_available():
        print("⚠️  Warning: LLM not available at", Config.LLM_BASE_URL)
        print("   Start it with: cd local-llm && python api_server.py")
        print("   Continuing with basic functionality...\n")
    else:
        print("✅ LLM connected\n")
    
    agent = ProductResearchAgent(llm)
    
    try:
        await agent.initialize()
        products = await agent.research_product(search_term)
        
        if not products:
            print("\n⚠️  No products found")
            return
        
        print(f"\n{'='*60}")
        print("📊 Generating Analysis...")
        print(f"{'='*60}\n")
        
        analyzer = ProductAnalyzer(products)
        analyzer.export_csv()
        analyzer.create_visualizations()
        
        stats = analyzer.get_summary_stats()
        print(f"\n{'='*60}")
        print("✅ Research Complete!")
        print(f"{'='*60}")
        print(f"\n📊 Summary:")
        print(f"  Total: {stats['total_products']} products")
        if 'by_source' in stats:
            print(f"  By source: {stats['by_source']}")
        if stats.get('price_stats'):
            ps = stats['price_stats']
            print(f"  Avg price: ${ps['mean']:.2f}")
            print(f"  Range: ${ps['min']:.2f} - ${ps['max']:.2f}")
        
        print(f"\n📁 Files:")
        print(f"   📄 {Config.OUTPUT_DIR}/product_research.csv")
        print(f"   📊 {Config.OUTPUT_DIR}/product_analysis.png\n")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await agent.close()

if __name__ == "__main__":
    asyncio.run(main())
