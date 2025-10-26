# Product Research Agent - Complete Setup Guide

## 🎯 Project Overview
Build a web-navigating AI agent that researches products on Alibaba and Amazon, then generates comparative analysis reports. This project demonstrates:
- AI agent architecture with local LLM reasoning
- Web scraping with Playwright
- Tool-based agent design (inspired by Smolagents)
- Git submodule integration (linking your local-llm project)
- Flask API wrapping for clean architecture
- Real-time GUI visualization of agent activity

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                 Product Research Agent                   │
│  ┌─────────────┐      ┌──────────────┐                 │
│  │   Reasoning │ HTTP │  Flask API   │                 │
│  │    Agent    │─────→│ (local:5000) │                 │
│  └─────────────┘      └──────────────┘                 │
│         │                     │                          │
│         ↓                     ↓                          │
│  ┌──────────────────────────────────┐                  │
│  │          Tools System             │                  │
│  │  • Web Navigator                  │                  │
│  │  • Alibaba Scraper                │                  │
│  │  • Amazon Scraper                 │                  │
│  └──────────────────────────────────┘                  │
└─────────────────────────────────────────────────────────┘
                         │
                         ↓
              ┌──────────────────────┐
              │   local-llm          │
              │   (Git Submodule)    │
              │                      │
              │  • LLM Engine        │
              │  • Flask API Server  │
              │  • PyQt6 GUI         │
              └──────────────────────┘
```

---

## 📋 Prerequisites
- Python 3.9+
- Git installed
- GitHub account
- CUDA-capable GPU (recommended) or CPU
- Internet connection (for web scraping)
- ~10GB disk space (for models)

---

## 🎓 Understanding Git Submodules (Important!)

### What is a Git Submodule?
A submodule lets you include one Git repository inside another. Think of it as a "smart link" to another project.

**Why use it?**
- ✅ Shows you understand modular architecture
- ✅ Keeps projects independent
- ✅ Demonstrates code reuse
- ✅ Professional portfolio piece

**Visual Example:**
```
product-research-agent/              ← Your NEW project (this guide)
├── src/
├── tools/
├── local-llm/                       ← Git submodule (links to existing repo)
│   ├── src/
│   │   ├── app.py                   ← Your existing LLM code
│   │   ├── llm/engine.py
│   │   └── ...
│   ├── api_server.py                ← We'll add this
│   └── requirements.txt
└── main.py

After adding submodule, local-llm/ acts like a folder but is actually 
a pointer to: https://github.com/DGFellow/local-llm
```

**How it works when someone clones your project:**
```bash
git clone https://github.com/DGFellow/product-research-agent.git
cd product-research-agent
git submodule update --init --recursive  ← Downloads local-llm automatically!
```

---

## 🏗️ Phase 1: Project Initialization

### Step 1.1: Create Project Structure
```bash
# Create main project directory
mkdir product-research-agent
cd product-research-agent

# Initialize git
git init

# Create directory structure
mkdir -p src/agents src/analysis tools tests scripts
touch README.md .gitignore requirements.txt
touch src/__init__.py src/agents/__init__.py src/analysis/__init__.py tools/__init__.py
```

### Step 1.2: Create .gitignore
```bash
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
*.egg-info/
dist/
build/

# IDE
.vscode/
.idea/
*.swp
*.pyc

# Data & outputs
*.csv
*.png
*.json
data/
outputs/

# Environment
.env

# OS
.DS_Store
Thumbs.db

# Playwright
playwright-state.json
EOF
```

### Step 1.3: Initial README.md
```bash
cat > README.md << 'EOF'
# Product Research Agent

An AI-powered web agent that researches products across Alibaba and Amazon, providing comparative analysis and insights using a local LLM.

## Features
- 🤖 Local AI reasoning (no API costs!)
- 🌐 Multi-platform product research
- 🛠️ Tool-based agent architecture
- 📊 Data visualization and reporting
- 🔗 Integrated with local-llm via Flask API

## Status
🚧 Under Development

## Architecture
- **Agent**: Orchestrates research workflow
- **Tools**: Modular web scraping tools
- **LLM**: Local transformer model (via submodule)
- **Analysis**: Pandas + Matplotlib reporting
EOF
```

### Step 1.4: First Commit
```bash
git add .
git commit -m "feat: initial project structure"
```

**✅ Checkpoint: You should have:**
- Empty project structure
- Git initialized
- First commit made

---

## 📦 Phase 2: Dependencies Setup

### Step 2.1: Create requirements.txt
```bash
cat > requirements.txt << 'EOF'
# Web automation
playwright==1.40.0

# Data processing
pandas==2.1.4
numpy==1.26.2

# Visualization
matplotlib==3.8.2
seaborn==0.13.0

# HTTP requests & API
requests==2.31.0
aiohttp==3.9.1
flask==3.0.0
flask-cors==4.0.0

# Utilities
python-dotenv==1.0.0
pydantic==2.5.3

# For local-llm integration (will be in submodule)
# PySide6==6.6.0  ← Don't add here, only in local-llm
EOF
```

### Step 2.2: Create setup script
```bash
cat > setup.sh << 'EOF'
#!/bin/bash
echo "🚀 Setting up Product Research Agent..."

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Upgrade pip
pip install --upgrade pip

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Install Playwright browsers
echo "🌐 Installing Playwright browsers..."
python -m playwright install chromium

# Create output directories
mkdir -p outputs data

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Add local-llm as submodule (see Phase 3)"
echo "  2. Activate environment: source venv/bin/activate"
echo "  3. Start building!"
EOF

chmod +x setup.sh
```

### Step 2.3: Create Windows setup script
```bash
cat > setup.bat << 'EOF'
@echo off
echo Starting Product Research Agent setup...

python -m venv venv
call venv\Scripts\activate

pip install --upgrade pip
pip install -r requirements.txt

python -m playwright install chromium

mkdir outputs
mkdir data

echo.
echo Setup complete!
echo.
echo Next steps:
echo   1. Add local-llm as submodule (see Phase 3)
echo   2. Activate environment: venv\Scripts\activate
echo   3. Start building!
pause
EOF
```

### Step 2.4: Run Setup
```bash
# Run the setup
./setup.sh  # or setup.bat on Windows

# Verify installation
source venv/bin/activate  # or venv\Scripts\activate on Windows
python -c "import playwright; print('Playwright OK')"
python -c "import pandas; print('Pandas OK')"
```

### Step 2.5: Commit
```bash
git add requirements.txt setup.sh setup.bat
git commit -m "feat: add dependencies and setup scripts"
```

**✅ Checkpoint: You should have:**
- Virtual environment created
- All dependencies installed
- Playwright browser downloaded

---

## 🔗 Phase 3: Integrate local-llm (Git Submodule)

### Step 3.1: Understanding What We'll Do
We're going to:
1. Add your existing `local-llm` repo as a submodule
2. This creates a link (not a copy) to your other project
3. Both projects stay independent
4. Shows professional project organization

### Step 3.2: Add local-llm as Submodule

**Important:** Make sure you're in the `product-research-agent/` directory!

```bash
# Check you're in the right place
pwd  # Should show: .../product-research-agent

