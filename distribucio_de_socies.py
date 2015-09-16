#!/usr/bin/env python
#-*- coding: utf8 -*-

import psycopg2
import config
import dbutils
import sys
from consolemsg import step, error, fail, warn

subquerySocis = """\
SELECT
    pc.name AS categoria,
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
    country.name AS pais,
    pa.id AS soci_id,
    m.id AS id_municipi,
    m.ine AS codi_ine,
    prov.code AS codi_provincia,
    ccaa.codi AS codi_ccaa,
    country.code AS codi_pais
FROM res_partner_address AS pa
JOIN (
    SELECT
        dades_inicials.partner_id,
        MIN(dades_inicials.id) AS id_unic
    FROM
        res_partner_address as dades_inicials
    WHERE
        dades_inicials.active
    GROUP BY dades_inicials.partner_id
    ) AS dades_inicials ON dades_inicials.id_unic = pa.id
LEFT JOIN res_partner AS p ON (p.id=pa.partner_id)
LEFT JOIN res_partner_category_rel AS p__c ON (pa.partner_id=p__c.partner_id)
LEFT JOIN res_partner_category AS pc ON (pc.id=p__c.category_id and pc.name='Soci')
LEFT JOIN res_municipi AS m ON (m.id=pa.id_municipi)
LEFT JOIN res_country_state AS prov ON (prov.id=pa.state_id)
LEFT JOIN res_comunitat_autonoma AS ccaa ON (ccaa.id=prov.comunitat_autonoma)
LEFT JOIN res_comarca AS com ON (com.id=m.comarca)
LEFT JOIN res_country AS country ON (country.id=pa.country_id)
WHERE
    pa.active AND
    pa.create_date < %(data)s AND
    p__c.category_id IS NOT NULL AND
    p__c.category_id = (SELECT id FROM res_partner_category WHERE name='Soci')
ORDER BY p.ref
"""



db = psycopg2.connect(**config.psycopg)
with db.cursor() as cursor :
    cursor.execute("""\
SELECT
    codi_pais,
    pais,
    codi_ccaa,
    comunitat_autonoma,
    codi_provincia,
    provincia,
    codi_ine,
    municipi,
    COUNT(soci_id) AS quants
FROM ("""+subquerySocis+""") AS detall
GROUP BY
    codi_pais,
    codi_ccaa,
    codi_provincia,
    codi_ine,
    pais,
    provincia,
    municipi,
    comunitat_autonoma,
    TRUE
ORDER BY
    pais ASC,
    comunitat_autonoma ASC,
    provincia ASC,
    municipi ASC,
    TRUE ASC
""", dict(
        data=sys.argv[1],
        ))

    print dbutils.csvTable(cursor)







