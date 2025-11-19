#!/bin/bash
# Cellular Automaton Simulator Launch Script

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Run the application
python src/main.py