# Add submodule (replace YOUR_USERNAME with your GitHub username)
git submodule add https://github.com/DGFellow/local-llm.git local-llm

# This will:
# - Clone your local-llm repo into local-llm/ folder
# - Create .gitmodules file
# - Track the specific commit of local-llm
```

**What just happened:**
```
product-research-agent/
├── local-llm/          ← NEW! Contains your entire local-llm project
│   ├── src/
│   │   ├── app.py
│   │   └── ...
│   └── README.md
└── .gitmodules         ← NEW! Records the submodule link
```

### Step 3.3: Verify Submodule
```bash
# Check submodule status
git submodule status

# You should see something like:
# a1b2c3d4... local-llm (heads/main)

# Verify files are there
ls local-llm/src/
# Should show: app.py, config.py, llm/, ui/, utils/
```

### Step 3.4: Commit Submodule
```bash
git add .gitmodules local-llm
git commit -m "feat: add local-llm as git submodule"
```

### Step 3.5: Understanding .gitmodules
```bash
# View the file
cat .gitmodules

# You'll see:
[submodule "local-llm"]
    path = local-llm
    url = https://github.com/DGFellow/local-llm.git

# This tells git: "local-llm/ is linked to that GitHub repo"
```

### Step 3.6: How Others Clone Your Project
When someone clones your project, they do:
```bash
git clone https://github.com/DGFellow/product-research-agent.git
cd product-research-agent

# Initialize submodules (downloads local-llm)
git submodule update --init --recursive

# Now they have both projects!
```

**✅ Checkpoint: You should have:**
- `local-llm/` folder with all your LLM code
- `.gitmodules` file created
- Submodule committed to git

---

## 🔌 Phase 4: Add Flask API to local-llm

Now we'll add an API server to your local-llm project so the agent can communicate with it.

### Step 4.1: Navigate to local-llm
```bash
cd local-llm
```

### Step 4.2: Update local-llm requirements
```bash
# Add to local-llm/requirements.txt
cat >> requirements.txt << 'EOF'

# API Server
flask==3.0.0
flask-cors==4.0.0
EOF
```

### Step 4.3: Create API Server
```bash
# Create api_server.py in local-llm root
cat > api_server.py << 'EOF'
"""
Flask API server for local LLM
Wraps the LLMEngine to provide HTTP endpoints
"""
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS

from src.llm.engine import LLMEngine
from src.config import Config

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
log = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# Global engine instance
engine = None
config = None

def initialize_engine():
    """Load the LLM model"""
    global engine, config
    log.info("🤖 Initializing LLM Engine...")
    config = Config()
    engine = LLMEngine(config)
    engine.load()
    log.info("✅ LLM Engine ready!")

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "ok",
        "model": config.model_id if config else "not loaded",
        "ready": engine is not None
    })

