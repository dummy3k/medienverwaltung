cd medienverwaltung-common/
python2.5 setup.py bdist_egg || exit 1

cd ../medienverwaltungweb
python2.5 setup.py bdist_egg || exit 1

cd ../medienverwaltung_cli
python2.5 setup.py bdist_egg || exit 1
