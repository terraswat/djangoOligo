Modifications
=============

The code repository is at:

 | `https://github.com/ucscHexmap/ucscSatOligo <https://github.com/ucscHexmap/ucscSatOligo>`_

The code at /data/www/djangoOligo is a clone of the repository. For minor
changes where you are feeling lucky, the code could be changed on the production
server. You always have the repository version to fall back to.

For more extensive changes, you probably want to have another clone in a development
environment to keep the production database clean and not interrupt service from
the production site.

Current Development State
^^^^^^^^^^^^^^^^^^^^^^^^^
To make this application usable, a few things need to be done, outlined in the
sections below.

Load the Data
-------------

Too Much Data to Display
------------------------
The query to the server currently returns ALL data matching the search criteria.
This won't work for lots of data. The Datatables widget which shows the search
results can do 'infinite scrolling' or paging, neither of which our code has
implemented. Some notes on infinite scrolling and paging in datatables below.

http://datatables.net/

    - request should contain rowStartIndex, rowRetrieveMax & sortColumn
    - response should contain rowsMatched
    - define a default limit on return
    - rowRetrieveMax
    - rowSortMax defaults to rowRetrieveMax
    - turn off sorting by secondary columns when rowsMatched > rowSortMax ?
    - either infinite scrolling or paging can be used. Here is a quick comparison of the two methods

    +---------------------+----------------+--------------------+
    |                     | paging         | scrolling          |
    +=====================+================+====================+
    |    server retrieval | on sort        | on sort            |
    +---------------------+----------------+--------------------+
    |  view/retrieve more | query a range  | query a range      |
    +---------------------+----------------+--------------------+
    |    # rows retrieved | rowRetrieveMax | auto by dataTables |
    +---------------------+----------------+--------------------+
    |    # rows displayed | rowRetrieveMax | viewport height    |
    +---------------------+----------------+--------------------+
    |     change viewport | rowRetrieveMax | resize             |
    +---------------------+----------------+--------------------+

Genome Browser Link
-------------------
The genome browser link should be grayed-out when there is no actual link
to be constructed

Client should prefix genomeBrowser when updating the link upon oligo selection?
(What did I meant by this?)

Advertize the Site
------------------
Tell search engines to search this app by updating proj/static/robots.txt

Handy Django Utilities
----------------------
	- python manage.py shell
	- python manage.py syncdb
	- python manage.py sql app (optional)
	- python manage.py loaddata oligo.json
	- python manage.py collect static