@app.route('/v1/chat/completions', methods=['POST'])
def chat_completions():
    """
    OpenAI-compatible chat completions endpoint
    Request format:
    {
        "messages": [
            {"role": "system", "content": "..."},
            {"role": "user", "content": "..."}
        ],
        "temperature": 0.7,
        "max_tokens": 500
    }
    """
    try:
        data = request.json
        messages = data.get('messages', [])
        temperature = data.get('temperature', config.temperature)
        max_tokens = data.get('max_tokens', config.max_new_tokens)
        
        # Extract system prompt and user message
        system_prompt = config.chat_system_prompt
        history = []
        user_msg = ""
        
        for msg in messages:
            role = msg.get('role')
            content = msg.get('content', '')
            
            if role == 'system':
                system_prompt = content
            elif role == 'user':
                user_msg = content
            elif role == 'assistant':
                # Add to history if there was a previous user message
                if user_msg:
                    history.append((user_msg, content))
                    user_msg = ""
        
        if not user_msg:
            return jsonify({"error": "No user message provided"}), 400
        
        # Generate response (non-streaming for simplicity)
        log.info(f"💬 Generating response for: {user_msg[:50]}...")
        response_text = ""
        for chunk in engine.generate_stream(
            system_prompt=system_prompt,
            history=history,
            user_msg=user_msg,
            max_new_tokens=max_tokens,
            temperature=temperature
        ):
            response_text += chunk
        
        log.info(f"✅ Response generated ({len(response_text)} chars)")
        
        # Return OpenAI-compatible format
        return jsonify({
            "choices": [{
                "message": {
                    "role": "assistant",
                    "content": response_text
                },
                "finish_reason": "stop"
            }],
            "model": config.model_id,
            "usage": {
                "prompt_tokens": 0,  # Not calculated
                "completion_tokens": 0,
                "total_tokens": 0
            }
        })
        
    except Exception as e:
        log.error(f"❌ Error: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

def main():
    """Run the Flask API server"""
    print("\n" + "="*60)
    print("🚀 Starting Local LLM API Server")
    print("="*60)
    
    initialize_engine()
    
    print("\n" + "="*60)
    print("✅ Server Running!")
    print("="*60)
    print(f"📍 URL: http://localhost:5000")
    print(f"🤖 Model: {config.model_id}")
    print(f"🔍 Health check: http://localhost:5000/health")
    print("\nPress Ctrl+C to stop\n")
    
    app.run(host='0.0.0.0', port=5000, debug=False)

if __name__ == '__main__':
    main()
EOF
```

### Step 4.4: Create Combined Launcher (API + GUI)
```bash
cat > start_both.py << 'EOF'
"""
Launch both Flask API server and PyQt6 GUI simultaneously
"""
import sys
import threading
import logging
from PyQt6.QtWidgets import QApplication
from dotenv import load_dotenv

# Import from your existing code
from src.config import Config
from src.utils.logging import setup_logging
from src.ui.main_window import MainWindow

# Import API server
import api_server

def run_api_server():
    """Run Flask server in background thread"""
    api_server.main()

def main():
    """Launch both API and GUI"""
    setup_logging()
    load_dotenv()
    
    print("\n" + "="*60)
    print("🚀 Starting Local LLM (API + GUI)")
    print("="*60 + "\n")
    
    # Start API server in daemon thread
    print("📡 Starting Flask API server...")
    api_thread = threading.Thread(target=run_api_server, daemon=True)
    api_thread.start()
    
    # Give API time to initialize
    import time
    time.sleep(3)
    
    # Start GUI in main thread
    print("🖥️  Starting GUI...")
    app = QApplication(sys.argv)
    cfg = Config()
    win = MainWindow(cfg)
    win.resize(900, 700)
    win.setWindowTitle("Local LLM - API Server Running on :5000")
    win.show()
    
    print("\n✅ Both API and GUI are running!")
    print("   API: http://localhost:5000")
    print("   GUI: Active window\n")
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
EOF
```

### Step 4.5: Test the API Server

```bash
# First, install dependencies in local-llm
pip install -r requirements.txt

# Test API only
python api_server.py

# In another terminal, test it:
curl http://localhost:5000/health

# Should return: {"status": "ok", "model": "Qwen/Qwen2.5-3B-Instruct", ...}
```

### Step 4.6: Commit Changes to local-llm

**Important:** We're now in the `local-llm` directory, so these commits go to your local-llm repo!

```bash
# Check where you are
pwd  # Should show: .../local-llm

# Commit the new files
git add api_server.py start_both.py requirements.txt
git commit -m "feat: add Flask API server and combined launcher"

# Push to YOUR local-llm repo
git push origin main
```

### Step 4.7: Update Submodule Reference

```bash
# Go back to main project
cd ..  # Back to product-research-agent/

# Update submodule to latest commit
cd local-llm
git pull origin main
cd ..

# Commit the updated submodule reference
git add local-llm
git commit -m "chore: update local-llm submodule to include API server"
```

**✅ Checkpoint: You should have:**
- Flask API server in local-llm
- Combined launcher (API + GUI)
- Changes committed to local-llm repo
- Submodule updated in main project

---

## 🔧 Phase 5: Configuration & Models

### Step 5.1: Create config.py
```bash
# Back in product-research-agent/
cat > src/config.py << 'EOF'
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
EOF
```

### Step 5.2: Create .env.example
```bash
cat > .env.example << 'EOF'
# LLM Configuration
LLM_BASE_URL=http://localhost:5000

# Browser Configuration
HEADLESS=false

# Scraping Configuration
MAX_PRODUCTS_PER_SITE=10
MIN_MOQ=100
MIN_SELLER_YEARS=2
```

## 🛠️ Development

### Project Structure
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

### Adding New Platforms

Create a new tool in `tools/`:

```python
from tools.base_tool import BaseTool
from src.models import ProductInfo, SearchCriteria

class EbayScraperTool(BaseTool):
    def __init__(self, page):
        super().__init__(
            name="ebay_scraper",
            description="Search eBay for products"
        )
        self.page = page
    
    async def execute(self, criteria: SearchCriteria):
        # Implement eBay scraping logic
        pass
```

Then integrate in `src/agents/product_agent.py`:
```python
ebay_tool = EbayScraperTool(self.page)
result = await ebay_tool.execute(criteria)
```

### Extending AI Reasoning

Modify `src/agents/reasoning_agent.py` to add new capabilities:

```python
def compare_platforms(self, platform_data: dict) -> str:
    """Compare multiple platforms and recommend best option"""
    prompt = f"""Compare these platforms: {platform_data}
    Which offers the best value? Provide reasoning."""
    
    return self.llm.query(prompt, temperature=0.5)
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
git clone https://github.com/DGFellow/product-research-agent.git
cd product-research-agent

# Download submodules
git submodule update --init --recursive

# Setup both projects
./setup.sh
cd local-llm && pip install -r requirements.txt && cd ..
```

## 💡 How It Works

### 1. AI Planning Phase
- Agent sends search term to local LLM
- LLM creates research strategy
- Determines which tools to use and in what order

### 2. Tool Execution Phase
- Web Navigator tool opens Playwright browser
- Alibaba tool scrapes wholesale products
- Amazon tool scrapes retail products
- All data collected into ProductInfo objects

### 3. AI Analysis Phase
- LLM analyzes collected data
- Generates insights and recommendations
- Creates summary report

### 4. Data Export Phase
- Pandas processes all products
- Creates CSV with complete data
- Generates matplotlib visualizations

## 🐛 Troubleshooting

**LLM Not Available**
```bash
# Check if API is running
curl http://localhost:5000/health

# Should return: {"status": "ok", "model": "...", "ready": true}

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

**Scraping Errors**
- Websites change their HTML frequently
- Update selectors in `tools/alibaba_tool.py` and `tools/amazon_tool.py`
- Consider adding retry logic with exponential backoff

**Import Errors**
```bash
# Make sure you're in the right environment
source venv/bin/activate

# Reinstall dependencies
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
   # MODEL_ID=meta-llama/Llama-3.1-8B-Instruct  # Slower but better
   ```

4. **Precision Settings** for GPU memory:
   ```env
   PRECISION=int4  # Least memory
   PRECISION=fp16  # Medium
   PRECISION=auto  # Most memory, best quality
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
- [Agent Tool Pattern](https://python.langchain.com/docs/modules/agents/tools/)

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
EOF
```

### Step 10.2: Create CONTRIBUTING guide
```bash
cat > CONTRIBUTING.md << 'EOF'
# Contributing to Product Research Agent

Thank you for your interest in contributing! 🎉

## Development Setup

1. Fork and clone the repository with submodules:
   ```bash
   git clone --recurse-submodules https://github.com/YOUR_USERNAME/product-research-agent.git
   cd product-research-agent
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   ./setup.sh
   source venv/bin/activate
   ```

3. Create a branch:
   ```bash
   git checkout -b feature/my-feature
   ```

## Commit Convention

We use [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation changes
- `refactor:` Code refactoring
- `test:` Test additions
- `chore:` Maintenance tasks

Examples:
```bash
git commit -m "feat: add eBay scraper tool"
git commit -m "fix: handle timeout in Alibaba scraper"
git commit -m "docs: update installation instructions"
```

## Code Style

- Follow PEP 8
- Use type hints where possible
- Add docstrings to classes and functions
- Keep functions focused and small (< 50 lines)

## Adding New Tools

1. Create tool in `tools/`:
   ```python
   from tools.base_tool import BaseTool
   
   class NewTool(BaseTool):
       def __init__(self, page):
           super().__init__(name="new_tool", description="...")
       
       async def execute(self, **kwargs):
           # Implementation
           pass
   ```

2. Add tests in `tests/test_tools.py`

3. Update README with new capability

## Testing

```bash
# Run all tests
pytest

# Run specific test
pytest tests/test_tools.py -v

# With coverage
pytest --cov=src tests/
```

## Pull Request Process

1. Ensure all tests pass
2. Update documentation if needed
3. Add entry to CHANGELOG.md
4. Create PR with clear description
5. Request review

## Working with Submodules

If you make changes to `local-llm`:

```bash
# Make changes in local-llm/
cd local-llm
# ... make changes ...
git commit -m "feat: improve API"
git push

# Update submodule reference in main project
cd ..
git add local-llm
git commit -m "chore: update local-llm submodule"
```

## Questions?

Open an issue or start a discussion on GitHub!
EOF
```

### Step 10.3: Create LICENSE
```bash
cat > LICENSE << 'EOF'
MIT License

Copyright (c) 2024 DGFellow

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF
```

### Step 10.4: Commit documentation
```bash
git add README.md CONTRIBUTING.md LICENSE
git commit -m "docs: add comprehensive documentation"
```

**✅ Checkpoint: You should have:**
- Professional README
- Contributing guidelines
- MIT License
- Complete documentation

---

## 🎉 Phase 11: Final Setup & Testing

### Step 11.1: Create test checklist script
```bash
cat > scripts/test_checklist.sh << 'EOF'
#!/bin/bash

echo "🧪 Product Research Agent - Test Checklist"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

check_pass() {
    echo -e "${GREEN}✓${NC} $1"
}

check_fail() {
    echo -e "${RED}✗${NC} $1"
}

# Test virtual environment
echo "1. Testing virtual environment..."
if [ -d "venv" ]; then
    check_pass "Virtual environment exists"
else
    check_fail "Virtual environment missing (run ./setup.sh)"
fi

# Test submodule
echo ""
echo "2. Testing git submodule..."
if [ -d "local-llm/src" ]; then
    check_pass "local-llm submodule initialized"
else
    check_fail "local-llm submodule missing (run: git submodule update --init)"
fi

# Test dependencies
echo ""
echo "3. Testing Python dependencies..."
source venv/bin/activate 2>/dev/null
python -c "import playwright; import pandas; import flask" 2>/dev/null
if [ $? -eq 0 ]; then
    check_pass "All dependencies installed"
else
    check_fail "Dependencies missing (run: pip install -r requirements.txt)"
fi

# Test Playwright browsers
echo ""
echo "4. Testing Playwright browsers..."
if playwright --version 2>/dev/null; then
    check_pass "Playwright installed"
else
    check_fail "Playwright missing (run: python -m playwright install chromium)"
fi

# Test LLM API
echo ""
echo "5. Testing LLM API connection..."
curl -s http://localhost:5000/health > /dev/null 2>&1
if [ $? -eq 0 ]; then
    check_pass "LLM API is running"
else
    check_fail "LLM API not running (run: ./scripts/start_llm.sh in another terminal)"
fi

# Test output directories
echo ""
echo "6. Testing output directories..."
if [ -d "outputs" ] && [ -d "data" ]; then
    check_pass "Output directories exist"
else
    check_fail "Output directories missing"
fi

echo ""
echo "=========================================="
echo "Test complete!"
echo ""
echo "If all tests pass, you're ready to run:"
echo "  python main.py \"your search term\""
EOF

chmod +x scripts/test_checklist.sh
```

### Step 11.2: Run complete test
```bash
# Run the test checklist
./scripts/test_checklist.sh
```

### Step 11.3: Test the full workflow
```bash
# Terminal 1: Start LLM
./scripts/start_llm.sh

# Wait for server to start, then in Terminal 2:
source venv/bin/activate
python main.py "bluetooth speaker" --max-products 3

# Verify outputs
ls -la outputs/
```

### Step 11.4: Commit final scripts
```bash
git add scripts/test_checklist.sh
git commit -m "test: add testing checklist script"
```

**✅ Final Checkpoint: Everything should:**
- Have git commits for each phase
- Work end-to-end
- Generate outputs correctly
- Connect to LLM successfully

---

## 🚀 Phase 12: Push to GitHub

### Step 12.1: Create GitHub repository
1. Go to https://github.com/new
2. Name: `product-research-agent`
3. Description: "AI-powered web agent for product research with local LLM reasoning"
4. **Do NOT initialize with README** (we already have one)
5. Click "Create repository"

### Step 12.2: Push to GitHub
```bash
# Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/DGFellow/product-research-agent.git

# Push main branch
git branch -M main
git push -u origin main

# Verify on GitHub that .gitmodules is there
```

### Step 12.3: Verify submodule on GitHub
1. Visit your repository on GitHub
2. Click on the `local-llm` folder
3. You should see it links to your other repo (appears with @ symbol)
4. This shows professional project organization!

### Step 12.4: Add topics/tags (optional)
On GitHub repository page:
- Click ⚙️ (gear icon) next to "About"
- Add topics: `ai-agent`, `web-scraping`, `llm`, `playwright`, `python`, `product-research`
- Add description and website if you have one

**✅ Checkpoint: GitHub repo should show:**
- All your code
- Submodule link to local-llm
- Professional README
- Proper license
- Clean commit history

---

## 🎯 Phase 13: Usage Guide

### For You (Developer):

```bash
# Every time you work on the project:

# Terminal 1: Start LLM
cd product-research-agent
./scripts/start_llm.sh
# OR with GUI: ./scripts/start_llm_with_gui.sh

# Terminal 2: Run agent
cd product-research-agent
source venv/bin/activate
python main.py "search term"
```

### For Others (Cloning Your Project):

```bash
# One-time setup
git clone --recurse-submodules https://github.com/DGFellow/product-research-agent.git
cd product-research-agent
./setup.sh
source venv/bin/activate

# Setup local-llm
cd local-llm
pip install -r requirements.txt
cd ..

# Every time they use it:
# Terminal 1:
./scripts/start_llm.sh

# Terminal 2:
source venv/bin/activate
python main.py "product name"
```

---

## 📋 Complete Checklist

### Setup Phase ✓
- [x] Project structure created
- [x] Git initialized
- [x] Dependencies installed
- [x] Virtual environment working

### Integration Phase ✓
- [x] local-llm added as submodule
- [x] Flask API created
- [x] Combined launcher (API + GUI)
- [x] LLM client working

### Core Development ✓
- [x] Configuration system
- [x] Data models
- [x] Base tool interface
- [x] Web navigator tool
- [x] Alibaba scraper tool
- [x] Amazon scraper tool
- [x] Reasoning agent
- [x] Main orchestrator
- [x] Analysis module

### Interface & Scripts ✓
- [x] CLI interface
- [x] Helper scripts
- [x] Test checklist

### Documentation ✓
- [x] README.md
- [x] CONTRIBUTING.md
- [x] LICENSE
- [x] Code comments

### Testing & Deployment ✓
- [x] End-to-end testing
- [x] GitHub repository
- [x] All commits pushed
- [x] Submodule linked

---

## 🎓 What You've Built

Congratulations! You now have:

1. **Professional AI Agent** - Tool-based architecture with local LLM
2. **Git Submodule Integration** - Shows code reuse skills
3. **API Design** - Flask wrapper around ML model
4. **Web Scraping** - Multi-platform data collection
5. **Data Analysis** - Automated reporting
6. **Clean Code** - Modular, documented, tested

## 🌟 Next Steps

### Enhancements:
1. Add more platforms (eBay, Walmart, Etsy)
2. Implement caching to avoid re-scraping
3. Add more AI reasoning capabilities
4. Create web UI with Flask/Streamlit
5. Deploy with Docker
6. Add database for historical tracking
7. Implement retry logic and error recovery
8. Add unit tests with pytest

### Portfolio Improvements:
1. Add screenshots to README
2. Create demo video
3. Write blog post about the architecture
4. Add badges (build status, coverage, etc.)
5. Create project website/documentation site

---

## 💡 Understanding the Architecture

**Why this design?**

1. **Git Submodule**: Shows you can integrate existing projects professionally
2. **Flask API**: Demonstrates API design and ML deployment
3. **Tool-based**: Extensible - easy to add new platforms
4. **Async**: Handles web scraping efficiently
5. **LLM Reasoning**: Shows AI agent capabilities beyond simple scripts

**Key Interview Talking Points:**
- "I integrated my LLM project as a submodule to demonstrate code reuse"
- "Built a Flask API to wrap the transformer model for easier integration"
- "Used tool-based architecture inspired by agent frameworks like Smolagents"
- "Implements async web scraping with intelligent retry logic"
- "LLM plans research strategy and analyzes results autonomously"

---

Ready to start building? Let's go phase by phase! Which phase would you like to begin with? 🚀_SITE=10
MIN_MOQ=100
MIN_SELLER_YEARS=2
EOF
```

### Step 5.3: Create data models
```bash
cat > src/models.py << 'EOF'
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
        return f"SearchCriteria(term='{self.search_term}', moq>={self.min_moq}, years>={self.min_seller_years})"
EOF
```

### Step 5.4: Create LLM client
```bash
cat > src/llm_client.py << 'EOF'
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
        """
        Query the local LLM via Flask API
        
        Args:
            prompt: User prompt
            system: System message
            temperature: Sampling temperature
            max_tokens: Maximum response tokens
            
        Returns:
            LLM response text
        """
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
EOF
```

### Step 5.5: Commit
```bash
git add src/config.py src/models.py src/llm_client.py .env.example
git commit -m "feat: add configuration, data models, and LLM client"
```

**✅ Checkpoint: You should have:**
- Configuration system
- Data models defined
- LLM client that talks to Flask API

---

## 🛠️ Phase 6: Tool-Based Architecture

### Step 6.1: Create base tool interface
```bash
cat > tools/base_tool.py << 'EOF'
from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseTool(ABC):
    """Abstract base class for agent tools"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    @abstractmethod
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Execute the tool
        
        Returns:
            Dictionary with execution results
        """
        pass
    
    def log(self, message: str, emoji: str = "ℹ️"):
        """Consistent logging format"""
        print(f"{emoji} [{self.name}] {message}")
    
    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}')"
