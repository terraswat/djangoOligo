Installation
============

The application is up and running. These instructions may be used to install on another machine.

Required Toolchain
------------------

* python v2.6
* mysql v5.1.73
* apache v2.2
* django v1.6 (limited by python v2.6)
* sphinx v1.3b2 or later for building this documentation

The `django documention`_ has all of the information needed to
install the above.

.. _django documention: https://docs.djangoproject.com/en/1.6/

Install notes for CentOS VM
---------------------------

VERSIONS:

- our standard VM install has python2.6, apache2.2, mysql5.1.73
	- Django1.6 supports the above, but Django1.7 needs python2.7, so we'll go with Django1.6

PACKAGES THAT SOE SYS-ADMIN INSTALLS:

- look for required packages with:
	* rpm -qa
	* yum list
- required packages:
	* mysql-devel (for sql client)
	* zlib-devel (for sql client)
	* pip install mod_wsgi
	* pip install Django==1.6.8

HTTP:

- Important files:
	- /etc/httpd/conf/httpd.conf
	- /etc/httpd/conf.d/wsgi.conf
	- /var/log/httpd/error_log
	- /etc/httpd/modules/
	- /etc/httpd/conf.d

- /etc/httpd/conf.d/wsgi.conf::

     Alias /robots.txt /data/www/djangoOligo/static/robots.txt
     Alias /favicon.ico /data/www/djangoOligo/static/favicon.ico

     Alias /media/ /data/www/djangoOligo/media/
     Alias /static/ /data/www/djangoOligo/static/

     <Directory /data/www/djangoOligo/static>
     Order deny,allow
     Allow from all
     </Directory>

     <Directory /data/www/djangoOligo/media>
     Order deny,allow
     Allow from all
     </Directory>

     WSGIScriptAlias / /data/www/djangoOligo/proj/wsgi.py
     WSGIPythonPath /data/www/djangoOligo
        
     <Directory /data/www/djangoOligo/proj>
     Options Indexes FollowSymLinks
     <Files wsgi.py>
     Order deny,allow
     Allow from all
     </Files>
     </Directory>


- /data/www/djangoOligo/proj/wsgi.py::

     import os, sys
     sys.path.append('/data/www/djangoOligo/proj')

DJANGO:

- set STATIC settings in proj/settings.py
- djangoOligo/deploy.py::

	from fabric.api import *
	# Hosts to deploy onto
	env.hosts = ['satoligo.soe.ucsc.edu']
	# Where your project code lives on the server
	env.project_root = '/data/www/djangoOligo'
	def deploy_static():
		with cd(env.project_root):
			run('./manage.py collectstatic -v0 --noinput')

mySQL CLIENT:

- MySQL-devel to compile
- zlib-devel to compile
- build and install::

    python setup.py build &> build.log
    python setup.py install &> install.log
