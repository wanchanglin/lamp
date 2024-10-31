# Configuration file for the Sphinx documentation builder.
# wl-25-08-2024, Sun: commence
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup ----------------------------------------------------------
#
# If extensions (or modules to document with autodoc) are in another
# directory, add these directories to sys.path here. If the directory is
# relative to the documentation root, use os.path.abspath to make it
# absolute, like shown here.
#
import os
import sys
# wl-26-08-2024, Mon: Source code dir relative to this file. You need to
# change the path if needed.
sys.path.insert(0, os.path.abspath('..'))

# -- Project information ------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'LAMP - Liverpool Annotation of metabolites using Mass sPectrometry'
copyright = '2024, Wanchang Lin, Warwick Dunn'
author = 'Wanchang Lin, Warwick Dunn'
release = '1.0.1'

# -- General configuration ---------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.autosummary',
    # 'sphinx.ext.coverage',
    # 'sphinx.ext.doctest',
    # 'sphinx.ext.todo',
    # 'sphinx.ext.mathjax'
    'nbsphinx'
]
autosummary_generate = True  # Turn on sphinx.ext.autosummary

napoleon_google_docstring = False
napoleon_use_param = False
napoleon_use_ivar = True

templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
source_suffix = {'.rst': 'restructuredtext'}

# The main toctree document.
master_doc = 'index'

# -- Options for HTML output ---------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
# html_static_path = ['_static']
