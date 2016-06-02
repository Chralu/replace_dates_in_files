#!/usr/bin/env python
from distutils.core import setup
setup(name='rename_files',
      version='3.2',
      description='Met a jour les dates dans les noms de fichiers et le contenu des fichiers.',
      author='Charly Caulet',
      author_email='ccaulet@sqli.com',
      url='https://github.com/Chralu/gandyn/',
      install_requires=['watchdog'],
      packages=[],
      scripts=['rename_files.py'],
      )