# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import os
import sys

# Assumendo che conf.py sia in docs/source
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)
print(f"Adding {project_root} to sys.path for autodoc") 

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Chess TUI'
copyright = '2025, Costantino Lombardi'
author = 'Costantino Lombardi'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',     # Per estrarre docstring dal codice Python
    'sphinx.ext.napoleon',    # Per supportare docstring in stile Google/NumPy
    'sphinx.ext.intersphinx', # Utile per linkare documentazione esterna
    'sphinx_rtd_theme',       # Per usare il tema installato
]

templates_path = ['_templates']
exclude_patterns = []

language = 'it'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
