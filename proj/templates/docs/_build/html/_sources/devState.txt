Current Development State
=========================

The code repository is at:

 | `https://github.com/ucscHexmap/ucscSatOligo <https://github.com/ucscHexmap/ucscSatOligo>`_
 
To make this application usable, a few things need to be done, outlined here.

**Load the Data**

Load oligo data using the django utility and json file::

 python manage.py loaddata oligo.json

**Too Much Data to Display**

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

**Genome Browser Link**

The genome browser link should be grayed-out when there is no actual link
to be constructed

Client should prefix genomeBrowser when updating the link upon oligo selection?
(I don't remember what I meant by this)

**Advertize the Site**

Tell search engines to search this app by updating proj/static/robots.txt

**Handy Django Utilities**

	- python manage.py shell
	- python manage.py syncdb
	- python manage.py sql app (optional)
	- python manage.py loaddata oligo.json
	- python manage.py collect static