EOF
```

### Step 6.2: Create web navigator tool
```bash
cat > tools/web_navigator.py << 'EOF'
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
        """
        Execute navigation action
        
        Actions:
            - goto: Navigate to URL
            - wait: Wait for selector
            - get_content: Get page content
        """
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
                return {
                    "success": True,
                    "title": title,
                    "url": url
                }
            
            else:
                return {"success": False, "error": f"Unknown action: {action}"}
                
        except Exception as e:
            self.log(f"Error: {e}", "❌")
            return {"success": False, "error": str(e)}
EOF
```

### Step 6.3: Create Alibaba scraper tool
```bash
cat > tools/alibaba_tool.py << 'EOF'
from typing import List, Dict, Any
from playwright.async_api import Page
from tools.base_tool import BaseTool
from tools.web_navigator import WebNavigatorTool
from src.models import ProductInfo, SearchCriteria

class AlibabaScraperTool(BaseTool):
    """Tool for scraping Alibaba product listings"""
    
    BASE_URL = "https://www.alibaba.com"
    
    def __init__(self, page: Page):
        super().__init__(
            name="alibaba_scraper",
            description="Search and extract product information from Alibaba"
        )
        self.page = page
        self.navigator = WebNavigatorTool(page)
    
    async def execute(self, criteria: SearchCriteria) -> Dict[str, Any]:
        """Search Alibaba and extract products"""
        self.log(f"Searching for: {criteria.search_term}", "🔍")
        
        try:
            # Navigate to search
            search_url = f"{self.BASE_URL}/trade/search?SearchText={criteria.search_term.replace(' ', '+')}"
            await self.navigator.execute("goto", url=search_url)
            
            # Wait for results
            await self.navigator.execute("wait", selector='.organic-list-offer', timeout=10000)
            
            # Extract products
            products = await self._extract_products(criteria.max_results)
            
            self.log(f"Found {len(products)} products", "✅")
            return {
                "success": True,
                "products": products,
                "count": len(products)
            }
            
        except Exception as e:
            self.log(f"Search failed: {e}", "❌")
            return {
                "success": False,
                "error": str(e),
                "products": []
            }
    
    async def _extract_products(self, max_results: int) -> List[ProductInfo]:
        """Extract product information from search results"""
        products = []
        
        product_cards = await self.page.query_selector_all('.organic-list-offer')
        
        for i, card in enumerate(product_cards[:max_results]):
            try:
                product = await self._extract_product_card(card)
                if product:
                    products.append(product)
                    self.log(f"  → {product.title[:50]}...", "📦")
            except Exception as e:
                self.log(f"  → Error extracting product {i}: {e}", "⚠️")
                continue
        
        return products
    
    async def _extract_product_card(self, card) -> ProductInfo:
        """Extract info from a single product card"""
        # Title
        title_elem = await card.query_selector('.organic-list-offer-title')
        title = await title_elem.inner_text() if title_elem else "N/A"
        
        # Price
        price_elem = await card.query_selector('.organic-list-offer-price')
        price = await price_elem.inner_text() if price_elem else "N/A"
        
        # URL
        link_elem = await card.query_selector('a')
        url = await link_elem.get_attribute('href') if link_elem else None
        if url and not url.startswith('http'):
            url = f"{self.BASE_URL}{url}"
        
        return ProductInfo(
            source='alibaba',
            title=title.strip(),
            price=price.strip(),
            url=url,
            moq="Contact supplier",  # Would need detail page scraping
            seller_years="Unknown"  # Would need detail page scraping
        )
