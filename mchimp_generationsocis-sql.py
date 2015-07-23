#!/usr/bin/env python
#-*- coding: utf8 -*-

import psycopg2
import config
import dbutils
import codecs
import sys
from consolemsg import step, error, fail, warn

def esPersonaFisica(soci) :
    return 0 if soci.nif[2] in "ABCDEFGHJNPQRSUVW" else 1

def ambPuntDeMilers(numero) :
    return '{:,}'.format(numero).replace(',','.')


db = psycopg2.connect(**config.psycopg)
with db.cursor() as cursor :
    cursor.execute("""\
        SELECT * FROM (
        SELECT DISTINCT ON (sub.soci_id)
            sub.soci_id as soci_id,
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
                soci.active AND
                pol.active AND
                pol.state = 'activa' AND
                cups.active AND
                TRUE
            GROUP BY
                soci.id
            ORDER BY
                soci.id ASC
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
        ) as result
        ORDER BY
            result.name ASC
            
    ;
""")

    shareUse = 170
    recommendedPercent = 70
    shareCost = 100

    print u'\t'.join(unicode(x) for x in [
        'ID',
        'Name',
        'Call name',
        'Soci',
        'NIF',
        'E-mail',
        'Language',
        'Legal entity',
        'Contracts',
        'Anual use',
        'Recommended shares',
        'Covered use',
        'Recommended investment',
        ])


    for line in dbutils.fetchNs(cursor) :
        try:

            totalUse = line.consumannual
            if totalUse is None:
                warn("Soci {} amb consum null".format(
                    line.nsoci))
                continue

            if totalUse * recommendedPercent < shareUse * 100 :
                error("El soci {} no te prou consum ({})".format(line.nsoci, totalUse))
                continue

            if line.nif[:2] != 'ES':
                warn("Soci amb un VAT code no espanyol: {}".format(line.nif[:2]))

            recommendedShares = (totalUse*recommendedPercent/100) // shareUse
            recommendedInvestment = recommendedShares * shareCost

                    
            print '\t'.join(
                    str(x)
                        .replace('\t',' ')
                        .replace('\n',' ')
                        .replace('\r',' ')
                    for x in [
                line.soci_id,
                line.name,
                line.name.split(',')[-1].strip() if esPersonaFisica(line) else '',
                line.nsoci[1:].lstrip('0'),
                line.nif[2:],
                line.email,
                line.lang,
                0 if esPersonaFisica(line) else 1,
                line.ncontractes,
                ambPuntDeMilers(totalUse),
                ambPuntDeMilers(recommendedShares),
                ambPuntDeMilers(recommendedShares * shareUse),
                ambPuntDeMilers(recommendedInvestment),
                ])
        except Exception as e:
            import traceback
            error("Error processant soci {}\n{}\n{}".format(
                line.nsoci,
                e,
                "\n".join(traceback.format_stack()),
                )) 








