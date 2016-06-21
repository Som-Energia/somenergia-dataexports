#!/usr/bin/env python
#-*- coding: utf8 -*-

from namespace import namespace as ns
import math
from consolemsg import step

from distribucio_de_socies import distribucioSocies
from distribucio_de_polissas import distribucioPolissas

import sys


def readCsvTable(filename):
    """Reads a tab separated csv file as an array of
    arrays"""
    with open(filename) as csv:
        return [
            [ field.strip() for field in line.split('\t') ]
            for line in csv
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

def generateMaps(year, month, itemFunction, itemName):
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
    distribucioItems = itemFunction(str(beginingNextMonth), dbutils.nsList)

    itemsPerCCAA = countBy('codi_ccaa', distribucioItems, noneValue='00')
    itemsPerProvincia = countBy('codi_provincia', distribucioItems, noneValue='00')
    itemsPerMunicipi = countBy('codi_ine', distribucioItems, noneValue='00000')
    itemsPerPais = countBy('codi_pais', distribucioItems, noneValue='00')

    relativeItemsPerCCAA = dict(
        (ccaa, items*10000./populationPerCCAA[ccaa])
        for ccaa, items in itemsPerCCAA.items()
        )

    relativeItemsPerProvincia = dict(
        (prov, items*10000./populationPerProvincia[prov])
        for prov, items in itemsPerProvincia.items()
	if prov in populationPerProvincia
        )


    totalItems = sum(value for value in itemsPerCCAA.values())


    months = (
        "Enero Febrero Marzo Abril Mayo Junio "
        "Julio Agosto Septiembre Octubre Noviembre Diciembre"
        ).split()


    output = ns(
        month = months[month-1].upper(),
        year = year,
        )

    step("Generant mapa amb valors absoluts")

    output.titol = "{}".format(itemName.capitalize())
    output.subtitol = ""

    maxItems = max(value for value in itemsPerCCAA.values()) and 1800
    minItems = min(value for value in itemsPerCCAA.values())
    for ccaa, population in populationPerCCAA.items():
        items = itemsPerCCAA.get(ccaa,0)
        output['number_'+ccaa] = items
        output['percent_'+ccaa] = '{:.1f}%'.format(items*100./totalItems).replace('.',',')
        output['color_'+ccaa] = mapColor(items, minItems, maxItems)
    renderMap('Mapa-distribución-{}-{:04}-{:02}'.format(itemName,year,month), output)

    step("Generant mapa amb valors relatius")

    output.titol = "{}/10.000 hab.".format(itemName.capitalize())
    output.subtitol = "             (datos INE 01/2014)"

    maxRelativeItems = max(value for value in relativeItemsPerCCAA.values()) and 10.
    minRelativeItems = min(value for value in relativeItemsPerCCAA.values())

    for ccaa, population in populationPerCCAA.items():
        relativeItem = relativeItemsPerCCAA.get(ccaa,0)
        output['number_'+ccaa] = '{:.1f}'.format(relativeItem).replace('.',',')
        output['color_'+ccaa] = mapColor(
            relativeItem, minRelativeItems, maxRelativeItems)
        output['percent_'+ccaa] = ''
    renderMap('Mapa-distribución-{}-pob-{:04}-{:02}'.format(itemName,year,month), output)


    output = ns(
        month = months[month-1].upper(),
        year = year,
        )
    
    output.titol = "{}".format(itemName.capitalize())
    output.subtitol = ""
    
    step("Generant mapa per provincies amb valors absoluts")

    maxItems = max(value for value in itemsPerProvincia.values()) and 1800
    minItems = min(value for value in itemsPerProvincia.values())
    for prov, population in populationPerProvincia.items():
        items = itemsPerProvincia.get(prov,0)
        output['number_'+prov] = items
        output['percent_'+prov] = '{:.1f}%'.format(items*100./totalItems).replace('.',',')
        output['color_'+prov] = mapColor(items, minItems, maxItems)
    renderMap('Mapa-distribución-{}-provincias-{:04}-{:02}'.format(itemName,year,month), output, 'MapaProvincias-template.svg')

    step("Generant mapa per provincies amb valors relatius")

    output.titol = "{}/10.000 hab.".format(itemName.capitalize())
    output.subtitol = "             (datos INE 01/2015)"

    maxRelativeItems = max(value for value in relativeItemsPerProvincia.values()) and 10.
    minRelativeItems = min(value for value in relativeItemsPerProvincia.values())

    for prov, population in populationPerProvincia.items():
        relativeItem = relativeItemsPerProvincia.get(prov,0)
        output['number_'+prov] = '{:.1f}'.format(relativeItem).replace('.',',')
        output['color_'+prov] = mapColor(
            relativeItem, minRelativeItems, maxRelativeItems)
        output['percent_'+prov] = ''
    renderMap('Mapa-distribución-{}-provincias-pob-{:04}-{:02}'.format(itemName,year,month), output, 'MapaProvincias-template.svg')



if __name__ == '__main__':
    year = int(sys.argv[1])
    month = int(sys.argv[2])
    generateMaps(year, month, distribucioSocies, "socixs")
    generateMaps(year, month, distribucioPolissas, "contratos")