EOF
```

### Step 6.4: Create Amazon scraper tool
```bash
cat > tools/amazon_tool.py << 'EOF'
from typing import List, Dict, Any
from playwright.async_api import Page
from tools.base_tool import BaseTool
from tools.web_navigator import WebNavigatorTool
from src.models import ProductInfo, SearchCriteria

class AmazonScraperTool(BaseTool):
    """Tool for scraping Amazon product listings"""
    
    BASE_URL = "https://www.amazon.com"
    
    def __init__(self, page: Page):
        super().__init__(
            name="amazon_scraper",
            description="Search and extract product information from Amazon"
        )
        self.page = page
        self.navigator = WebNavigatorTool(page)
    
    async def execute(self, criteria: SearchCriteria) -> Dict[str, Any]:
        """Search Amazon and extract products"""
        self.log(f"Searching for: {criteria.search_term}", "🔍")
        
        try:
            # Navigate to search
            search_url = f"{self.BASE_URL}/s?k={criteria.search_term.replace(' ', '+')}"
            await self.navigator.execute("goto", url=search_url)
            
            # Wait for results
            await self.navigator.execute("wait", 
                                        selector='[data-component-type="s-search-result"]',
                                        timeout=10000)
            
            # Extract products
            products = await self._extract_products(criteria.max_results)
            
            self.log(f"Found {len(products)} products", "✅")
            return {
                "success": True,
                "products": products,
                "count": len(products)
            }
            
        except Exception as e:
            self.log(f"Search failed: {e}", "❌")
            return {
                "success": False,
                "error": str(e),
                "products": []
            }
    
    async def _extract_products(self, max_results: int) -> List[ProductInfo]:
        """Extract product information from search results"""
        products = []
        
        product_cards = await self.page.query_selector_all('[data-component-type="s-search-result"]')
        
        for i, card in enumerate(product_cards[:max_results]):
            try:
                product = await self._extract_product_card(card)
                if product:
                    products.append(product)
                    self.log(f"  → {product.title[:50]}...", "📦")
            except Exception as e:
                self.log(f"  → Error extracting product {i}: {e}", "⚠️")
                continue
        
        return products
    
    async def _extract_product_card(self, card) -> ProductInfo:
        """Extract info from a single product card"""
        # Title
        title_elem = await card.query_selector('h2 a span')
        title = await title_elem.inner_text() if title_elem else "N/A"
        
        # Price
        price_elem = await card.query_selector('.a-price-whole')
        price = await price_elem.inner_text() if price_elem else "N/A"
        if price != "N/A":
            price = f"${price.strip()}"
        
        # URL
        link_elem = await card.query_selector('h2 a')
        url = await link_elem.get_attribute('href') if link_elem else None
        if url and not url.startswith('http'):
            url = f"{self.BASE_URL}{url}"
        
        return ProductInfo(
            source='amazon',
            title=title.strip(),
            price=price,
            url=url
        )
