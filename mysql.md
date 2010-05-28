---
title: MySQL
layout: default
---

MySql
=====

First create a user and database. I will wait here.

Now modify the following url to match your needs:

    mysql://USER:PASSWORD@localhost/DATABASE?charset=utf8

Create the database management script this way:

    mv_manage_db manage manage_local.py --url=mysql://USER:PASSWORD@localhost/DATABASE?charset=utf8
    chmod a+x local/manage_local.py
    ./local/manage_local.py version_control
    ./local/manage_local.py upgrade

And finally edit your <code>production.ini</code> and change this line:

    # SQLAlchemy database URL
    sqlalchemy.url = mysql://USER:PASSWORD@localhost/DATABASE?charset=utf8
    
