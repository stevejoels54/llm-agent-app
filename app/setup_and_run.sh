#!/bin/bash

echo "Setting up AI Agent Development Environment"
echo "=============================================="

if [ ! -f "main.py" ]; then
    echo "Error: Please run this script from the app/ directory"
    exit 1
fi

echo "Using current Python environment..."

echo "Checking Ollama status..."
if ! curl -s http://localhost:11434/api/tags > /dev/null; then
    echo "Error: Ollama not running on localhost:11434"
    echo "Please start Ollama: ollama serve"
    echo "And ensure llama3.2 is installed: ollama pull llama3.2"
    exit 1
else
    echo "Ollama is running"
fi

echo "Starting Inngest dev server in background..."
npx inngest-cli@latest dev -u http://127.0.0.1:5050/api/inngest --no-discovery &
INNGEST_PID=$!

sleep 3

echo "Starting Flask application..."
echo "App will be available at: http://localhost:5050"
echo "Inngest dashboard at: http://localhost:8288"
echo ""
echo "To test the agent, run in another terminal:"
echo "   python test_agent.py"
echo ""
echo "Press Ctrl+C to stop all services"

trap "echo 'Stopping services...'; kill $INNGEST_PID 2>/dev/null; exit" INT

python main.py

kill $INNGEST_PID 2>/dev/null
