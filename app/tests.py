"""
tests.py
^^^^^^^^
Unit tests for the python code.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/testing/
"""
from django.core.urlresolvers import reverse
import json
from django.test import TestCase
from app.models import Array, Comment, Family, Oligo, Population, Population_total
from app.views import commentCols, keyComment, oligoCols, keyOligo, deriveFields

def create_population_total(name, group, count, order, descr):
    return Population_total.objects.create(name = name, group = group, count = count, order=order, descr = descr)

def create_population(primer, name, count):
    return Population.objects.create(primer = primer, name = name, count = count)

def create_array(name, descr):
    return Array.objects.create(name = name, descr = descr)

def create_comment(primer, rating, text):
    return Comment.objects.create(primer = primer, rating = int(rating), text = text)

def create_family(name, descr):
    return Family.objects.create(name = name, descr = descr)

def create_oligo(primer, family, array, frequency, chr, bestStart, bestEnd, location, genomeBrowser, citation):
    return Oligo.objects.create(primer = primer, family = family, array = array, frequency = frequency, chr = chr, bestStart = bestStart, bestEnd = bestEnd, location = location, genomeBrowser = genomeBrowser, citation = citation)

class Index(TestCase):

    def test_index_url_exists(self):
        """
        the url app/ should exist
        """
        response = self.client.get(reverse('app:index'))
        self.assertEqual(response.status_code, 200)

class Init(TestCase):

    def test_init_url_returns_population_totals(self):
        """
        init() should return all of the population_total rows
        """
        create_population_total('pt1', 'pt1group', 66, 1, 'popTotal1 descr')
        create_population_total('pt2', 'pt2group', 88, 2, 'popTotal2 descr')
        response = self.client.get(reverse('app:init'))
        self.assertEqual(response.status_code, 200)
        obj = json.loads(response.content)
        exp = json.loads('{"population_total": [{"count": 66, "name": "pt1", "group": "pt1group", "descr": "popTotal1 descr", "order": 1}, {"count": 88, "name": "pt2", "group": "pt2group", "descr": "popTotal2 descr", "order": 2}]}')
        self.assertEqual(obj['population_total'], exp['population_total'])

    def test_init_url_returns_arrays(self):
        """
        init() should return all of the array rows
        """
        create_array('array1', 'array1 descr')
        create_array('array2', 'array2 descr')
        response = self.client.get(reverse('app:init'))
        self.assertEqual(response.status_code, 200)
        obj = json.loads(response.content)
        exp = json.loads('{"array": [{"name": "array1", "descr": "array1 descr"}, {"name": "array2", "descr": "array2 descr"}]}')
        self.assertEqual(obj['array'], exp['array'])

    def test_init_url_returns_familys(self):
        """
        init() should return all of the family rows
        """
        create_family('family1', 'family1 descr')
        create_family('family2', 'family2 descr')
        response = self.client.get(reverse('app:init'))
        self.assertEqual(response.status_code, 200)
        obj = json.loads(response.content)
        exp = json.loads('{"family": [{"name": "family1", "descr": "family1 descr"}, {"name": "family2", "descr": "family2 descr"}]}')
        self.assertEqual(obj['family'], exp['family'])

    def test_init_url_returns_oligoCount(self):
        """
        init() should return the total number of oligos in the database
        """
        create_oligo('p1', 'f1', 'a1', '1', '1', '111', '1111', 'l1', 'g1', 'c1')
        create_oligo('p2', 'f2', 'a2', '2', '2', '222', '2222', 'l2', 'g2', 'c2')
        response = self.client.get(reverse('app:init'))
        self.assertEqual(response.status_code, 200)
        obj = json.loads(response.content)
        self.assertEqual(obj['oligoCount'], 2)

