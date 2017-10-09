#!/usr/bin/env python
#-*- coding: utf8 -*-

from yamlns import namespace as ns
import math
from consolemsg import step

from distribucio_de_socies import distribucioSocies

import sys

def readCsvTable(filename):
    """Reads a tab separated csv file as an array of
    arrays"""
    with open(filename) as csvSocis:
        return [
            [ field.strip() for field in line.split('\t') ]
            for line in csvSocis
            if line.strip()
            ]

def readCsvNs(filename):
    """reads a tab separated csv file as an array of namespaces
    using column headers (first line) as keys"""
    table = readCsvTable(filename)

    keys = table[0]
    return [
        ns((key, value) for key, value in zip(keys, line))
        for line in table[1:]
        ]

def countBy(column, data, noneValue=None) :
    """Groups the quantities sharing a value in one column"""
    result={}
    for line in data:
        keyValue = line[column]
        if keyValue == None:
            keyValue = noneValue
        previousCount = result.get(keyValue,0)
        result[keyValue] = previousCount + int(line.quants)
    return result

def renderMap(filename, data, template="MapaSocios-template.svg"):
    with open(template) as svgTemplateFile:
        svgTemplate = svgTemplateFile.read()

    svgcontent = svgTemplate.format(**data)

    with open(filename+'.svg','w') as svgAbsolut:
        svgAbsolut.write(svgcontent)

    import subprocess
#    subprocess.call(["inkscape", filename+'.svg', '-e', filename+'.png', '--export-dpi', '200'])
    subprocess.call(["convert", '-density', '200', filename+'.svg', filename+'.png'])


def mapColor(value, minValue, maxValue):
    with open('scale-classic.csv') as scalecsv:
        colors = [ color.strip() for color in scalecsv ]

    ncolors = len(colors)-1
    return colors[min(ncolors, int(ncolors*(value-minValue)/(maxValue-minValue)))]

def generateMaps(year, month):
    import datetime
    import dbutils

    beginingNextMonth = (
        datetime.date(year, month+1, 1)
        if month != 12 else 
        datetime.date(year+1, 1, 1)
        ) - datetime.timedelta(days=1)

    populationPerCCAA = dict(
        (line.code, int(line.population_2014_01))
        for line in readCsvNs('poblacio_ccaa.csv')
        )
    populationPerProvincia = dict(
        (line.code, int(line.population_2015_01))
        for line in readCsvNs('poblacio_provincies-20150101.csv')
        )

#    distribucioSocis = readCsvNs("distribucio.csv")
    distribucioSocis = distribucioSocies(str(beginingNextMonth), dbutils.nsList)

    socisPerCCAA = countBy('codi_ccaa', distribucioSocis, noneValue='00')
    socisPerProvincia = countBy('codi_provincia', distribucioSocis, noneValue='00')
    socisPerMunicipi = countBy('codi_ine', distribucioSocis, noneValue='00000')
    socisPerPais = countBy('codi_pais', distribucioSocis, noneValue='00')

    relativeSocisPerCCAA = dict(
        (ccaa, socis*10000./populationPerCCAA[ccaa])
        for ccaa, socis in socisPerCCAA.items()
        )

    relativeSocisPerProvincia = dict(
        (prov, socis*10000./populationPerProvincia[prov])
        for prov, socis in socisPerProvincia.items()
        if prov in populationPerProvincia
        )


    totalSocis = sum(value for value in socisPerCCAA.values())


    months = (
        "Enero Febrero Marzo Abril Mayo Junio "
        "Julio Agosto Septiembre Octubre Noviembre Diciembre"
        ).split()


    output = ns(
        month = months[month-1].upper(),
        year = year,
        )

    step("Generant mapa amb valors absoluts")

    output.titol = ""
    output.subtitol = ""

    maxSocis = max(value for value in socisPerCCAA.values()) and 1800
    minSocis = min(value for value in socisPerCCAA.values())
    for ccaa, population in populationPerCCAA.items():
        socis = socisPerCCAA.get(ccaa,0)
        output['number_'+ccaa] = socis
        output['percent_'+ccaa] = '{:.1f}%'.format(socis*100./totalSocis).replace('.',',')
        output['color_'+ccaa] = mapColor(socis, minSocis, maxSocis)
    renderMap('SocisPerCCAA-absoluts-{:04}-{:02}'.format(year,month), output)

    step("Generant mapa amb valors relatius")

    output.titol = "Socixs/10.000 hab."
    output.subtitol = "             (datos INE 01/2014)"

    maxRelativeSocis = max(value for value in relativeSocisPerCCAA.values()) and 10.
    minRelativeSocis = min(value for value in relativeSocisPerCCAA.values())

    for ccaa, population in populationPerCCAA.items():
        relativeSoci = relativeSocisPerCCAA.get(ccaa,0)
        output['number_'+ccaa] = '{:.1f}'.format(relativeSoci).replace('.',',')
        output['color_'+ccaa] = mapColor(
            relativeSoci, minRelativeSocis, maxRelativeSocis)
        output['percent_'+ccaa] = ''
    renderMap('SocisPerCCAA-relatius-{:04}-{:02}'.format(year,month), output)


    output = ns(
        month = months[month-1].upper(),
        year = year,
        )
    step("Generant mapa per provincies amb valors absoluts")

    maxSocis = max(value for value in socisPerProvincia.values()) and 1800
    minSocis = min(value for value in socisPerProvincia.values())
    for prov, population in populationPerProvincia.items():
        socis = socisPerProvincia.get(prov,0)
        output['number_'+prov] = socis
        output['percent_'+prov] = '{:.1f}%'.format(socis*100./totalSocis).replace('.',',')
        output['color_'+prov] = mapColor(socis, minSocis, maxSocis)
    renderMap('SocisPerProvincies-absoluts-{:04}-{:02}'.format(year,month), output, 'MapaProvincias-template.svg')

    step("Generant mapa per provincies amb valors relatius")

    output.titol = "Socixs/10.000 hab."
    output.subtitol = "             (datos INE 01/2015)"

    maxRelativeSocis = max(value for value in relativeSocisPerProvincia.values()) and 10.
    minRelativeSocis = min(value for value in relativeSocisPerProvincia.values())

    for prov, population in populationPerProvincia.items():
        relativeSoci = relativeSocisPerProvincia.get(prov,0)
        output['number_'+prov] = '{:.1f}'.format(relativeSoci).replace('.',',')
        output['color_'+prov] = mapColor(
            relativeSoci, minRelativeSocis, maxRelativeSocis)
        output['percent_'+prov] = ''
    renderMap('SocisPerProvincies-relatius-{:04}-{:02}'.format(year,month), output, 'MapaProvincias-template.svg')



if __name__ == '__main__':
    year = int(sys.argv[1])
    month = int(sys.argv[2])
    generateMaps(year, month)




