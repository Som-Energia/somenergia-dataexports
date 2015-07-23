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

subquerySocis = """\
SELECT pc.name AS categoria,
       m.name AS municipi,
       p.ref AS num_soci,
       p.vat AS nif,
       pa.email AS email,
       pa.name AS nom,
       prov.name AS provincia,
       pa.zip AS codi_postal,
       p.lang AS idioma,
       com.name AS comarca,
       ccaa.name AS comunitat_autonoma,
       pa.id AS soci_id,
       m.id AS id_municipi
FROM res_partner_address AS pa
LEFT JOIN res_partner AS p ON (p.id=pa.partner_id)
LEFT JOIN res_partner_category_rel AS p__c ON (pa.partner_id=p__c.partner_id)
LEFT JOIN res_partner_category AS pc ON (pc.id=p__c.category_id and pc.name='Soci')
LEFT JOIN res_municipi AS m ON (m.id=pa.id_municipi)
LEFT JOIN res_country_state AS prov ON (prov.id=pa.state_id)
LEFT JOIN res_comunitat_autonoma AS ccaa ON (ccaa.id=prov.comunitat_autonoma)
LEFT JOIN res_comarca AS com ON (com.id=m.comarca)
WHERE pa.active AND p__c.category_id IS NOT NULL AND
  p__c.category_id = (SELECT id FROM res_partner_category WHERE name='Soci')
ORDER BY p.ref
"""



db = psycopg2.connect(**config.psycopg)
with db.cursor() as cursor :
    cursor.execute("""\
SELECT
    municipi,
    provincia,
    comunitat_autonoma,
    COUNT(soci_id) AS quants
FROM ("""+subquerySocis+""") AS detall
GROUP BY
    provincia,
    municipi,
    comunitat_autonoma
ORDER BY
    comunitat_autonoma ASC,
    provincia ASC,
    municipi ASC,
    true ASC
""")

    print dbutils.csvTable(cursor)







