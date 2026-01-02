# Installation & Setup Guide

## System Requirements

LifeGrid requires:
- **Python**: 3.11 or higher (3.13 recommended)
- **Operating System**: Linux, macOS, or Windows
- **Tkinter**: Usually bundled with Python
- **Dependencies**: NumPy 1.24+, SciPy 1.11+, Pillow 10+ (optional)

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/James-HoneyBadger/LifeGrid.git
cd LifeGrid
```

### 2. Install Dependencies

Using pip:

```bash
pip install -r requirements.txt
```

### 3. Verify Installation

Check that all dependencies are correctly installed:

```bash
python -c "import numpy, scipy, PIL; print('✓ All dependencies installed')"
```

If Tkinter is missing, install it:

**On Ubuntu/Debian:**
```bash
sudo apt-get install python3-tk
```

**On Fedora/RHEL:**
```bash
sudo dnf install python3-tkinter
```

**On macOS (with Homebrew):**
```bash
brew install python-tk
```

**On Windows:**
Tkinter is included with Python from python.org. If using Conda, run:
```bash
conda install tk
```

## Running LifeGrid

### From Command Line

```bash
python src/main.py
```

### Using the Helper Script (Unix/Linux/macOS)

```bash
./run.sh
```

### From Python

```python
from lifegrid.gui.app import launch
launch()
```

## Troubleshooting Installation

### "No module named 'tkinter'"

Tkinter is not installed. See above for OS-specific installation instructions.

### "No module named 'numpy'" (or scipy/PIL)

Install missing dependencies:

```bash
pip install numpy scipy pillow
```

Or reinstall all requirements:

```bash
pip install --upgrade -r requirements.txt
```

### Application Won't Start

1. Verify Python version: `python --version` (should be 3.11+)
2. Check all dependencies: `pip list`
3. Try running in verbose mode: `python -v src/main.py`

### Tkinter Display Issues (Linux)

If the GUI doesn't appear, try:

```bash
pip install --upgrade --force-reinstall python-tk
```

Or for Conda users:

```bash
conda install -c conda-forge tk
```

## Virtual Environment Setup (Recommended)

For a clean installation, use a virtual environment:

```bash
# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate          # On Linux/macOS
venv\Scripts\activate             # On Windows

# Install dependencies
pip install -r requirements.txt

# Run LifeGrid
python src/main.py
```

## Development Installation

For contributing to LifeGrid, install in editable mode with development dependencies:

```bash
pip install -e ".[dev]"
```

This includes tools for testing and type checking.

## Verifying Your Installation

Run the diagnostic test:

```bash
python -c "
import tkinter
import numpy as np
import scipy
from PIL import Image
print('✓ Python version:', __import__('sys').version.split()[0])
print('✓ Tkinter: Available')
print('✓ NumPy:', np.__version__)
print('✓ SciPy:', scipy.__version__)
print('✓ Pillow: Available')
print('All systems ready for LifeGrid!')
"
```

## Next Steps

- Read the [User Guide](./user_guide.md) to learn how to use LifeGrid
- Try the [Getting Started Tutorial](../tutorials/01_getting_started.md)
- Explore built-in patterns in the Pattern menu

## Getting Help

If you encounter issues:
1. Check [Troubleshooting Guide](./troubleshooting.md)
2. Review [FAQ](./faq.md)
3. Create an issue on [GitHub](https://github.com/James-HoneyBadger/LifeGrid/issues)
