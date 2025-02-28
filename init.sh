#!/bin/bash

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
echo "Requirements installed"

brew install ollama
echo "Ollama installed"

ollama serve
echo "Ollama running"

ollama run deepseek-r1
echo "Deepseek installed"
