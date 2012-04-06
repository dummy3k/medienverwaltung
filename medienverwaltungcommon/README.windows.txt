How to install
==============

install python 2.7

install pip
http://stackoverflow.com/a/4921215/6297

pip install virtualenv

install mysql server
create mysql database / user

install: http://effbot.org/downloads/PIL-1.1.7.win32-py2.7.exe

\medienverwaltung>
run 'virtualenv local.env --system-site-packages' to create local environment

run 'local.env\scripts\activate.bat'

\medienverwaltung>cd medienverwaltungcommon
run 'python setup.py develop' to install dependencies

Create the Database:
====================



MySQL:
install driver: http://www.codegood.com/download/10/

create database and user:
SQL> CREATE DATABASE mv;
SQL> CREATE USER mv@localhost IDENTIFIED BY 'DykQDhpjCWDA3wdg';
SQL> GRANT ALL ON mv.* TO mv@localhost;
SQL> FLUSH PRIVILEGES;

\medienverwaltung>
mv_manage_db.exe manage manage_local.py --url=mysql://mv:DykQDhpjCWDA3wdg@localhost/mv?charset=utf8

Sqlite:
\medienverwaltung>
mv_manage_db.exe manage manage_local.py --url=sqlite:///production.db


Create Database:
medienverwaltung>python manage_local.py version_control
medienverwaltung>python manage_local.py upgrade

Upgrade / Downgrade Database to specific version with 0 as target version
medienverwaltung>mv_manage_db.exe version_control --url=sqlite:///tmp.db 
medienverwaltung>mv_manage_db.exe upgrade --url=sqlite:///tmp.db && mv_manage_db.exe downgrade --url=sqlite:///tmp.db 0

Other
=====

this might work:

FILE: /etc/init.d/medienverwaltung
source /var/www/medienverwaltung/env/bin/activate

case "$1" in
  start)
    paster serve --daemon --pid-file=/var/run/medienverwaltung.pid --log-file=/var/log/apache2/medienverwaltung.log /var/www/medienverwaltung/production.ini start
    ;;
  stop)
    paster serve --daemon --pid-file=/var/run/medienverwaltung.pid --log-file=/var/log/apache2/medienverwaltung.log /var/www/medienverwaltung/production.ini stop
    ;;
  restart)
    paster serve  --daemon --pid-file=/var/run/medienverwaltung.pid --log-file=/var/log/apache2/medienverwaltung.log /var/www/medienverwaltung/production.ini  restart
    ;;
  *)
    echo $"Usage: $0 {start|stop|restart}"
    exit 1
esac
update-rc.d medienverwaltung defaults
