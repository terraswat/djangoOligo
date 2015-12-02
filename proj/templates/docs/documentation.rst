this Documentation
==================

Access the documentation pages at
`http://satoligo.soe.ucsc.edu/docs <http://satoligo.soe.ucsc.edu/docs>`_.

The source files for this documentation are in
djangoOligo/proj/templates/docs with docs.rst being the root source document.
Sphinx was used to build these doc pages.

The doc pages are in the same repository as the source code:

 | `https://github.com/ucscHexmap/ucscSatOligo <https://github.com/ucscHexmap/djangoOligo>`_

To build the docs in HTML form::

 cd djangoOligo/proj/templates/docs
 make html

The resulting html files will be in the _build directory in the docs directory,
where docs.html is the root page. This is the directory from which apache
serves the documentation pages.
