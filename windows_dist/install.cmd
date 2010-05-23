python26\python.exe python26\Scripts\virtualenv-script.py local.env
call local.env\Scripts\activate.bat

easy_install lxml==2.2.2
easy_install -f http://dl.dropbox.com/u/530973/py/index.html medienverwaltungweb

mv_manage_db manage manage_local.py --url=sqlite:///production.db
IF NOT EXIST "production.db" (
    echo "Creating production.db"
    python manage_local.py version_control
)
python manage_local.py upgrade
paster make-config medienverwaltungweb production.ini