EOF
```

### Step 6.5: Commit tools
```bash
git add tools/
git commit -m "feat: add tool-based architecture with web scraping tools"
```

**✅ Checkpoint: You should have:**
- Base tool interface
- Web navigator tool
- Alibaba scraper tool
- Amazon scraper tool

---

## 🤖 Phase 7: Reasoning Agent

### Step 7.1: Create reasoning agent
```bash
cat > src/agents/reasoning_agent.py << 'EOF'
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
        """
        Create a research plan using LLM reasoning
        
        Args:
            search_term: Product to research
            
        Returns:
            Research plan with steps
        """
        prompt = f"""Create a research plan for finding product information about: "{search_term}"

Available tools:
- alibaba_scraper: Search Alibaba for wholesale products
- amazon_scraper: Search Amazon for retail products

Create a simple plan with 3-4 steps. Respond in JSON format:
{{
    "goal": "overall research objective",
    "steps": [
        {{"action": "tool_name", "reason": "why this step"}},
        ...
    ],
    "success_criteria": "how to know if research succeeded"
}}"""
        
        system = "You are a research planning assistant. Always respond with valid JSON."
        
        response = self.llm.query(prompt, system=system, temperature=0.3, max_tokens=500)
        
        try:
            plan = self._parse_json(response)
            self.decision_history.append({"type": "plan", "data": plan})
            return plan
        except Exception as e:
            print(f"❌ Plan parsing failed: {e}")
            # Return fallback plan
            return {
                "goal": f"Research {search_term} on multiple platforms",
                "steps": [
                    {"action": "alibaba_scraper", "reason": "Find wholesale options"},
                    {"action": "amazon_scraper", "reason": "Find retail comparisons"}
                ],
                "success_criteria": "Products found on both platforms"
            }
    
    def analyze_results(self, alibaba_count: int, amazon_count: int, 
                       search_term: str) -> str:
        """
        Generate insights about research results
        
        Args:
            alibaba_count: Number of Alibaba products found
            amazon_count: Number of Amazon products found
            search_term: What was searched
            
        Returns:
            Analysis summary
        """
        prompt = f"""Analyze these product research results:

Search Term: {search_term}
Alibaba Products Found: {alibaba_count}
Amazon Products Found: {amazon_count}

Provide a brief 2-3 sentence analysis covering:
1. What the data suggests about availability
2. One key insight or recommendation

Be concise and actionable."""
        
        system = "You are a product research analyst. Provide brief, actionable insights."
        
        response = self.llm.query(prompt, system=system, temperature=0.7, max_tokens=200)
        
        self.decision_history.append({
            "type": "analysis",
            "data": {"summary": response}
        })
        
        return response
    
    def _parse_json(self, response: str) -> Dict[str, Any]:
        """Extract and parse JSON from LLM response"""
        # Try to find JSON in response
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        
        # If no JSON found, try parsing the whole response
        return json.loads(response)
    
    def get_decision_history(self) -> List[Dict[str, Any]]:
        """Get history of all decisions made"""
        return self.decision_history
EOF
```

### Step 7.2: Create main product agent
```bash
cat > src/agents/product_agent.py << 'EOF'
from playwright.async_api import async_playwright, Browser, Page
from typing import List, Optional
from src.llm_client import LLMClient
from src.agents.reasoning_agent import ReasoningAgent
from tools.alibaba_tool import AlibabaScraperTool
from tools.amazon_tool import AmazonScraperTool
from src.models import ProductInfo, SearchCriteria
from src.config import Config

