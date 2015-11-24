Server Code
===========

The server code is in python making use of the django framework. There are
application modules to handle the details of the HTTP requests, and project
modules to handle the django settings.

Directory structure
-------------------
The source code is arranged according to django's default directory structure,
intermingled with the client sources, like so::

 djangoOligo
    app
    proj

**app** : files specific to the application.

**proj** : files for managing the application through django.

Source Code
-----------

.. toctree::
   app
   proj
