#!/usr/bin/env python
#-*- coding: utf8 -*-

import ooop
from dbconfig import dbconfig
import codecs
import sys
import argparse

O = ooop.OOOP(**dbconfig(profile='local'))

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
        'Contracts',
        'Anual use',
        'Recommended investment',
        ])

    for i,soci_id in enumerate(soci_ids):
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
        if not i%10 : print ".", ; sys.stdout.flush()
        if not len(consums) :
            print >> sys.stderr, soci_id, "Sin contratos"

        shareUse = 170
        recommendedProportion = .70
        shareCost = 100

        totalUse = sum((contract['annual_use_kwh'] for contract in consums))
        recommendedInvestment = ((totalUse*recommendedProportion)//shareUse)*shareCost

        if totalUse < 5 :
            print >> sys.stderr, soci_id, "Sin consumo"

        print >> output, u'\t'.join(unicode(x).replace('\t',' ') for x in [
            soci_id,
            soci.name,
            soci.name.split(',')[-1].strip(),
            soci.address[0].email,
            soci.lang,
            len(consums),
            totalUse,
            recommendedInvestment,
            ])



