#!/usr/bin/env python
#-*- coding: utf8 -*-

import psycopg2
import config
import dbutils
import sys
from consolemsg import step, error, fail, warn
from namespace import namespace as ns


step("Loading {}...".format(sys.argv[1]))
with open(sys.argv[1]) as sqlfile:
    query = sqlfile.read()

variables = ns()
if len(sys.argv)>=3:
    step("Loading variables...".format(sys.argv[2]))
    variables = ns.load(sys.argv[2])
    warn(variables.dump())

step("Connecting to the database...")
db = psycopg2.connect(**config.psycopg)

with db.cursor() as cursor :
    cursor.execute(query, variables)
    print dbutils.csvTable(cursor)







