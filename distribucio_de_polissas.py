#!/usr/bin/env python
#-*- coding: utf8 -*-

import psycopg2
import config
import sys


def distribucioPolissas(date, date_end, dbhandler, debug=False):


    db = psycopg2.connect(**config.psycopg)
    with db.cursor() as cursor :
        cursor.execute(open("distribucio_de_polissas.sql","r").read().rstrip(), dict(
        date=date,
        date_end=date_end
        ))

        return dbhandler(cursor)


if __name__ == '__main__':
    import dbutils
    import datetime
    debug = False
    if '--debug' in sys.argv:
        sys.argv.remove('--debug')
        debug = True
    date = sys.argv[1] if len(sys.argv)>1 else str(datetime.date.today())
    date_end = sys.argv[2] if len(sys.argv)>2 else str(datetime.date.today())
    print distribucioPolissas(date=date, date_end=date_end, dbhandler=dbutils.csvTable, debug=debug)
