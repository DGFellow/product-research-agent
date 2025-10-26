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