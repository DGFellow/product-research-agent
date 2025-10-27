# 🤖 Product Research Agent

An AI-powered web agent that autonomously researches products across Alibaba and Amazon using a **local LLM** (zero API costs) for intelligent reasoning and decision-making.

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

- 🧠 **Local AI Reasoning** - Uses your own LLM via Flask API (zero API costs)
- 🌐 **Multi-Platform Scraping** - Alibaba and Amazon simultaneously
- 🛠️ **Tool-Based Architecture** - Modular, extensible design
- 📊 **Smart Analysis** - Automated comparative reports with matplotlib
- 🎯 **AI Planning** - LLM creates research strategy
- 💡 **Real-Time Insights** - AI-generated analysis and recommendations
- 🖥️ **Visual Feedback** - Optional GUI to watch LLM thinking

## 🏗️ Architecture

```
Product Research Agent
│
├── Reasoning Agent (AI Planning & Analysis)
│   └── Local LLM (Flask API)
│
├── Tools
│   ├── Web Navigator
│   ├── Alibaba Scraper
│   └── Amazon Scraper
│
└── Analyzer (Data + Visualizations)
```

**Key Innovation:** Integrates `local-llm` repository as a Git submodule, demonstrating:
- Clean separation of concerns
- Code reuse across projects
- Professional project architecture

## 🚀 Quick Start

### 1. Clone with Submodules
```bash
git clone --recurse-submodules https://github.com/DGFellow/product-research-agent.git
cd product-research-agent

# If you forgot --recurse-submodules:
git submodule update --init --recursive
```

### 2. Setup Environment
```bash
# Run setup script
./setup.sh  # Linux/Mac
# OR
setup.bat   # Windows

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate  # Windows
```

### 3. Setup local-llm
```bash
cd local-llm
pip install -r requirements.txt
cd ..
```

### 4. Start Local LLM

**Terminal 1 - API Only:**
```bash
./scripts/start_llm.sh
# Wait for: "✅ Server Running! 📍 URL: http://localhost:5000"
```

**OR Terminal 1 - API + GUI (see LLM activity):**
```bash
./scripts/start_llm_with_gui.sh
# Opens GUI window + starts API
```

### 5. Run Research Agent

**Terminal 2:**
```bash
source venv/bin/activate

# Interactive mode
python main.py

# Direct search
python main.py "wireless earbuds"

# Headless mode (no browser window)
python main.py "bluetooth speakers" --headless

# More products per site
python main.py "laptop stand" --max-products 20
```

## 📖 Usage Example

```bash
$ python main.py "coffee maker"

🤖 Connecting to local LLM...
✅ LLM connected

🚀 Initializing browser...
✅ Browser ready

============================================================
🔬 Researching: coffee maker
============================================================

🧠 Phase 1: AI Planning
   Goal: Compare coffee makers across wholesale and retail platforms
   Steps: 2 actions

📍 Phase 2: Data Collection
🔍 [alibaba_scraper] Searching for: coffee maker
📦 [alibaba_scraper]   → Espresso Coffee Maker Machine...
✅ [alibaba_scraper] Found 10 products

🔍 [amazon_scraper] Searching for: coffee maker
📦 [amazon_scraper]   → Keurig K-Elite Coffee Maker...
✅ [amazon_scraper] Found 10 products

🧠 Phase 3: AI Analysis

💡 Insights:
Strong availability across both platforms with 10 products each. 
Alibaba offers wholesale options for bulk purchasing, while Amazon 
provides diverse retail choices for immediate consumer needs.

============================================================
📊 Generating Analysis...
============================================================

✅ Exported to outputs/product_research.csv
✅ Saved visualization to outputs/product_analysis.png

📊 Summary:
  Total: 20 products
  By source: {'alibaba': 10, 'amazon': 10}
  Avg price: $67.45
  Range: $19.99 - $299.00

📁 Files:
   📄 outputs/product_research.csv
   📊 outputs/product_analysis.png
```

## 📊 Output Files

### CSV Report (`product_research.csv`)
- Complete product listings
- Prices, URLs, seller info
- Timestamps for all records
- Ready for Excel/Sheets

### Visualization (`product_analysis.png`)
- Price distribution by platform
- Product count comparison
- Average price analysis
- Top 10 products ranking

## 🔧 Configuration

Create `.env` file (copy from `.env.example`):

```env
# LLM Configuration
LLM_BASE_URL=http://localhost:5000

# Browser Configuration
HEADLESS=false

# Scraping Configuration
MAX_PRODUCTS_PER_SITE=10
MIN_MOQ=100
MIN_SELLER_YEARS=2
```

