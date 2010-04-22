##cd medienverwaltung-common/
##python2.5 setup.py bdist_egg
##python2.6 setup.py bdist_egg
##cp dist/*.egg /home/dummy/Dropbox/Public/py/

cd medienverwaltungweb
python2.5 setup.py bdist_egg
#python2.6 setup.py bdist_egg
cp dist/*.egg /home/dummy/Dropbox/Public/py/

cd ..
