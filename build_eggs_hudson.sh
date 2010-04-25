if [ -d "unittest.env" ];
then
    echo "Unittest environment exists"
    do_setup="NO"
else
    echo "Creating unittest environment"
    virtualenv unittest.env || exit 1
    do_setup="YES"
fi

source unittest.env/bin/activate

cd medienverwaltung-common/
if [ $do_setup == "YES" ];
then
    python setup.py develop
fi
python2.5 setup.py bdist_egg || exit 1

cd ../medienverwaltungweb
#python2.5 setup.py compile_catalog || exit 1
if [ $do_setup == "YES" ];
then
    easy_install http://dl.dropbox.com/u/530973/py/python_amazon_product_api-0.2.3-py2.5.egg
    python setup.py develop
fi
nosetests || exit 1
python2.5 setup.py bdist_egg || exit 1

cd ../medienverwaltung_cli
python2.5 setup.py bdist_egg || exit 1
