# Contributing to LifeGrid

Thank you for your interest in contributing to LifeGrid! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Submitting Changes](#submitting-changes)

## Code of Conduct

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md).

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/LifeGrid.git
   cd LifeGrid
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/James-HoneyBadger/LifeGrid.git
   ```

## Development Setup

### Prerequisites

- Python 3.13 or higher
- Git
- Virtual environment tool (venv recommended)

### Installation

1. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install development dependencies**:
   ```bash
   pip install pytest pytest-cov mypy sphinx sphinx-rtd-theme
   ```

4. **Verify installation**:
   ```bash
   pytest tests/ -v
   ```

   All 136 tests should pass.

## How to Contribute

### Reporting Bugs

Before creating bug reports:
- Check the [issue tracker](https://github.com/James-HoneyBadger/LifeGrid/issues)
- Search for existing issues

When creating a bug report, include:
- **Clear title** and description
- **Steps to reproduce** the problem
- **Expected behavior**
- **Actual behavior**
- **Screenshots** (if applicable)
- **Environment details** (OS, Python version)
- **Error messages** and stack traces

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. Include:
- **Clear title** and description
- **Use case** and motivation
- **Proposed solution** or approach
- **Alternative solutions** considered
- **Mockups** or examples (if applicable)

### Pull Requests

1. **Create a branch** for your work:
   ```bash
   git checkout -b feature/my-new-feature
   ```

2. **Make your changes** following our coding standards

3. **Add tests** for new functionality

4. **Update documentation** as needed

5. **Run tests**:
   ```bash
   pytest tests/ -v
   ```

6. **Check code quality**:
   ```bash
   mypy src/
   ```

7. **Commit your changes**:
   ```bash
   git commit -m "Add feature: description of feature"
   ```
   
   Use descriptive commit messages following this format:
   - `Add feature: ...` for new features
   - `Fix bug: ...` for bug fixes
   - `Refactor: ...` for code refactoring
   - `Docs: ...` for documentation changes
   - `Test: ...` for test additions/changes

8. **Push to your fork**:
   ```bash
   git push origin feature/my-new-feature
   ```

9. **Create Pull Request** on GitHub

## Coding Standards

### Python Style

- Follow [PEP 8](https://pep8.org/) style guide
- Use 4 spaces for indentation (no tabs)
- Maximum line length: 100 characters
- Use meaningful variable and function names

### Type Hints

- Add type hints to all function signatures
- Use `typing` module for complex types
- Example:
  ```python
  def process_grid(grid: np.ndarray, size: int) -> np.ndarray:
      """Process the grid."""
      return grid * size
  ```

### Docstrings

- Use Google-style docstrings
- Include for all public modules, classes, and functions
- Example:
  ```python
  def step(self, num_steps: int = 1) -> None:
      """Advance the simulation by the specified number of steps.
      
      Args:
          num_steps: Number of generations to simulate. Defaults to 1.
          
      Raises:
          ValueError: If num_steps is negative.
          
      Example:
          >>> sim = Simulator()
          >>> sim.initialize("Conway's Game of Life")
          >>> sim.step(10)
      """
      pass
  ```

### Code Organization

- Keep functions small and focused
- Use meaningful names
- Avoid deep nesting (max 3 levels)
- Extract complex logic into separate functions
- Use constants for magic numbers

### Imports

- Group imports: standard library, third-party, local
- Sort alphabetically within groups
- Use absolute imports
- Example:
  ```python
  import os
  import sys
  from typing import Dict, List
  
  import numpy as np
  from PIL import Image
  
  from src.core.simulator import Simulator
  from src.patterns import get_pattern
  ```

## Testing

### Writing Tests

- Add tests for all new features
- Place tests in `tests/` directory
- Name test files `test_*.py`
- Name test functions `test_*`
- Use pytest fixtures for setup
- Test edge cases and error conditions

Example test:

```python
def test_simulator_initialization():
    """Test simulator initializes correctly."""
    sim = Simulator()
    assert sim.generation == 0
    assert sim.population == 0
    assert sim.config is not None

def test_simulator_step():
    """Test simulator advances generations."""
    sim = Simulator()
    sim.initialize("Conway's Game of Life")
    initial_gen = sim.generation
    sim.step(5)
    assert sim.generation == initial_gen + 5
```

### Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=src

# Run specific test file
pytest tests/test_core.py

# Run specific test
pytest tests/test_core.py::test_simulator_initialization

# Run with verbose output
pytest tests/ -v
```

### Test Coverage

- Aim for >80% code coverage
- All new code should have tests
- Check coverage:
  ```bash
  pytest tests/ --cov=src --cov-report=html
  open htmlcov/index.html
  ```

## Documentation

### Code Documentation

- Add docstrings to all public APIs
- Include examples in docstrings
- Document parameters and return values
- Explain complex algorithms

### User Documentation

When adding features, update:
- `docs/` - Sphinx documentation
- `README.md` - If user-facing
- `QUICK_REFERENCE.md` - For API changes
- Example scripts in `examples/`

### Building Documentation

```bash
cd docs
make html
open _build/html/index.html
```

## Submitting Changes

### Pull Request Checklist

Before submitting, ensure:

- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] New tests added for new functionality
- [ ] Type hints added
- [ ] Docstrings complete
- [ ] Documentation updated
- [ ] Commit messages are clear
- [ ] Branch is up to date with master
- [ ] No merge conflicts

### Pull Request Description

Include in your PR:
- **Summary** of changes
- **Motivation** for changes
- **Related issues** (use "Fixes #123")
- **Testing performed**
- **Screenshots** (if UI changes)
- **Breaking changes** (if any)

### Review Process

1. Maintainers will review your PR
2. Address any feedback
3. Once approved, PR will be merged
4. Delete your feature branch after merge

## Project Structure

```
LifeGrid/
├── src/
│   ├── core/           # Core simulator
│   ├── automata/       # Automaton implementations
│   ├── gui/            # GUI components
│   ├── *.py            # Feature modules
│   └── main.py         # Entry point
├── tests/              # Test suite
├── docs/               # Sphinx documentation
├── examples/           # Example scripts
└── README.md           # Project overview
```

## Areas for Contribution

### Good First Issues

- Add new patterns to pattern library
- Improve error messages
- Add tooltips to GUI
- Write example scripts
- Improve documentation

### Intermediate

- Implement new cellular automata
- Add export formats
- Optimize performance
- Add keyboard shortcuts
- Create tutorials

### Advanced

- Parallel processing for large grids
- Rule discovery algorithms
- Advanced visualization features
- CI/CD pipeline
- PyPI packaging

## Questions?

- Open an issue for questions
- Tag with `question` label
- Check existing issues first

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Acknowledgments

Thank you for contributing to LifeGrid! Your help makes this project better for everyone.

---

**Happy Contributing!** 🎉
