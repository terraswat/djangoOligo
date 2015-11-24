"""
views.py
^^^^^^^^
Respond to HTTP requests in the django context.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/class-based-views/
"""
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest, Http404, HttpRequest, QueryDict
from django.shortcuts import render_to_response
from django.core import serializers # extra?
from django.core.urlresolvers import reverse
from django.utils import html
from functools import reduce
import json
import itertools

from app.models import Array, Comment, Family, Oligo, Population, Population_total

popTotalCols = ('name', 'count', 'group', 'order', 'descr')

def keyPopTotal(name):
    row = {}
    for key in popTotalCols:
        row[key] = getattr(name, key)
    return row

arrayCols = ('name', 'descr')

def keyArray(name): # family table has the same columns as array
    row = {}
    for key in arrayCols:
        row[key] = getattr(name, key)
    return row

def init(request):
    """
    Respond to an HTTP request for the initial app context, at the URL ...app/init

    :return: population totals
    :return: satellite array names
	:return: satellite family names
    :return: total number of oligos in the database
    """
    if request.method == 'GET':
        popTotal = map(keyPopTotal, Population_total.objects.all())
        array = map(keyArray, Array.objects.all())
        family = map(keyArray, Family.objects.all())
        count = Oligo.objects.count()
        response = HttpResponse(json.dumps({
            'population_total': popTotal,
            'array': array,
            'family': family,
            'oligoCount': count,
        }))
        response['Content-Type'] = "application/json"
        return response
    return HttpResponseBadRequest(json.dumps({'error':'POST not supported'}))

oligoCols = ('primer', 'family', 'array', 'frequency', 'chr', 'bestStart', 'bestEnd', 'location', 'genomeBrowser', 'citation')

def keyOligo(primer):
    row = {}
    for key in oligoCols:
        row[key] = getattr(primer, key)
    return row

def deriveFields(oligo):
    # Calculate the average rating and round the frequency for this oligo.
    def sumRatings(sum, comment):
        return sum + comment.rating
    comments = Comment.objects.filter(primer=oligo['primer'])
    ratingSum = reduce(sumRatings, comments, 0)
    ratingCount = comments.count()
    if ratingCount > 0:
        oligo['rating'] = int(round(float(ratingSum)/float(ratingCount), 0))
    else:
        oligo['rating'] = 0
    oligo['frequency'] = round(oligo['frequency'], 2)
    return oligo

def filter(q):
    def popFilter(oligo):
        pops = Population.objects.filter(primer=oligo.primer)
        pops = pops.filter(name__iexact=q['population'])
        return (pops.count() > 0)

    if q.__contains__('primer'):
        objs = Oligo.objects.filter(primer__contains=q['primer'].upper())
    else:
        objs = Oligo.objects.all()
    if q.__contains__('family'):
        objs = objs.filter(family__iexact=q['family'])
    if q.__contains__('chr'):
        objs = objs.filter(chr=q['chr'])
    if q.__contains__('array'):
        objs = objs.filter(array__iexact=q['array'])
    if q.__contains__('population'):
        objs = itertools.ifilter(popFilter, objs)
    return objs

def prepOligos(parms):
    oligosData = map(deriveFields, map(keyOligo, filter(parms)))
    return oligosData

def oligos(request):
    """
    Respond to an HTTP request for filtered oligos, at the URL ...app/oligos
	We assume the data from the client is valid

    :param family: satellite family, if absent, no filtering on this
    :param chr: human chromosome, if absent, no filtering on this
    :param population: human population, if absent, no filtering on this
    :param array: array name, if absent, no filtering on this
    :param primer: oligo primer substring search
    :return: filtered oligos rows
    :return: total number of matches found in the database
    """
    if request.method == 'GET':
        parms = request.GET
        data = prepOligos(parms)
        response = HttpResponse(json.dumps( data ))
        response['Content-Type'] = "application/json"
        return response
    return HttpResponseBadRequest(json.dumps({'error':'POST not supported'}))

populationCols = ('primer', 'name', 'count')

def keyPopulation(name):
    row = {}
    for key in populationCols:
        row[key] = getattr(name, key)
    return row

def populations(request):
    """
    Respond to an HTTP request for an oligo's population counts, at the URL ...app/populations

    :param primer: oligo primer
    :return: population counts for the oligo
    :return: oligo primer
    """
    if request.method == 'GET':
        q = request.GET
        if q.__contains__('primer'):
            objs = Population.objects.filter(primer=q['primer'])
            data = map(keyPopulation, objs)
            response = HttpResponse(json.dumps( data ))
            response['Content-Type'] = "application/json"
            return response
        return HttpResponseBadRequest(json.dumps({'error':'primer is required'}))
    return HttpResponseBadRequest(json.dumps({'error':'POST not supported'}))

commentCols = ('primer', 'rating', 'text')

def keyComment(name):
    row = {}
    for key in commentCols:
        row[key] = getattr(name, key)
    return row

def findComments(primer):
    unordered = Comment.objects.filter(primer=primer)
    objs = sorted(unordered, key=lambda comment: comment.id, reverse=True)
    data = map(keyComment, objs)
    response = HttpResponse(json.dumps({'primer': primer, 'data': data}))
    response['Content-Type'] = "application/json"
    return response

def comments(request):
    """
    Respond to an HTTP request for an oligo's comments, at the URL ...app/comments

    :param primer: oligo primer
    :return: comments
    :return: oligo primer
    """
    if request.method == 'GET':
        q = request.GET
        if q.__contains__('primer'):
            primer = q['primer']
            return findComments(primer)
        return HttpResponseBadRequest(json.dumps({'error': 'primer is required'}))
    return HttpResponseBadRequest(json.dumps({'error':'POST not supported'}))

def addComment(request):
    """
    Respond to an HTTP request to add a comment to an oligo, at the URL ...app/addComment

    :param primer: oligo primer
    :param rating: user's rating
    :type rating: 1 - 5
    :param comment: user's comment
    :return: new comment list
    """
    if request.method == 'GET':
        q = request.GET
        if q.__contains__('primer'):
            if q.__contains__('rating'):
                rating = q['rating']
            else:
                rating = 0;
            if q.__contains__('text'):
                text = html.escape(q['text']) #escape evil embedded html
            elif q.__contains__('rating') == False:
                return HttpResponseBadRequest(json.dumps({'error': 'at least one of rating or text is required'}))
            else:
                text = '';
            comment = Comment(
                primer = q['primer'],
                rating = rating,
                text = text
            )
            comment.save()
            return findComments(q['primer'])
        return HttpResponseBadRequest(json.dumps({'error': 'primer is required'}))
    return HttpResponseBadRequest(json.dumps({'error':'POST not supported'}))

def help(request):
    return render_to_response('app/help.html')

def index(request):
    return render_to_response('app/index.html')