class Oligos(TestCase):

    def test_derived_oligo_rating(self):
        """
        derivedFields should calculate the average rating of an oligo
        """
        create_oligo('p2', 'f2', 'a2', '2', '2', '222', '2222', 'l2', 'g2', 'c2')
        create_comment('p1', '1', 'a p1 comment')
        create_comment('p2', '2', 'a p2 comment')
        create_comment('p2', '4', 'another p2 comment')
        oligos = map(keyOligo, Oligo.objects.all())
        obj = deriveFields(oligos[0])
        self.assertEqual(obj['rating'], 3)

    def test_derived_oligo_frequency(self):
        """
        derivedFields should round the frequency of an oligo to two decimal places
        """
        create_oligo('p2', 'f2', 'a2', '0.125', '2', '222', '2222', 'l2', 'g2', 'c2')
        create_comment('p1', '1', 'a p1 comment')
        create_comment('p2', '2', 'a p2 comment')
        create_comment('p2', '4', 'another p2 comment')
        oligos = map(keyOligo, Oligo.objects.all())
        obj = deriveFields(oligos[0])
        self.assertEqual(obj['frequency'], 0.13)

    def test_oligos_url_with_all_filters(self):
        """
        the url app/oligos/ should return matching oligos when all filters are supplied
        """
        create_oligo('P1', 'f1', 'a1', '1', '1', '111', '1111', 'l1', 'g1', 'c1')
        create_oligo('P2', 'f2', 'a2', '2', '2', '222', '2222', 'l2', 'g2', 'c2') # the one
        create_oligo('P22', 'f1', 'a2', '2', '2', '222', '2222', 'l2', 'g2', 'c2')
        create_oligo('P222', 'f2', 'a1', '2', '2', '222', '2222', 'l2', 'g2', 'c2')
        create_oligo('P2222', 'f2', 'a2', '2', '1', '222', '2222', 'l2', 'g2', 'c2')
        create_population('P2', 'pop2', '22')
        response = self.client.get(reverse('app:oligos'), {'primer': 'P2', 'family': 'f2', 'array': 'a2', 'chr': '2', 'population': 'pop2'})
        self.assertEqual(response.status_code, 200)
        obj = json.loads(response.content)
        exp = json.loads('[{"rating": 0, "bestStart": 222, "family": "f2", "citation": "c2", "genomeBrowser": "g2", "bestEnd": 2222, "chr": "2", "frequency": 2.0, "location": "l2", "array": "a2", "primer": "P2"}]')
        self.assertEqual(obj, exp)

    def test_oligos_url_with_all_filters_case_insensitive(self):
        """
        the url app/oligos/ should return matching oligos using case-insensitive matching
        """
        create_oligo('P1', 'f1', 'a1', '1', '1', '111', '1111', 'l1', 'g1', 'c1')
        create_oligo('P2', 'f2', 'a2', '2', '2', '222', '2222', 'l2', 'g2', 'c2') # the one
        create_oligo('P22', 'f1', 'a2', '2', '2', '222', '2222', 'l2', 'g2', 'c2')
        create_oligo('P222', 'f2', 'a1', '2', '2', '222', '2222', 'l2', 'g2', 'c2')
        create_oligo('P2222', 'f2', 'a2', '2', '1', '222', '2222', 'l2', 'g2', 'c2')
        create_population('p2', 'pop2', '22')
        response = self.client.get(reverse('app:oligos'), {'primer': 'P2', 'family': 'f2', 'array': 'a2', 'chr': '2', 'population': 'pop2'})
        self.assertEqual(response.status_code, 200)
        obj = json.loads(response.content)
        exp = json.loads('[{"rating": 0, "bestStart": 222, "family": "f2", "citation": "c2", "genomeBrowser": "g2", "bestEnd": 2222, "chr": "2", "frequency": 2.0, "location": "l2", "array": "a2", "primer": "P2"}]')
        self.assertEqual(obj, exp)


    def test_oligos_url_without_any_filters(self):
        """
        the url app/oligos/ should return matching oligos when no filters are supplied
        """
        create_oligo('p1', 'f1', 'a1', '1', '1', '111', '1111', 'l1', 'g1', 'c1')
        create_oligo('p2', 'f2', 'a2', '2', '2', '222', '2222', 'l2', 'g2', 'c2') # the one
        response = self.client.get(reverse('app:oligos'), {})
        self.assertEqual(response.status_code, 200)
        obj = json.loads(response.content)
        exp = json.loads('[{"rating": 0, "bestStart": 111, "family": "f1", "citation": "c1", "genomeBrowser": "g1", "bestEnd": 1111, "chr": "1", "frequency": 1.0, "location": "l1", "array": "a1", "primer": "p1"}, {"rating": 0, "bestStart": 222, "family": "f2", "citation": "c2", "genomeBrowser": "g2", "bestEnd": 2222, "chr": "2", "frequency": 2.0, "location": "l2", "array": "a2", "primer": "p2"}]')
        self.assertEqual(obj, exp)

    def test_oligos_url_with_a_filter_with_no_matches(self):
        """
        the url app/oligos/ should return no oligos when nothing matches
        """
        create_oligo('p1', 'f1', 'a1', '1', '1', '111', '1111', 'l1', 'g1', 'c1')
        create_oligo('p2', 'f2', 'a2', '2', '2', '222', '2222', 'l2', 'g2', 'c2') # the one
        response = self.client.get(reverse('app:oligos'), {'primer': 'p3'})
        self.assertEqual(response.status_code, 200)
        obj = json.loads(response.content)
        exp = json.loads('[]')
        self.assertEqual(obj, exp)

    def test_oligos_url_with_population_filter(self):
        """
        the url app/oligos/ should return matching oligos with population filter
        """
        create_oligo('p1', 'f1', 'a1', '1', '1', '111', '1111', 'l1', 'g1', 'c1')
        create_oligo('p2', 'f2', 'a2', '2', '2', '222', '2222', 'l2', 'g2', 'c2') # the one
        create_population('p2', 'pop2', '22')
        response = self.client.get(reverse('app:oligos'), {'population': 'pop2'})
        self.assertEqual(response.status_code, 200)
        obj = json.loads(response.content)
        exp = json.loads('[{"rating": 0, "bestStart": 222, "family": "f2", "citation": "c2", "genomeBrowser": "g2", "bestEnd": 2222, "chr": "2", "frequency": 2.0, "location": "l2", "array": "a2", "primer": "p2"}]')
        self.assertEqual(obj, exp)

    def test_oligos_url_with_chr_filter(self):
        """
        the url app/oligos/ should return matching oligos with chr filter
        """
        create_oligo('p1', 'f1', 'a1', '1', '1', '111', '1111', 'l1', 'g1', 'c1')
        create_oligo('p2', 'f2', 'a2', '2', '2', '222', '2222', 'l2', 'g2', 'c2') # the one
        response = self.client.get(reverse('app:oligos'), {'chr': '2'})
        self.assertEqual(response.status_code, 200)
        obj = json.loads(response.content)
        exp = json.loads('[{"rating": 0, "bestStart": 222, "family": "f2", "citation": "c2", "genomeBrowser": "g2", "bestEnd": 2222, "chr": "2", "frequency": 2.0, "location": "l2", "array": "a2", "primer": "p2"}]')
        self.assertEqual(obj, exp)

    def test_oligos_url_with_array_filter(self):
        """
        the url app/oligos/ should return matching oligos with array filter
        """
        create_oligo('p1', 'f1', 'a1', '1', '1', '111', '1111', 'l1', 'g1', 'c1')
        create_oligo('p2', 'f2', 'a2', '2', '2', '222', '2222', 'l2', 'g2', 'c2') # the one
        response = self.client.get(reverse('app:oligos'), {'array': 'a2'})
        self.assertEqual(response.status_code, 200)
        obj = json.loads(response.content)
        exp = json.loads('[{"rating": 0, "bestStart": 222, "family": "f2", "citation": "c2", "genomeBrowser": "g2", "bestEnd": 2222, "chr": "2", "frequency": 2.0, "location": "l2", "array": "a2", "primer": "p2"}]')
        self.assertEqual(obj, exp)

    def test_oligos_url_with_family_filter(self):
        """
        the url app/oligos/ should return matching oligos with family filter
        """
        create_oligo('p1', 'f1', 'a1', '1', '1', '111', '1111', 'l1', 'g1', 'c1')
        create_oligo('p2', 'f2', 'a2', '2', '2', '222', '2222', 'l2', 'g2', 'c2') # the one
        response = self.client.get(reverse('app:oligos'), {'family': 'f2'})
        self.assertEqual(response.status_code, 200)
        obj = json.loads(response.content)
        exp = json.loads('[{"rating": 0, "bestStart": 222, "family": "f2", "citation": "c2", "genomeBrowser": "g2", "bestEnd": 2222, "chr": "2", "frequency": 2.0, "location": "l2", "array": "a2", "primer": "p2"}]')
        self.assertEqual(obj, exp)

    def test_oligos_url_with_filter_matching_start_of_primer(self):
        """
        the url app/oligos/ should return matching oligos with a filter matching the start of the primer string
        """
        create_oligo('P1', 'f1', 'a1', '1', '1', '111', '1111', 'l1', 'g1', 'c1')
        create_oligo('P22', 'f2', 'a2', '2', '2', '222', '2222', 'l2', 'g2', 'c2') # the one
        response = self.client.get(reverse('app:oligos'), {'primer': 'p2'})
        self.assertEqual(response.status_code, 200)
        obj = json.loads(response.content)
        exp = json.loads('[{"rating": 0, "bestStart": 222, "family": "f2", "citation": "c2", "genomeBrowser": "g2", "bestEnd": 2222, "chr": "2", "frequency": 2.0, "location": "l2", "array": "a2", "primer": "P22"}]')
        self.assertEqual(obj, exp)

    def test_oligos_url_with_filter_matching_end_of_primer(self):
        """
        the url app/oligos/ should return matching oligos with a filter matching the end of the primer string
        """
        create_oligo('P1', 'f1', 'a1', '1', '1', '111', '1111', 'l1', 'g1', 'c1')
        create_oligo('P22', 'f2', 'a2', '2', '2', '222', '2222', 'l2', 'g2', 'c2') # the one
        response = self.client.get(reverse('app:oligos'), {'primer': '22'})
        self.assertEqual(response.status_code, 200)
        obj = json.loads(response.content)
        exp = json.loads('[{"rating": 0, "bestStart": 222, "family": "f2", "citation": "c2", "genomeBrowser": "g2", "bestEnd": 2222, "chr": "2", "frequency": 2.0, "location": "l2", "array": "a2", "primer": "P22"}]')
        self.assertEqual(obj, exp)

    def test_oligos_url_with_filter_matching_middle_of_primer(self):
        """
        the url app/oligos/ should return matching oligos with a filter matching the middle of the primer string
        """
        create_oligo('p1', 'f1', 'a1', '1', '1', '111', '1111', 'l1', 'g1', 'c1')
        create_oligo('p21', 'f2', 'a2', '2', '2', '222', '2222', 'l2', 'g2', 'c2') # the one
        response = self.client.get(reverse('app:oligos'), {'primer': '2'})
        self.assertEqual(response.status_code, 200)
        obj = json.loads(response.content)
        exp = json.loads('[{"rating": 0, "bestStart": 222, "family": "f2", "citation": "c2", "genomeBrowser": "g2", "bestEnd": 2222, "chr": "2", "frequency": 2.0, "location": "l2", "array": "a2", "primer": "p21"}]')
        self.assertEqual(obj, exp)

