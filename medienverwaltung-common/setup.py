from setuptools import setup, find_packages
import sys, os

version = '0.0'

setup(name='medienverwaltung-common',
      version=version,
      description="medienverwaltung-common",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='',
      author_email='',
      url='',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      scripts=['scripts/mv_common_test.py',
               'scripts/mv_manage_db.py'],
      data_files=[('medienverwaltungcommon/db_repo', ['medienverwaltungcommon/db_repo/migrate.cfg'])],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
