#!python

# Usage: python tsv2json.py <table>
#    where: a file named <table>.tsv must exist as the input file
#           a file named <table>.json will be created

import sys
import string
import json
import os

INDENT=4

table = sys.argv[1]
genPk = False

if table == 'population':
    genPk = True
if table == 'comment':
    genPk = True

tsv = open(table + '.tsv', 'r')
jsn = open(table + '.json', 'a+')
jsn.truncate(0)

titles = [string.strip(t) for t in string.split(tsv.readline(), sep='\t')]
i = 1
model = 'app.' + table

jsn.write('[\n')

for line in tsv:
    row = {}
    row['model'] = 'app.' + table
    if genPk:
        row['pk'] = i
        i += 1
    row['fields'] = {}
    for attr, val in zip(titles, string.split(line, sep='\t')):
        row['fields'][attr] = string.strip(val)
    jsn.write(json.dumps(row, indent=INDENT))
    jsn.write(',\n')

position = jsn.tell()
jsn.truncate(position - 2)
jsn.write('\n]\n')
tsv.close()
jsn.close()
