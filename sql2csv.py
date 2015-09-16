#!/usr/bin/env python
#-*- coding: utf8 -*-

import psycopg2
import config
import dbutils
import sys
from consolemsg import step, error, fail, warn

with open(sys.argv[1]) as sqlfile:
    query = sqlfile.read()

db = psycopg2.connect(**config.psycopg)
with db.cursor() as cursor :
    cursor.execute(query)
    print dbutils.csvTable(cursor)







