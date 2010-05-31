---
title: Debian Lenny
layout: default
---

Debian Lenny
============

Add this to your <code>/etc/apt/sources.list</code>:
 
    deb http://ftp.de.debian.org/debian/ testing main
    deb-src http://ftp.de.debian.org/debian/ testing main

Add the following to your <code>/etc/apt/preferences</code>. This file
might not exists.

    Package: *
    Pin: release a=testing
    Pin-Priority: 200

Install [PIL v1.17](http://www.pythonware.com/products/pil/):

    aptitude install -t testing python-imaging
