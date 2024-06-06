import os
import sys
sys.path.insert(0, os.path.abspath('..'))

project = 'AparatLib'
author = 'Abol'
release = '0.4.1'

extensions = [
    'myst_parser',  # Extension for parsing Markdown files
    'sphinx.ext.autodoc',  # Include documentation from docstrings
    'sphinx.ext.napoleon',  # Support for NumPy and Google style docstrings
    'sphinx.ext.viewcode',  # Add links to highlighted source code
]

templates_path = ['_templates']
exclude_patterns = []

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

source_suffix = {
    '.rst': 'restructuredtext',
    '.txt': 'restructuredtext',
    '.md': 'markdown',
}

# -- Options for autodoc extension -------------------------------------------

autodoc_member_order = 'bysource'

# -- Options for Napoleon extension ------------------------------------------

napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True

# -- Custom CSS for dark mode ------------------------------------------------

def setup(app):
    app.add_css_file('custom.css')
    app.add_js_file('custom.js')
