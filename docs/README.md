# LifeGrid Documentation

Welcome to the LifeGrid documentation. This folder contains comprehensive guides, tutorials, API reference, and architectural documentation.

## Documentation Structure

### 📖 [Guides](./guides/)
User-friendly guides for common tasks and workflows:
- **Installation & Setup** - Get LifeGrid running on your system
- **User Guide** - Learn how to use the application
- **Configuration** - Customize settings and preferences
- **File Formats** - Understanding RLE and JSON pattern formats

### 🎓 [Tutorials](./tutorials/)
Step-by-step tutorials for learning LifeGrid:
- **Getting Started** - First steps with the simulator
- **Drawing & Editing** - Creating and modifying patterns
- **Advanced Features** - Leveraging power-user features
- **Custom Rules** - Creating your own cellular automaton rules
- **Exporting & Sharing** - Save and export your work

### 🔧 [API Reference](./reference/)
Technical documentation for developers:
- **Core API** - Simulator and configuration interfaces
- **Automata API** - Cellular automaton implementations
- **GUI API** - User interface components
- **Plugin System** - Extending LifeGrid with plugins
- **Advanced Modules** - Pattern analysis, visualization, statistics

### 🏗️ [Architecture](./architecture/)
Design and implementation details:
- **System Architecture** - High-level system design
- **Module Breakdown** - Component responsibilities
- **Data Flow** - How data moves through the system
- **Extension Points** - Where and how to extend LifeGrid

## Quick Navigation

- **New Users**: Start with [Getting Started](./tutorials/01_getting_started.md)
- **Experienced Users**: Check [Advanced Features Guide](./guides/advanced_features.md)
- **Developers**: Read [System Architecture](./architecture/system_architecture.md)
- **Plugin Authors**: See [Plugin Development Guide](./guides/plugin_development.md)

## What is LifeGrid?

LifeGrid is an interactive, extensible cellular automaton simulator built with Python and Tkinter. It provides:

- **Multiple Automata**: Conway's Life, HighLife, Immigration, Rainbow, Langton's Ant, Brian's Brain, Wireworld, and custom life-like rules
- **Interactive Drawing**: Draw patterns directly on the canvas with various drawing tools
- **Pattern Library**: Built-in patterns for quick experimentation
- **Export Capabilities**: Save patterns as JSON or PNG images
- **Statistics Tracking**: Monitor population metrics in real-time
- **Undo/Redo**: Full history support for easy experimentation
- **Plugin System**: Extend functionality with custom plugins
- **Performance Optimized**: Fast simulations using NumPy and SciPy

## Version Information

- **Current Version**: 3.0.0
- **Python Requirement**: 3.11+
- **License**: MIT

## Getting Help

- Check the relevant documentation section above
- Review [Frequently Asked Questions](./guides/faq.md)
- See [Troubleshooting Guide](./guides/troubleshooting.md)
- Report issues on [GitHub](https://github.com/James-HoneyBadger/LifeGrid)
