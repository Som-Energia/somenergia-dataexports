#!/usr/bin/env python
#-*- coding: utf8 -*-

import ooop
from dbconfig import dbconfig
import codecs
import sys
import argparse
from consolemsg import step, error, fail, warn

O = ooop.OOOP(**dbconfig(profile='prod'))

soci_ids = O.ResPartner.search(
    [('category_id','=','Soci')
    ])




with codecs.open(sys.argv[1],'w', 'utf8') as output:
    print >> output, u'\t'.join(unicode(x) for x in [
        'ID',
        'Name',
        'Call name',
        'E-mail',
        'Language',
        'Legal entity',
        'Contracts',
        'Anual use',
        'Recommended shares',
        'Covered use',
        'Recommended investment',
        ])

    for i,soci_id in enumerate(soci_ids):
        step("Soci {}...".format(soci_id))

        try:
            soci = O.ResPartner.get(soci_id)
            contractes = O.GiscedataPolissa.search(
                [
                    '|',
                    ('titular.id', '=', soci_id),
                    ('pagador.id', '=', soci_id),
                ]
            )

            consums = [
                dict(
                    contract_id = contracte['name'],
                    supply_address = contracte['cups_direccio'],
                    annual_use_kwh = cups['conany_kwh'],
                    )
                if cups else dict()
                for contracte, cups in (
                    (contracte, O.GiscedataCupsPs.read(contracte['cups'][0], ['conany_kwh']))
                    if contracte['cups'] else (contracte, None)
                    for contracte in O.GiscedataPolissa.read(
                        contractes, ['name','cups','cups_direccio'])
                    )
                ]
            if not len(consums) :
                error("El soci {} no te contractes".format(soci_id))
                continue

            if any('annual_use_kwh' not in contract for contract in consums) :
                warn("El soci {} te un contracte sense consum anual calculat".format(soci_id))
                continue

            shareUse = 170
            recommendedPercent = 70
            shareCost = 100

            def ambPuntDeMilers(numero) :
                return '{:,}'.format(numero).replace(',','.')

            totalUse = sum((contract.get('annual_use_kwh',0) for contract in consums))
            recommendedShares = (totalUse*recommendedPercent/100) // shareUse
            recommendedInvestment = recommendedShares * shareCost

            if totalUse < shareUse :
                error("El soci {} no te prou consum ({})".format(soci_id, totalUse))
                continue

            print >> output, u'\t'.join(unicode(x).replace('\t',' ') for x in [
                soci_id,
                soci.name,
                soci.name.split(',')[-1].strip(),
                soci.address[0].email,
                soci.lang,
                1 if soci.vat[2] in "ABCDEFGHJNPQRSUVW" else 0,
                len(consums),
                ambPuntDeMilers(totalUse),
                ambPuntDeMilers(recommendedShares),
                ambPuntDeMilers(recommendedShares * shareUse),
                ambPuntDeMilers(recommendedInvestment),
                ])
        except Exception as e:
            import traceback
            error("{}\n{}".format(
                e,
                "\n".join(traceback.format_stack()),
                )) 



