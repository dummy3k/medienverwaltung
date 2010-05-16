from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='medienverwaltung_cli',
      version=version,
      description="commandline interface for medienverwaltung",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='dummy3k',
      author_email='l4711@gmx.net',
      url='http://github.com/dummy3k/medienverwaltung',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          "feedparser"
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
