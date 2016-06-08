#!/usr/bin/env python
from distutils.core import setup
setup(name='replace_dates_in_files',
      version='3.2',
      description='Met a jour les dates dans les noms de fichiers et le contenu des fichiers.',
      author='Charly Caulet',
      author_email='contact@charly-caulet.net',
      url='https://github.com/Chralu/replace_dates_in_files',
      install_requires=['watchdog'],
      packages=[],
      scripts=['replace_dates_in_files.py'],
      )
