#!/usr/bin/env python
# coding=utf-8
import sys
from os.path import abspath, relpath

import sphinx.environment

sys.path.insert(0, abspath(relpath('../', __file__)))
import pureyaml


def _warn_node(func):
    def wrapper(self, msg, node):
        if msg.startswith('nonlocal image URI found:'):
            return

        return func(self, msg, node)

    return wrapper


sphinx.environment.BuildEnvironment.warn_node = _warn_node(sphinx.environment.BuildEnvironment.warn_node)


# noinspection PyUnusedLocal
def doctree_read_handler(app, doctree):
    """
    Add 'orphan' to metadata for partials

    :type app: sphinx.application.Sphinx
    :type doctree: docutils.nodes.document
    """
    # noinspection PyProtectedMember
    docname = sys._getframe(2).f_locals['docname']
    if docname.startswith('_partial'):
        app.env.metadata[docname]['orphan'] = True


def autodoc_skip_member_handler(app, what, name, obj, skip, options):
    """
    Skip un parseable functions.

    :type app: sphinx.application.Sphinx
    :param str what: the type of the object which the docstring belongs to
        (one of "module", "class", "exception", "function", "method", "attribute")
    :param str name: the fully qualified name of the object
    :param type obj: the object itself
    :param bool skip: a boolean indicating if autodoc will skip this member
    :param sphinx.ext.autodoc.Options options: the options given to the directive
    :rtype: bool
    """
    if 'YAMLTokens' in name:
        return True
    return False


def setup(app):
    """
    Silence warnings that partials are not included in toctree.

    :type app: sphinx.application.Sphinx
    """
    app.connect('doctree-read', doctree_read_handler)
    app.connect('autodoc-skip-member', autodoc_skip_member_handler)


extensions = [  # :off
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.coverage',
    'sphinx.ext.viewcode',
]  # :on

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
exclude_patterns = ['**/tokens.py']
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
