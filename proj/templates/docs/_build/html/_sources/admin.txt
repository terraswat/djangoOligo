Django Admin
============

Access the admin pages at `http://satoligo.soe.ucsc.edu/admin <http://satoligo.soe.ucsc.edu/admin>`_.

The django admin pages give convenient access to the database without directly
using SQL.

As new satellite array names are added, they should be added to the arrays table
to populate the application's drop down list for searches.

The sources specific to the admin pages are:

 | djangoOligo/proj/templates/admin/
 |	base_site.html
 |	index.html
 | djangoOligo/app/
 |	admin.py

