Database
========

Schema:
See the Django model at djangoOligo/app/models.py or view the actual data in
mySql.

Load new data by creating a json or tsv file for the database table of interest.
Example data files and a tsv-to-json converter (tsv2json.py) are at
djangoOligo/app/fixtures.

The json file may then be loaded into the database using a django utility::

 python manage.py loaddata oligo.json

 TBD: executed from which directory?
