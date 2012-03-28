import sys
import os

cwd = os.path.dirname(os.path.realpath(__file__))
main_dir = os.path.normpath(cwd + '/../')
sys.path.append(main_dir)

#print sys.path

from config.all import *

language = 'gl'
html_logo = '../images/logos/logo-gl.png'
latex_logo = '../images/logos/logo-gl.png'
latex_documents = [
  ('index', 'e-cidadania.tex', u'Documentacion',
   u'Cidadania S. Coop. Galega', 'manual'),
]
