Client Code
===========

The client code is in javascript, css and html making use of django templates.

Libraries
----------
Existing open-source libraries are leveraged as follows:

* **jquery** : web browser-agnostic utlities
* **underscore** : functional programming utilities
* **dataTables** : jquery plugin for the oligos table
* **jquery-ui** : UI utilities
* **select2** : jquery-ui plugin for the searchable drop-down selects

Directory structure
-------------------
The source code is arranged according to django's default directory structure,
intermingled with the server sources, like so::

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

Source Code
-----------

The client source code is detailed at the following links.

.. toctree::
   :maxdepth: 2

   clientSource
