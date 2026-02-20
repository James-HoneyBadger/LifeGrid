# Configuration file for the Sphinx documentation builder.
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

# Allow Sphinx to import the package when building API docs
sys.path.insert(0, os.path.abspath("../src"))

# -- Project information -------------------------------------------------------
project = "LifeGrid"
copyright = "2024, Honey Badger Universe"
author = "Honey Badger Universe"
release = "3.2.0"

# -- General configuration -----------------------------------------------------
extensions = [
    "myst_parser",           # Markdown support
    "sphinx.ext.autodoc",    # API docs from docstrings
    "sphinx.ext.viewcode",   # Links to source
    "sphinx.ext.napoleon",   # Google/NumPy-style docstrings
]

# MyST-Parser: recognise both .rst and .md source files
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output ---------------------------------------------------
html_theme = "sphinx_rtd_theme"

# MyST heading anchors (auto-generate anchors for every heading level)
myst_heading_anchors = 3
