import os
import sys
sys.path.insert(0, os.path.abspath('..'))

project = 'Your Project Name'
author = 'Your Name'
release = '0.1'

extensions = [
    'myst_parser',
]

templates_path = ['_templates']
exclude_patterns = []

html_theme = 'alabaster'
html_static_path = ['_static']

source_suffix = {
    '.rst': 'restructuredtext',
    '.txt': 'restructuredtext',
    '.md': 'markdown',
}
