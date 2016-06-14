#!/usr/bin/env python
#-*- coding: utf8 -*-

from namespace import namespace as ns
import math
from consolemsg import step

from distribucio_de_polissas import distribucioPolissas

from mapa_socis import *

import sys


def generateMaps(year, month, endyear, endmonth):
    import datetime
    import dbutils

    beginingNextMonth = (
        datetime.date(year, month+1, 1)
        if month != 12 else 
        datetime.date(year+1, 1, 1)
        ) - datetime.timedelta(days=1)
    
    beginingNextEndMonth = (
        datetime.date(endyear, endmonth+1, 1)
        if endmonth != 12 else 
        datetime.date(endyear+1, 1, 1)
        ) - datetime.timedelta(days=1)
    
    populationPerCCAA = dict(
        (line.code, int(line.population_2014_01))
        for line in readCsvNs('poblacio_ccaa.csv')
        )
    populationPerProvincia = dict(
        (line.code, int(line.population_2015_01))
        for line in readCsvNs('poblacio_provincies-20150101.csv')
        )

#    distribucioPolissas = readCsvNs("distribucio.csv")
    distribucioPolissa = distribucioPolissas(str(beginingNextMonth),str(beginingNextEndMonth), dbutils.nsList)

    socisPerCCAA = countBy('codi_ccaa', distribucioPolissa, noneValue='00')
    socisPerProvincia = countBy('codi_provincia', distribucioPolissa, noneValue='00')
    socisPerMunicipi = countBy('codi_ine', distribucioPolissa, noneValue='00000')
    socisPerPais = countBy('codi_pais', distribucioPolissa, noneValue='00')

    relativePolissasPerCCAA = dict(
        (ccaa, socis*10000./populationPerCCAA[ccaa])
        for ccaa, socis in socisPerCCAA.items()
        )

    relativePolissasPerProvincia = dict(
        (prov, socis*10000./populationPerProvincia[prov])
        for prov, socis in socisPerProvincia.items()
	if prov in populationPerProvincia
        )


    totalPolissas = sum(value for value in socisPerCCAA.values())


    months = (
        "Enero Febrero Marzo Abril Mayo Junio "
        "Julio Agosto Septiembre Octubre Noviembre Diciembre"
        ).split()


    output = ns(
        month = months[month-1].upper(),
        year = year,
        endmonth = months[endmonth-1].upper(),
        endyear = endyear,
        )

    step("Generant mapa amb valors absoluts")

    output.titol = ""
    output.subtitol = ""

    maxPolissas = max(value for value in socisPerCCAA.values()) and 1800
    minPolissas = min(value for value in socisPerCCAA.values())
    for ccaa, population in populationPerCCAA.items():
        socis = socisPerCCAA.get(ccaa,0)
        output['number_'+ccaa] = socis
        output['percent_'+ccaa] = '{:.1f}%'.format(socis*100./totalPolissas).replace('.',',')
        output['color_'+ccaa] = mapColor(socis, minPolissas, maxPolissas)
    renderMap('PolissasPerCCAA-absoluts-{:04}-{:02}'.format(year,month), output,'MapaContratos-template.svg')

    step("Generant mapa amb valors relatius")

    output.titol = "Polissas/10.000 hab."
    output.subtitol = "             (datos INE 01/2014)"

    maxRelativePolissas = max(value for value in relativePolissasPerCCAA.values()) and 10.
    minRelativePolissas = min(value for value in relativePolissasPerCCAA.values())

    for ccaa, population in populationPerCCAA.items():
        relativeSoci = relativePolissasPerCCAA.get(ccaa,0)
        output['number_'+ccaa] = '{:.1f}'.format(relativeSoci).replace('.',',')
        output['color_'+ccaa] = mapColor(
            relativeSoci, minRelativePolissas, maxRelativePolissas)
        output['percent_'+ccaa] = ''
    renderMap('PolissasPerCCAA-relatius-{:04}-{:02}'.format(year,month), output,'MapaContratos-template.svg')


    output = ns(
        month = months[month-1].upper(),
        year = year,
        )
    step("Generant mapa per provincies amb valors absoluts")

    maxPolissas = max(value for value in socisPerProvincia.values()) and 1800
    minPolissas = min(value for value in socisPerProvincia.values())
    for prov, population in populationPerProvincia.items():
        socis = socisPerProvincia.get(prov,0)
        output['number_'+prov] = socis
        output['percent_'+prov] = '{:.1f}%'.format(socis*100./totalPolissas).replace('.',',')
        output['color_'+prov] = mapColor(socis, minPolissas, maxPolissas)
    renderMap('PolissasPerProvincies-absoluts-{:04}-{:02}'.format(year,month), output, 'MapaProvincias-template.svg')

    step("Generant mapa per provincies amb valors relatius")

    output.titol = "Polissas/10.000 hab."
    output.subtitol = "             (datos INE 01/2015)"

    maxRelativePolissas = max(value for value in relativePolissasPerProvincia.values()) and 10.
    minRelativePolissas = min(value for value in relativePolissasPerProvincia.values())

    for prov, population in populationPerProvincia.items():
        relativeSoci = relativePolissasPerProvincia.get(prov,0)
        output['number_'+prov] = '{:.1f}'.format(relativeSoci).replace('.',',')
        output['color_'+prov] = mapColor(
            relativeSoci, minRelativePolissas, maxRelativePolissas)
        output['percent_'+prov] = ''
    renderMap('PolissasPerProvincies-relatius-{:04}-{:02}'.format(year,month), output, 'MapaProvincias-template.svg')



if __name__ == '__main__':
    year = int(sys.argv[1])
    month = int(sys.argv[2])
    end_year = int(sys.argv[3])
    end_month = int(sys.argv[4])
    generateMaps(year, month, end_year, end_month)





