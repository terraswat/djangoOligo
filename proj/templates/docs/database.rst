Database
========

Django Admin
------------

The django admin pages provide convenient access to the database without directly
using SQL. Access these pages at
`http://satoligo.soe.ucsc.edu/admin <http://satoligo.soe.ucsc.edu/admin>`_.

As new satellite array names are added, they should be added to the arrays table
to populate the application's drop down list for searches.

The sources specific to the admin pages are:

 | djangoOligo/proj/templates/admin/
 |	base_site.html
 |	index.html
 | djangoOligo/app/
 |	admin.py

Loading Data
------------
To load small amounts of data, the admin pages may be used.

To load the oligos, a django command line utility may be used to load json-formatted
data like so::

 cd djangoOligo/app/fixtures
 python manage.py loaddata oligo.json

Or, if a tsv file is more convenient, there is a tsv-to-json converter::

 cd djangoOligo/app/fixtures
 python tsv2json.py oligo.tsv
 python manage.py loaddata oligo.json

Schema
------
The admin pages will give you a high-level view of the data tables. For more
details, see the django model at djangoOligo/app/models.py or view the actual
database in mySql.

MySQL
-----
You can get into the mySql shell with::

 mysql -u admin -p
