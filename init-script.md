---
title: Init Script
layout: default
---

Init Script
===========

Create a file at <code>/etc/init.d/medienverwaltung</code> with this
content:

    #!/usr/bin/env bash

    #uncomment and edit to use virtualenv
    #source /var/www/medienverwaltung/env/bin/activate

    ini_path="/path/to/config.ini"
    instance_name="default"
    pid_file=/var/run/medienverwaltung-$instance_name.pid
    log_file=/var/log/apache2/medienverwaltung-$instance_name.log

    case "$1" in
        ("start")
            paster serve --daemon --pid-file=$pid_file --log-file=$log_file $ini_path start
            ;;
        (stop)
            paster serve --daemon --pid-file=$pid_file --log-file=$log_file ${ini_path} stop
            ;;
        ("restart")
            paster serve --daemon --pid-file=$pid_file --log-file=$log_file $ini_path restart
            ;;
        (*) 
            echo $"Usage: $0 {start|stop|restart}"
            exit 1
    esac

And put it to use:

    chmod a+x /etc/init.d/medienverwaltung
    update-rc.d medienverwaltung defaults