class Populations(TestCase):

    def test_populations_url_with_no_data(self):
        """
        the url app/populations/ should return a 400 response when no input data is supplied
        """
        response = self.client.get(reverse('app:populations'))
        self.assertEqual(response.status_code, 400)

    def test_populations_url_with_oligo_with_data(self):
        """
        the url app/populations/ should return all of an oligo's populations
        """
        create_population('p1', 'pop1', '11')
        create_population('p2', 'pop1', '11')
        create_population('p2', 'pop2', '22')
        response = self.client.get(reverse('app:populations'), {'primer': 'p2'})
        self.assertEqual(response.status_code, 200)
        obj = json.loads(response.content)
        exp = json.loads('[{"count": 11, "primer": "p2", "name": "pop1"}, {"count": 22, "primer": "p2", "name": "pop2"}]')
        self.assertEqual(obj, exp)

    def test_populations_url_with_oligo_with_no_data(self):
        """
        the url app/populations/ should return an empty array when oligo has no populations
        """
        create_population('p1', 'pop1', '11')
        response = self.client.get(reverse('app:populations'), {'primer': 'p2'})
        self.assertEqual(response.status_code, 200)
        obj = json.loads(response.content)
        exp = json.loads('[]')
        self.assertEqual(obj, exp)

class Comments(TestCase):

    def test_comments_url_with_no_input(self):
        """
        the url app/comments/ should return a 400 response when no input data is supplied
        """
        response = self.client.get(reverse('app:comments'))
        self.assertEqual(response.status_code, 400)

    def test_comments_url_with_oligo_with_no_data(self):
        """
        the url app/comments/ should return an empty array when oligo has no comments
        """
        create_comment('p1', '3', 'a p1 comment')
        response = self.client.get(reverse('app:comments'), {'primer': 'p2'})
        self.assertEqual(response.status_code, 200)
        obj = json.loads(response.content)
        exp = json.loads('{"primer": "p2", "data": []}')
        self.assertEqual(obj, exp)

    def test_comments_url_with_oligo_with_data(self):
        """
        the url app/comments/ should return all of an oligo's comments
        """
        create_comment('p1', '3', 'a p1 comment')
        create_comment('p2', '2', 'a p2 comment')
        create_comment('p2', '5', 'another p2 comment')
        response = self.client.get(reverse('app:comments'), {'primer': 'p2'})
        self.assertEqual(response.status_code, 200)
        obj = json.loads(response.content)
        exp = json.loads('{"primer": "p2", "data": [{"rating": 5, "primer": "p2", "text": "another p2 comment"}, {"rating": 2, "primer": "p2", "text": "a p2 comment"}]}')
        self.assertEqual(obj, exp)

