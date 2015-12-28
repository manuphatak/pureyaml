#!/usr/bin/env python
# coding=utf-8
import sys
from os.path import abspath, relpath
import sphinx.environment


def _warn_node(func):
    def wrapper(self, msg, node):
        if msg.startswith('nonlocal image URI found:'):
            return

        return func(self, msg, node)

    return wrapper


sphinx.environment.BuildEnvironment.warn_node = _warn_node(sphinx.environment.BuildEnvironment.warn_node)

sys.path.insert(0, abspath(relpath('../', __file__)))

import pureyaml

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.doctest', 'sphinx.ext.coverage', 'sphinx.ext.viewcode', ]

templates_path = ['_templates']

source_suffix = '.rst'

source_encoding = 'utf-8-sig'

master_doc = 'index'

# General information about the project.
project = 'pureyaml'
copyright = '2015, Manu Phatak'
author = pureyaml.__author__
version = pureyaml.__version__
release = pureyaml.__version__

# language = None
# today = ''
# today_fmt = '%B %d, %Y'
exclude_patterns = ['build']
# default_role = None
# add_function_parentheses = True
# add_module_names = True
# show_authors = False
pygments_style = 'sphinx'
# modindex_common_prefix = []
# keep_warnings = False

viewcode_import = True
# -- Options for HTML output -------------------------------------------
html_theme = 'sphinx_rtd_theme'
# html_theme_options = {}
# html_theme_path = []
# html_title = None
# html_short_title = None
# html_logo = None
# html_favicon = None
html_static_path = ['_static']
# html_last_updated_fmt = '%b %d, %Y'
# html_use_smartypants = True
# html_sidebars = {}
# html_additional_pages = {}
# html_domain_indices = True
# html_use_index = True
# html_split_index = False
# html_show_sourcelink = True
# html_show_sphinx = True
# html_show_copyright = True
# html_use_opensearch = ''
# html_file_suffix = None
htmlhelp_basename = 'pureyamldoc'

# -- Options for LaTeX output ------------------------------------------

latex_elements = {}
# 'papersize': 'letterpaper',
# 'pointsize': '10pt',
# 'preamble': '',

latex_documents = [(  # :off
    'index',
    'pureyaml.tex',
    'pureyaml Documentation',
    'Manu Phatak',
    'manual',
)]  # :on

# latex_logo = None
# latex_use_parts = False
# latex_show_pagerefs = False
# latex_show_urls = False
# latex_appendices = []
# latex_domain_indices = True

# -- Options for manual page output ------------------------------------

man_pages = [(  # :off
    'index',
    'pureyaml',
    'pureyaml Documentation',
    ['Manu Phatak'],
    1
)]  # :on
# man_show_urls = False

# -- Options for Texinfo output ----------------------------------------

texinfo_documents = [(  # :off
    'index',
    'pureyaml',
    'pureyaml Documentation',
    'Manu Phatak',
    'pureyaml',
    'One line description of project.',
    'Miscellaneous'
)]  # :on

# texinfo_appendices = []
# texinfo_domain_indices = True
# texinfo_show_urls = 'footnote'
# texinfo_no_detailmenu = False
