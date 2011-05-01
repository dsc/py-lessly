#!/usr/bin/env python
# encoding: utf-8

import csv

class LesslyCSVDialect(csv.Dialect):
    delimiter = ','
    skipinitialspace = True
    lineterminator = '\n'
    quotechar = '"'
    doublequote = False
    escapechar = '\\'
    quoting = csv.QUOTE_MINIMAL

csv.register_dialect('lessly', LesslyCSVDialect)


def readDict(path, header=None):
    f = open(path, 'rU')
    if header: f.readline() # throw away header line
    return csv.DictReader(f, fieldnames=header, dialect='lessly')

def writeDict(path, header=None):
    f = open(path, 'w')
    return csv.DictWriter(f, fieldnames=header, dialect='lessly')

