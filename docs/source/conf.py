"""
Configuration file for sphinx documentation builder.
"""

import os
import re
import sys
# Allow sphinx to find package for docstrings
sys.path.insert(0, os.path.abspath('../../src/'))

# -- Project information

project = "mlte"
copyright = "2022, Kyle Dotterrer"
author = "Kyle Dotterrer"

release = '0.1'
version = '0.1.2'

# -- General configuration
extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'autoapi.extension',
    'myst_parser'
]

autosummary_generate = True

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
}

intersphinx_disabled_domains = ["std"]

# -- Options for HTML output
html_theme = "sphinx_rtd_theme"

# -- Options for EPUB output
epub_show_urls = "footnote"

# -- Options for autoapi
autoapi_type = "python"
autoapi_dirs = ["../../src"]
autoapi_ignore = ["*internal*"]
autoapi_options = ["members", "special-members", "undoc-members", "imported-members"]
autoapi_add_toctree_entry = False
autoapi_python_class_content = "both"