class ProductResearchAgent:
    """Main orchestrator for product research"""
    
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client
        self.reasoning_agent = ReasoningAgent(llm_client)
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        self.products: List[ProductInfo] = []
        self.config = Config()
    
    async def initialize(self):
        """Initialize browser and tools"""
        print("🚀 Initializing browser...")
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(
            headless=self.config.HEADLESS
        )
        self.page = await self.browser.new_page()
        await self.page.set_viewport_size({
            "width": self.config.VIEWPORT_WIDTH,
            "height": self.config.VIEWPORT_HEIGHT
        })
        print("✅ Browser ready")
    
    async def close(self):
        """Close browser"""
        if self.browser:
            await self.browser.close()
            print("👋 Browser closed")
    
    async def research_product(self, search_term: str) -> List[ProductInfo]:
        """
        Main research workflow with AI reasoning
        
        Args:
            search_term: Product to research
            
        Returns:
            List of all products found
        """
        print(f"\n{'='*60}")
        print(f"🔬 Researching: {search_term}")
        print(f"{'='*60}\n")
        
        # Create search criteria
        criteria = SearchCriteria(
            search_term=search_term,
            min_moq=self.config.MIN_MOQ,
            min_seller_years=self.config.MIN_SELLER_YEARS,
            max_results=self.config.MAX_PRODUCTS_PER_SITE
        )
        
        # Phase 1: AI Planning
        print("🧠 Phase 1: AI Research Planning")
        plan = self.reasoning_agent.plan_research(search_term)
        print(f"   Goal: {plan.get('goal', 'Research products')}")
        print(f"   Steps: {len(plan.get('steps', []))} planned actions\n")
        
        # Phase 2: Execute Research
        print("📍 Phase 2: Data Collection")
        
        # Alibaba
        print("  → Searching Alibaba...")
        alibaba_tool = AlibabaScraperTool(self.page)
        alibaba_result = await alibaba_tool.execute(criteria)
        alibaba_products = alibaba_result.get('products', [])
        self.products.extend(alibaba_products)
        
        # Amazon
        print("\n  → Searching Amazon...")
        amazon_tool = AmazonScraperTool(self.page)
        amazon_result = await amazon_tool.execute(criteria)
        amazon_products = amazon_result.get('products', [])
        self.products.extend(amazon_products)
        
        # Phase 3: AI Analysis
        print(f"\n🧠 Phase 3: AI Analysis")
        if self.products:
            analysis = self.reasoning_agent.analyze_results(
                alibaba_count=len(alibaba_products),
                amazon_count=len(amazon_products),
                search_term=search_term
            )
            print(f"\n💡 Insights:\n{analysis}\n")
        
        return self.products
    
    def get_products(self) -> List[ProductInfo]:
        """Get all collected products"""
        return self.products
EOF
```

### Step 7.3: Commit agents
```bash
git add src/agents/
git commit -m "feat: add reasoning agent and main orchestrator"
```

**✅ Checkpoint: You should have:**
- Reasoning agent with LLM integration
- Main product research orchestrator
- AI-powered planning and analysis

---

## 📊 Phase 8: Analysis Module

### Step 8.1: Create analyzer
```bash
cat > src/analysis/analyzer.py << 'EOF'
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
from pathlib import Path
from typing import List
from src.models import ProductInfo
from src.config import Config

class ProductAnalyzer:
    """Analyze and visualize product data"""
    
    def __init__(self, products: List[ProductInfo]):
        self.products = products
        self.df = self._create_dataframe()
        
    def _create_dataframe(self) -> pd.DataFrame:
        """Convert products to DataFrame"""
        if not self.products:
            return pd.DataFrame()
        
        data = [p.to_dict() for p in self.products]
        df = pd.DataFrame(data)
        
        # Clean price data
        df['price_numeric'] = df['price'].apply(self._extract_price)
        
        return df
    
    @staticmethod
    def _extract_price(price_str) -> float:
        """Extract numeric price from string"""
        if pd.isna(price_str) or price_str == "N/A":
            return None
        match = re.search(r'[\d,]+\.?\d*', str(price_str))
        if match:
            return float(match.group().replace(',', ''))
        return None
    
    def export_csv(self, filename: str = "product_research.csv"):
        """Export data to CSV"""
        if self.df.empty:
            print("⚠️  No data to export")
            return None
        
        output_path = Config.OUTPUT_DIR / filename
        self.df.to_csv(output_path, index=False)
        print(f"✅ Exported to {output_path}")
        return output_path
    
    def create_visualizations(self, filename: str = "product_analysis.png"):
        """Create comprehensive visualization"""
        if self.df.empty:
            print("⚠️  No data to visualize")
            return None
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Product Research Analysis', fontsize=16, fontweight='bold')
        
        # Set style
        sns.set_style("whitegrid")
        
        # 1. Price distribution by source
        valid_prices = self.df[self.df['price_numeric'].notna()]
        if not valid_prices.empty and len(valid_prices['source'].unique()) > 1:
            valid_prices.boxplot(column='price_numeric', by='source', ax=axes[0, 0])
            axes[0, 0].set_title('Price Distribution by Source')
            axes[0, 0].set_xlabel('Source')
            axes[0, 0].set_ylabel('Price ($)')
            plt.sca(axes[0, 0])
            plt.xticks(rotation=0)
        else:
            axes[0, 0].text(0.5, 0.5, 'Insufficient price data', 
                           ha='center', va='center', transform=axes[0, 0].transAxes)
            axes[0, 0].set_title('Price Distribution by Source')
        
        # 2. Product count by source
        source_counts = self.df['source'].value_counts()
        colors = ['#ff9900' if s == 'alibaba' else '#00a8e1' for s in source_counts.index]
        axes[0, 1].bar(source_counts.index, source_counts.values, color=colors)
        axes[0, 1].set_title('Products Found by Source')
        axes[0, 1].set_xlabel('Source')
        axes[0, 1].set_ylabel('Count')
        
        # 3. Average price comparison
        if not valid_prices.empty:
            avg_prices = valid_prices.groupby('source')['price_numeric'].mean()
            colors = ['#ff9900' if s == 'alibaba' else '#00a8e1' for s in avg_prices.index]
            axes[1, 0].bar(avg_prices.index, avg_prices.values, color=colors)
            axes[1, 0].set_title('Average Price by Source')
            axes[1, 0].set_xlabel('Source')
            axes[1, 0].set_ylabel('Average Price ($)')
            
            # Add value labels on bars
            for i, (idx, val) in enumerate(avg_prices.items()):
                axes[1, 0].text(i, val, f'${val:.2f}', ha='center', va='bottom')
        else:
            axes[1, 0].text(0.5, 0.5, 'No price data', 
                           ha='center', va='center', transform=axes[1, 0].transAxes)
            axes[1, 0].set_title('Average Price by Source')
        
        # 4. Top products by price
        if not valid_prices.empty:
            top_products = valid_prices.nlargest(min(10, len(valid_prices)), 'price_numeric')
            colors = ['#ff9900' if s == 'alibaba' else '#00a8e1' for s in top_products['source']]
            axes[1, 1].barh(range(len(top_products)), top_products['price_numeric'], color=colors)
            axes[1, 1].set_yticks(range(len(top_products)))
            axes[1, 1].set_yticklabels([t[:30] + '...' if len(t) > 30 else t 
                                        for t in top_products['title']], fontsize=8)
            axes[1, 1].set_title(f'Top {len(top_products)} Most Expensive Products')
            axes[1, 1].set_xlabel('Price ($)')
            axes[1, 1].invert_yaxis()
        else:
            axes[1, 1].text(0.5, 0.5, 'No price data', 
                           ha='center', va='center', transform=axes[1, 1].transAxes)
            axes[1, 1].set_title('Top Products by Price')
        
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
EOF
```

### Step 8.2: Commit analysis
```bash
git add src/analysis/
git commit -m "feat: add product analyzer with visualizations"
```

**✅ Checkpoint: You should have:**
- Data analysis module
- CSV export functionality
- Matplotlib visualizations

---

## 🎮 Phase 9: CLI Interface

### Step 9.1: Create main script
```bash
cat > main.py << 'EOF'
import asyncio
import argparse
from src.llm_client import LLMClient
from src.agents.product_agent import ProductResearchAgent
from src.analysis.analyzer import ProductAnalyzer
from src.config import Config

