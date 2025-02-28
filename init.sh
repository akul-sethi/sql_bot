#!/bin/bash

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
echo "Requirements installed"

brew install ollama
echo "Ollama installed"

nohup ollama serve &
echo "Start server"

ollama pull llama3.1
echo "Llama installed"
