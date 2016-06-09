#!/usr/bin/env python
#-*- coding: utf8 -*-

import psycopg2
import config
import sys


def distribucioPolissas(date, dbhandler, debug=False):


    db = psycopg2.connect(**config.psycopg)
    with db.cursor() as cursor :
        cursor.execute("""\
select  municipi.name as municipi, 
	municipi.ine as codi_ine, 
	provincia.name as provincia, 
	provincia.code as codi_provincia, 
	comunitat.name as comunitat_autonoma, 
	comunitat.codi as codi_ccaa, 
	pais.name as pais, 
	pais.code as codi_pais, 
	count(polissa.id) as quants 
	from giscedata_polissa polissa
	left join res_partner rp on rp.id = polissa.soci
	inner join giscedata_cups_ps cups on polissa.cups = cups.id
	left join res_municipi  municipi on cups.id_municipi=municipi.id
	left join res_country_state provincia on provincia.id = municipi.state
	LEFT JOIN res_comunitat_autonoma AS comunitat ON comunitat.id = provincia.comunitat_autonoma
	left join res_country as pais on pais.id = provincia.country_id
where polissa.data_alta < %(date)s and 
	(polissa.data_baixa > %(date)s
		or polissa.data_baixa is null) and 
	TRUE
GROUP BY
	codi_pais,
	codi_ccaa,
	codi_provincia,
	codi_ine,
	pais,
	provincia,
	municipi,
	comunitat.name
ORDER BY
	pais ASC,
	comunitat_autonoma ASC,
	provincia ASC,
	municipi ASC,
	TRUE ASC
""", dict(
        date=date,
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
    print date
    print distribucioPolissas(date=date, dbhandler=dbutils.csvTable, debug=debug)
