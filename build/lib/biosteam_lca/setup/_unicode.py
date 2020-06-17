# -*- coding: utf-8 -*-
"""
Created on Sat May 19 14:23:21 2019

@author: cyshi
"""

import csv
import sys

PY3 = sys.version_info > (3,)
if PY3:
    dt = ";"
else:
    dt = b";"


class UnicodeReader: 
    """Below was adapted from: http://python3porting.com/problems.html#csv-api-changes, "Common migration problems"

       **References**
                [1]Regebro, Lennart. Porting to Python 3: An in-depth guide. CreateSpace, 2011.
    """
    def __init__(self, filename, dialect=csv.excel,
                 encoding="utf-8", **kw):
        self.filename = filename
        self.dialect = dialect
        self.encoding = encoding
        self.kw = kw

    def __enter__(self):
        if PY3:
            self.f = open(self.filename, 'rt',
                          encoding=self.encoding, newline='')
        else:
            self.f = open(self.filename, 'rb')
        self.reader = csv.reader(self.f, dialect=self.dialect,
                                 **self.kw)
        return self

    def __exit__(self, type, value, traceback):
        self.f.close()

    def next(self):
        row = next(self.reader)
        if PY3:
            return row
        return [s.decode(self.encoding) for s in row]

    __next__ = next

    def __iter__(self):
        return self

