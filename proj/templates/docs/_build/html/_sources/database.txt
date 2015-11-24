Database
========

Schema:
See the Django model at djangoOligo/app/models.py or view the actual data in
mySql.

Load new data by updating the json file at djangoOligo/app/fixtures/oligo.json
and using the django manager to load it with::
    python manage.py loaddata oligo.json