## 🛠️ Project Structure

```
product-research-agent/
├── src/
│   ├── agents/              # AI reasoning & orchestration
│   │   ├── reasoning_agent.py
│   │   └── product_agent.py
│   ├── analysis/            # Data analysis & viz
│   │   └── analyzer.py
│   ├── config.py            # Configuration
│   ├── llm_client.py        # LLM API client
│   └── models.py            # Data models
├── tools/                   # Modular tools
│   ├── base_tool.py
│   ├── web_navigator.py
│   ├── alibaba_tool.py
│   └── amazon_tool.py
├── local-llm/               # Git submodule
│   ├── src/                 # Original LLM code
│   ├── api_server.py        # Flask API wrapper
│   └── start_both.py        # API + GUI launcher
├── scripts/                 # Helper scripts
├── outputs/                 # Generated reports
├── main.py                  # CLI entry point
└── requirements.txt
```

## 🤝 Git Submodule Workflow

### Updating local-llm Submodule

```bash
# Pull latest changes from local-llm
cd local-llm
git pull origin main

# Return to main project
cd ..

# Commit the updated submodule reference
git add local-llm
git commit -m "chore: update local-llm submodule"
git push
```

### If Someone Clones Your Project

```bash
git clone --recurse-submodules https://github.com/DGFellow/product-research-agent.git
cd product-research-agent

# Setup
./setup.sh
cd local-llm && pip install -r requirements.txt && cd ..

# Run
./scripts/start_llm.sh  # Terminal 1
python main.py "search term"  # Terminal 2
```

## 💡 How It Works

### 1. AI Planning Phase
- Agent sends search term to local LLM
- LLM creates research strategy
- Determines which tools to use

### 2. Tool Execution Phase
- Web Navigator opens Playwright browser
- Alibaba tool scrapes wholesale products
- Amazon tool scrapes retail products
- Data collected into ProductInfo objects

### 3. AI Analysis Phase
- LLM analyzes collected data
- Generates insights and recommendations
- Creates summary report

### 4. Data Export Phase
- Pandas processes products
- Creates CSV with complete data
- Generates matplotlib visualizations

## 🐛 Troubleshooting

**LLM Not Available**
```bash
# Check if API is running
curl http://localhost:5000/health

# Should return: {"status": "ok", "ready": true}

# If not, start it:
cd local-llm
python api_server.py
```

**Browser Errors**
```bash
# Reinstall Playwright browsers
python -m playwright install chromium
```

**Submodule Issues**
```bash
# Re-initialize submodules
git submodule deinit -f local-llm
git submodule update --init --recursive
```

**Import Errors**
```bash
# Make sure you're in the right environment
source venv/bin/activate
pip install -r requirements.txt
```

## 📈 Performance Tips

1. **Use Headless Mode** for faster scraping:
   ```bash
   python main.py "product" --headless
   ```

2. **Adjust Product Limits** for speed:
   ```bash
   python main.py "product" --max-products 5
   ```

3. **Model Selection** - In `local-llm/.env`:
   ```env
   MODEL_ID=Qwen/Qwen2.5-3B-Instruct  # Faster
   ```

4. **Precision Settings** for GPU memory:
   ```env
   PRECISION=int4  # Least memory
   PRECISION=fp16  # Medium
   PRECISION=auto  # Best quality
   ```

## 🌟 Key Features for Portfolio

This project demonstrates:

✅ **Git Submodules** - Professional code organization  
✅ **API Design** - Flask wrapper around ML models  
✅ **Agent Architecture** - Tool-based AI agents  
✅ **Web Scraping** - Playwright automation  
✅ **Data Analysis** - Pandas + Matplotlib  
✅ **LLM Integration** - Local model deployment  
✅ **Async Programming** - Python asyncio  
✅ **Modular Design** - Clean, extensible code

## 🎓 Learning Resources

- [Playwright Docs](https://playwright.dev/python/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Git Submodules Tutorial](https://git-scm.com/book/en/v2/Git-Tools-Submodules)
- [Smolagents Framework](https://huggingface.co/docs/smolagents)

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📝 License

MIT License - see [LICENSE](LICENSE) file

## 🙏 Acknowledgments

- HuggingFace Transformers for local LLM capabilities
- Playwright team for excellent browser automation
- Inspired by Smolagents tool-based architecture

## 📬 Contact

GitHub: [@DGFellow](https://github.com/DGFellow)  
Project: [product-research-agent](https://github.com/DGFellow/product-research-agent)

---

**Built with ❤️ using local AI - No API costs, full control!**
