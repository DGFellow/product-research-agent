import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Project paths
    PROJECT_ROOT = Path(__file__).parent.parent
    DATA_DIR = PROJECT_ROOT / "data"
    OUTPUT_DIR = PROJECT_ROOT / "outputs"
    
    # LLM settings
    LLM_BASE_URL = os.getenv("LLM_BASE_URL", "http://localhost:5000")
    LLM_TIMEOUT = 60  # seconds
    
    # Browser settings
    HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
    VIEWPORT_WIDTH = 1920
    VIEWPORT_HEIGHT = 1080
    
    # Scraping settings
    MAX_PRODUCTS_PER_SITE = int(os.getenv("MAX_PRODUCTS_PER_SITE", "10"))
    REQUEST_DELAY = 2  # seconds between requests
    
    # Search criteria defaults
    MIN_MOQ = int(os.getenv("MIN_MOQ", "100"))
    MIN_SELLER_YEARS = int(os.getenv("MIN_SELLER_YEARS", "2"))

# Create directories
Config.DATA_DIR.mkdir(exist_ok=True)
Config.OUTPUT_DIR.mkdir(exist_ok=True)