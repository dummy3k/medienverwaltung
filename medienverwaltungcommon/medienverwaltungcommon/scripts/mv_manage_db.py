#!/usr/bin/env python
import os.path
import sys
import medienverwaltungcommon.db_repo
#~ from migrate.versioning.shell import main
import migrate.versioning.shell

def main():
    repo_path = medienverwaltungcommon.db_repo.__file__
    repo_path = os.path.dirname(repo_path)
    repo_path = repo_path.replace('\\', '\\\\')
    #~ print "repo_path: %s" % repo_path

    migrate.versioning.shell.main(repository=repo_path)
