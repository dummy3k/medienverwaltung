#!/usr/bin/python
import os.path
import medienverwaltungcommon

#~ print "Hello World"
repo_path = medienverwaltungcommon.__file__
repo_path = os.path.dirname(repo_path)
repo_path = os.path.join(repo_path, 'db_repo')
print repo_path

