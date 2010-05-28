---
title: Downloads
layout: default
---

Downloads
=========

Windows
-------
The installer contains a basic python environment and will download the
latest version automatically.
Because of this you have to be connected to the Internet while
installing it.
You may even install it as an non administrative user.
You won't even need a database installed, because Sqlite will be used.

If you did not understand any this, never mind. Just download and run it
it will work.

* [Install_Medienverwaltung.exe](http://dl.dropbox.com/u/530973/Install_Medienverwaltung.exe)

Debian, Ubuntu
--------------

Install needed dependencies:

    sudo aptitude install build-essential python-dev libxslt1-dev libxml2-dev
    
Create and activate virtual environment
    
    virtualenv production.env
    production.env\Scripts\activate.bat
    
Easy install the medienverwaltungweb package

    easy_install -f http://dl.dropbox.com/u/530973/py/index.html medienverwaltungweb
    
Create a Sqlite database. If you want a MySql database,
[look here](mysql.html).

    mv_manage_db manage manage_local.py --url=sqlite:///production.db
    hmod a+x local/manage_local.py
    ./local/manage_local.py version_control
    ./local/manage_local.py upgrade
    
Create the config file

    paster make-config medienverwaltungweb production.ini

And finally start the webserver.

    paster serve production.ini

If everything works out, you may want to create an
[init-script](init-script.html).


Source Code
-----------

The source code is available at
[GitHub](http://dummy3k.github.com/medienverwaltung/).

Basically you just clone the source and follow the steps above for your
plattform. But instead of the <code>easy_install</code> part you run
<code>python setup.py develop</code>

    git clone git://github.com/dummy3k/medienverwaltung.git

    cd medienverwaltung
    virtualenv mv.env
    mv.env\Scripts\activate.bat

    cd medienverwaltungcommon
    python setup.py develop

    cd /medienverwaltungweb
    python setup.py develop
    
