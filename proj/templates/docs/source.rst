Source Code
===========

The code repository is at:

 | `https://github.com/ucscHexmap/ucscSatOligo <https://github.com/ucscHexmap/djangoOligo>`_

Directory structure
-------------------
The source code uses django's default directory structure,
intermingling client and server sources, like so::

 djangoOligo
    app
       static
          css
             lib
          images
          js
             lib
       templates
          app
    proj
       static
       templates
          admin
          docs
    static

Below are explanations for the major directories:

**app** : files specific to the application, including the app server sources.

**app/static** : javascript, css and images, including libraries.

**app/templates/app** : html templates.

**proj** : files for managing the application through django, including the proj server sources.

**proj/static** : favicon.ico and robots.txt.

**proj/templates/admin** : source files for the django admin pages.

**proj/templates/docs** : this documention.

**static** : django gathers all static files here for easy access by apache.

Client Code
-----------
The client code is in javascript, css and html making use of django templates.

Libraries
^^^^^^^^^
Existing open-source libraries are leveraged as follows:

* **jquery** : web browser-agnostic utlities
* **underscore** : functional programming utilities
* **dataTables** : jquery plugin for the oligos table
* **jquery-ui** : UI utilities
* **select2** : jquery-ui plugin for the searchable drop-down selects

Source Code
^^^^^^^^^^^

.. toctree::
   :maxdepth: 2

   clientSource

Server Code
-----------
The server code is in python making use of the django framework. There are
'app' modules to handle content pages, and 'proj'
modules that mostly handle django negotiations with apache.

Source Code
^^^^^^^^^^^

.. toctree::
   app
   proj