class AddComment(TestCase):

    def test_addComment_url_with_no_primer(self):
        """
        the url app/addComment/ should return a 400 response when no primer supplied
        """
        response = self.client.get(reverse('app:addComment'), {'rating': '3', 'text': 'a comment'})
        self.assertEqual(response.status_code, 400)

    def test_addComment_url_with_no_rating_no_text(self):
        """
        the url app/addComment/ should return a 400 response when both rating & text are not supplied
        """
        response = self.client.get(reverse('app:addComment'), {'primer': 'p2'})
        self.assertEqual(response.status_code, 400)

    def test_addComment_url_with_no_text(self):
        """
        the url app/addComment/ should succeed when rating is supplied, but text is not
        """
        response = self.client.get(reverse('app:addComment'), {'primer': 'p2', 'rating': '3'})
        self.assertEqual(response.status_code, 200)
        obj = map(keyComment, Comment.objects.filter(primer='p2'))
        exp = json.loads('[{"primer": "p2", "rating": 3, "text": ""}]')
        self.assertEqual(obj, exp)

    def test_addComment_url_with_no_rating(self):
        """
        the url app/addComment/ should succeed when text is supplied, but rating is not
        """
        response = self.client.get(reverse('app:addComment'), {'primer': 'p2', 'text': 'a comment'})
        self.assertEqual(response.status_code, 200)
        obj = map(keyComment, Comment.objects.filter(primer='p2'))
        exp = json.loads('[{"primer": "p2", "rating": 0, "text": "a comment"}]')
        self.assertEqual(obj, exp)

    def test_addComment_url_with_embedded_html(self):
        """
        the url app/addComment/ should escape any embedded html
        """
        response = self.client.get(reverse('app:addComment'), {'primer': 'p2', 'text': '<p>evil html</p>'})
        self.assertEqual(response.status_code, 200)
        obj = map(keyComment, Comment.objects.filter(primer='p2'))
        self.assertEqual(obj[0]['text'], "&lt;p&gt;evil html&lt;/p&gt;")

class Help(TestCase):

    def test_help_url_exists(self):
        """
        the url app/help/ should exist
        """
        response = self.client.get(reverse('app:help'))
        self.assertEqual(response.status_code, 200)
