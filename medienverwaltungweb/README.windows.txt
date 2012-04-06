Installation and Setup
======================

Prerequisite:
	see medienverwaltungcommon\README

	active local environment
	medienverwaltung\local.env\scripts/activate

	easy_install --allow-hosts=lxml.de,*.python.org lxml==2.3
    pip install babel
	
    medienverwaltungweb>python setup.py develop

	pip install repoze.who.plugins.openid

Make a config file as follows::

    medienverwaltungweb>paster make-config medienverwaltungweb config.ini
	

Tweak the config file and especially edited these values:
    - language
    - sqlalchemy.url
	- Register at Amazon: http://aws.amazon.com:
		- modify Amazon.AccessKeyID
		- modify Amazon.SecretAccessKey

Then setup the application:
	medienverwaltungweb>paster setup-app config.ini

Then you are ready to go:
	medienverwaltungweb>paster serve config.ini --reload




Thanks goto:
- http://deepliquid.com/content/Jcrop.html
