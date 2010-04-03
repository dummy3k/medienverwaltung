python setup.py extract_messages --no-location
python setup.py update_catalog -l de
poedit medienverwaltungweb/i18n/de/LC_MESSAGES/medienverwaltungweb.po
python setup.py compile_catalog
touch development.ini
