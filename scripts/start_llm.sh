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