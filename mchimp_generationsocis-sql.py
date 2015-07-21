#!/usr/bin/env python
#-*- coding: utf8 -*-

import psycopg2
import config
import dbutils
import codecs
import sys

def esPersonaFisica(soci) :
    return 0 if soci.nif[2] in "ABCDEFGHJNPQRSUVW" else 1

def ambPuntDeMilers(numero) :
    return '{:,}'.format(numero).replace(',','.')


db = psycopg2.connect(**config.psycopg)
with db.cursor() as cursor :
    cursor.execute("""\
        SELECT DISTINCT ON (sub.soci_id)
            sub.name AS name,
            sub.nsoci AS nsoci,
            sub.nif AS nif,
            sub.lang AS lang,
            sub.consumannual AS consumannual,
            sub.ncontractes AS ncontractes,
            address.email,
            FALSE
        FROM (
            SELECT
                soci.id AS soci_id,
                soci.name AS name,
                soci.ref AS nsoci,
                soci.vat AS nif,
                soci.lang AS lang,
                SUM(cups.conany_kwh) AS consumannual,
                COUNT(cups.conany_kwh) AS ncontractes,
                FALSE
            FROM res_partner AS soci
            LEFT JOIN
                giscedata_polissa AS pol ON (
                    pol.titular = soci.id OR
                    pol.pagador = soci.id
                    )
            LEFT JOIN 
                giscedata_cups_ps AS cups ON cups.id = pol.cups
            LEFT JOIN
                res_partner_category_rel AS cat ON cat.partner_id = soci.id
            WHERE
                cat.category_id = 8 AND
/*                soci.id < 1000 AND */
                soci.active AND
                pol.active AND
                pol.state = 'activa' AND
                cups.active AND
                TRUE
            GROUP BY
                soci.id
            ORDER BY
                soci.id
        ) AS sub
        LEFT JOIN
            res_partner_address AS address ON (address.partner_id = sub.soci_id)
        WHERE
            address.active AND
            address.email IS NOT NULL AND
            address.email != '' AND
            TRUE
        GROUP BY
            sub.soci_id,
            sub.name,
            sub.nsoci,
            sub.nif,
            sub.lang,
            sub.consumannual,
            sub.ncontractes,
            address.email,
            TRUE
            
    ;
""")

    for line in dbutils.fetchNs(cursor) :
        print '\t'.join(
                str(x)
                    .replace('\t',' ')
                    .replace('\n',' ')
                    .replace('\r',' ')
                for x in [
            line.name,
            line.name.split(',')[-1].strip() if esPersonaFisica(line) else '',
            line.nsoci,
            line.nif,
            line.lang,
            line.consumannual,
            line.ncontractes,
            line.email,

#            soci.name,
#            soci.name.split(',')[-1].strip(),
#            soci.ref[1:].lstrip('0'),
#            soci.vat[2:],
#            soci.address[0].email,
#            soci.lang,
#            1 if soci.vat[2] in "ABCDEFGHJNPQRSUVW" else 0,
#            len(consums),
#            ambPuntDeMilers(totalUse),
#            ambPuntDeMilers(recommendedShares),
#            ambPuntDeMilers(recommendedShares * shareUse),
#            ambPuntDeMilers(recommendedInvestment),
            ])

#    csv = dbutils.csvTable(cursor)
#    print csv






