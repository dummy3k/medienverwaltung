cd medienverwaltungcommon/
#~ python2.5 setup.py bdist_egg
#~ python2.6 setup.py bdist_egg
python setup.py bdist_egg || exit 1
cp dist/*.egg /home/dummy/Dropbox/Public/py/ || exit 1

cd ../medienverwaltung_cli/
#~ python2.5 setup.py bdist_egg
#~ python2.6 setup.py bdist_egg
python setup.py bdist_egg || exit 1
cp dist/*.egg /home/dummy/Dropbox/Public/py/ || exit 1

cd ../medienverwaltungweb || exit 1
#~ python2.5 setup.py bdist_egg
#~ python2.6 setup.py bdist_egg
python setup.py bdist_egg || exit 1
cp dist/*.egg /home/dummy/Dropbox/Public/py/ || exit 1

cd ..
