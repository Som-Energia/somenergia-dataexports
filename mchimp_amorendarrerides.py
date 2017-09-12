#!/usr/bin/env python
#-*- coding: utf8 -*-

import psycopg2
import config
import dbutils
import codecs
import sys
from consolemsg import step, error, fail, warn
from namespace import namespace as ns

def esPersonaFisica(soci) :
    return 0 if soci.nif[2] in "ABCDEFGHJNPQRSUVW" else 1

def ambPuntDeMilers(numero) :
    return '{:,}'.format(numero).replace(',','.')


db = psycopg2.connect(**config.psycopg)
with db.cursor() as cursor :
    cursor.execute("""\
        SELECT DISTINCT gi.id, rpa.email, rp.lang
        FROM res_partner AS rp, res_partner_address AS rpa, somenergia_soci AS ss, generationkwh_investment as gi
        WHERE rp.id = rpa.partner_id AND
            rp.id = ss.partner_id AND
            ss.id = gi.member_id AND
            gi.purchase_date <= '2015-09-15' AND
            gi.active = True
        ;
    """)


    print u'\t'.join(unicode(x) for x in [
        'id',
        'email',
        'lang',
        ])


    for line in dbutils.fetchNs(cursor) :
        try:


            print '\t'.join(
                    str(x)
                        .replace('\t',' ')
                        .replace('\n',' ')
                        .replace('\r',' ')
                    for x in [
                line.id,
                line.email,
                line.lang,
            ])
        except Exception as e:
            import traceback
            error("Error processant soci {}\n{}\n{}".format(
                line.nsoci,
                e,
                "\n".join(traceback.format_stack()),
                )) 
            error(ns(cas=line).dump())








