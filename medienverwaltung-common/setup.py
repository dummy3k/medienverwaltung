from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='medienverwaltungcommon',
      version=version,
      description="medienverwaltungcommon",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='',
      author_email='',
      url='',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      scripts=['scripts/mv_find_dvds.py',
               'scripts/mv_manage_db.py'],
      data_files=[('medienverwaltungcommon/db_repo', ['medienverwaltungcommon/db_repo/migrate.cfg'])],
      include_package_data=True,
      zip_safe=False,
        install_requires=[
            "SQLAlchemy==0.5.7", #0.6beta wont work for me
            "sqlalchemy-migrate"
        ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
