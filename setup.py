from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup
setup(name='hislain',
      description='Static Blog Publishing System',
      author='YuviPanda',
      author_email='me@yuvi.in',
      version='0.2',
      packages=['hislain'],
      scripts=['hislain/hislain'],
      install_requires=['PyYAML', 'Jinja2', 'simplejson', 'PyRSS2Gen', 'Markdown', 'python-dateutil']
      )