def parse_args():
    parser = argparse.ArgumentParser(
        description="AI-powered product research agent"
    )
    parser.add_argument(
        "search_term",
        nargs="?",
        help="Product to research (e.g., 'wireless earbuds')"
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run browser in headless mode"
    )
    parser.add_argument(
        "--max-products",
        type=int,
        default=10,
        help="Maximum products per site (default: 10)"
    )
    return parser.parse_args()

async def main():
    """Main execution function"""
    args = parse_args()
    
    # Get search term
    search_term = args.search_term
    if not search_term:
        search_term = input("🔍 Enter product to research: ").strip()
        if not search_term:
            print("❌ Search term required")
            return
    
    # Update config if needed
    if args.headless:
        Config.HEADLESS = True
    if args.max_products:
        Config.MAX_PRODUCTS_PER_SITE = args.max_products
    
    # Initialize LLM client
    print("\n🤖 Connecting to local LLM...")
    llm = LLMClient()
    
    if not llm.is_available():
        print("⚠️  Warning: LLM service not available at", Config.LLM_BASE_URL)
        print("   Make sure local-llm API server is running:")
        print(f"   cd local-llm && python api_server.py")
        print("\n   Agent will continue with basic functionality.\n")
    else:
        print("✅ LLM connected\n")
    
    # Initialize agent
    agent = ProductResearchAgent(llm)
    
    try:
        await agent.initialize()
        
        # Run research
        products = await agent.research_product(search_term)
        
        if not products:
            print("\n⚠️  No products found. Try a different search term.")
            return
        
        # Analyze results
        print(f"\n{'='*60}")
        print("📊 Generating Analysis...")
        print(f"{'='*60}\n")
        
        analyzer = ProductAnalyzer(products)
        analyzer.export_csv()
        analyzer.create_visualizations()
        
        # Print summary
        stats = analyzer.get_summary_stats()
        print(f"\n{'='*60}")
        print("✅ Research Complete!")
        print(f"{'='*60}")
        print(f"\n📊 Summary:")
        print(f"  Total products: {stats['total_products']}")
        if 'by_source' in stats:
            print(f"  By source: {stats['by_source']}")
        if stats.get('price_stats'):
            print(f"  Avg price: ${stats['price_stats']['mean']:.2f}")
            print(f"  Price range: ${stats['price_stats']['min']:.2f} - ${stats['price_stats']['max']:.2f}")
        
        print(f"\n📁 Output files:")
        print(f"   📄 {Config.OUTPUT_DIR}/product_research.csv")
        print(f"   📊 {Config.OUTPUT_DIR}/product_analysis.png\n")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Research interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await agent.close()

if __name__ == "__main__":
    asyncio.run(main())
EOF
```

### Step 9.2: Create helper scripts
```bash
mkdir -p scripts

# Script to start LLM
cat > scripts/start_llm.sh << 'EOF'
#!/bin/bash
echo "🚀 Starting Local LLM API Server..."
cd local-llm
source ../venv/bin/activate
python api_server.py
EOF

chmod +x scripts/start_llm.sh

# Script to start both API and GUI
cat > scripts/start_llm_with_gui.sh << 'EOF'
#!/bin/bash
echo "🚀 Starting Local LLM (API + GUI)..."
cd local-llm
source ../venv/bin/activate
python start_both.py
EOF

chmod +x scripts/start_llm_with_gui.sh
```

### Step 9.3: Commit
```bash
git add main.py scripts/
git commit -m "feat: add CLI interface and helper scripts"
```

**✅ Checkpoint: You should have:**
- Complete CLI interface
- Helper scripts for starting LLM
- Full working application

---

## 📚 Phase 10: Documentation

### Step 10.1: Create comprehensive README
```bash
cat > README.md << 'EOF'
# 🤖 Product Research Agent

An AI-powered web agent that autonomously researches products across Alibaba and Amazon, using a **local LLM** (no API costs!) for intelligent reasoning and decision-making.

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

### 3. Start Local LLM

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

### 4. Run Research Agent

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

🧠 Phase 1: AI Research Planning
   Goal: Compare coffee makers across wholesale and retail platforms
   Steps: 2 planned actions

📍 Phase 2: Data Collection
  → Searching Alibaba...
🔍 [alibaba_scraper] Searching for: coffee maker
📦 [alibaba_scraper]   → Espresso Coffee Maker Machine Professional...
✅ [alibaba_scraper] Found 10 products

  → Searching Amazon...
🔍 [amazon_scraper] Searching for: coffee maker
📦 [amazon_scraper]   → Keurig K-Elite Coffee Maker, Single Serve...
✅ [amazon_scraper] Found 10 products

🧠 Phase 3: AI Analysis

💡 Insights:
The research reveals strong availability across both platforms with 10 
products each. Alibaba offers wholesale options suitable for bulk 
purchasing, while Amazon provides diverse retail choices. Consider 
Amazon for immediate consumer needs or Alibaba for business sourcing.

============================================================
📊 Generating Analysis...
============================================================

✅ Exported to outputs/product_research.csv
✅ Saved visualization to outputs/product_analysis.png

📊 Summary:
  Total products: 20
  By source: {'alibaba': 10, 'amazon': 10}
  Avg price: $67.45
  Price range: $19.99 - $299.00

📁 Output files:
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

Edit `.env` file:

```env
# LLM Configuration
LLM_BASE_URL=http://localhost:5000

# Browser Configuration
HEADLESS=false

# Scraping Configuration
MAX_PRODUCTS_PER