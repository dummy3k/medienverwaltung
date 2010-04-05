This file is for you to describe the medienverwaltungweb application. Typically
you would include information such as the information below:

Installation and Setup
======================

Install ``medienverwaltungweb`` using easy_install::

    easy_install medienverwaltungweb
    (this won't work)

Make a config file as follows::

    paster make-config medienverwaltungweb config.ini

Tweak the config file and especially edited these values:
    - language
    - sqlalchemy.url
    - Amazon.AccessKeyID
    - Amazon.SecretAccessKey
    
Then setup the application::

    paster setup-app config.ini

Then you are ready to go.

Todo for devlopment:
    sudo easy_install babel

Thanks goto:
- http://deepliquid.com/content/Jcrop.html
