#!/usr/bin/env python

from distutils.core import setup

setup(name='GADjango',
      version='0.0.1',
      description='Simple Performance data sender to Google Analytics',
      author='Tomas Sirny',
      author_email='tsirny@gmail.com',
      url='https://github.com/junckritter/gadjango',
      packages=['gadjango'],
      package_data = { 'gadjango': [ 'templates/gadjango/*.html']},
     )
