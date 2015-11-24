"""
models.py
^^^^^^^^^
Define the database schema using django models.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/db/
"""
from django.db import models

class Oligo(models.Model):
    primer = models.CharField("Primer (5'-> 3')", primary_key=True, max_length=255)
    family = models.CharField('Satellite Family', max_length=255)
    array = models.CharField('Array Name', max_length=255)
    frequency = models.FloatField('Frequency', default=0)
    chr = models.CharField('Human Chromosome', max_length=2, default='1')
    bestStart = models.IntegerField('Best Start', default=0)
    bestEnd = models.IntegerField('Best End', default=0)
    location = models.CharField('Location with 10% le', max_length=255)
    genomeBrowser = models.CharField('UCSC Genome Browser', max_length=1023, blank=True, null=True)
    citation = models.CharField('Citations', max_length=2047, blank=True, null=True)
    def __unicode__(self):
        return self.primer

class Population(models.Model):
    primer = models.CharField('Primer', max_length=255)
    name = models.CharField('Name', max_length=255)
    count = models.IntegerField('Count', default=0)
    def __unicode__(self):
        return self.primer + ': ' + self.name

class Population_total(models.Model):
    name = models.CharField('Name', primary_key=True, max_length=3)
    group = models.CharField('Group', max_length=80, default='')
    count = models.IntegerField('Count', default=0)
    order = models.IntegerField('Order of Appearance', default=0)
    descr = models.CharField('Description', max_length=255)
    def __unicode__(self):
        return self.name

class Comment(models.Model):
    primer = models.CharField('Primer', max_length=255)
    rating = models.IntegerField('Rating', default=0)
    text = models.TextField('Comment', max_length=2047, blank=True)
    def __unicode__(self):
        return self.primer

class Array(models.Model):
    name = models.CharField('Name', primary_key=True, max_length=255)
    descr = models.CharField('Description', max_length=255, blank=True)
    def __unicode__(self):
        return self.name

class Family(models.Model):
    name = models.CharField('Name', primary_key=True, max_length=255)
    descr = models.CharField('Description', max_length=255, blank=True)
    def __unicode__(self):
        return self.name
