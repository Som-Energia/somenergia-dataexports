#!/usr/bin/env python
#-*- coding: utf8 -*-

from namespace import namespace as ns
import math
from consolemsg import step

month = 7
year = 2014


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
        if keyValue == 'None':
            keyValue = noneValue
        previousCount = result.get(keyValue,0)
        result[keyValue] = previousCount + int(line.quants)
    return result

def renderMap(filename, data):
    with open("MapaSocios-template.svg") as svgTemplateFile:
        svgTemplate = svgTemplateFile.read()

    with open(filename,'w') as svgAbsolut:
        svgAbsolut.write(svgTemplate.format(**output))


populationPerCCAA = dict(
    (line.code, int(line.population_2014_01))
    for line in readCsvNs('poblacio_ccaa.csv')
    )

distribucioSocis = readCsvNs("distribucio.csv")

socisPerCCAA = countBy('codi_ccaa', distribucioSocis, noneValue='00')
socisPerProvincia = countBy('codi_provincia', distribucioSocis, noneValue='00')
socisPerMunicipi = countBy('codi_ine', distribucioSocis, noneValue='00000')

relativeSocisPerCCAA = dict(
    (ccaa, socis*10000./populationPerCCAA[ccaa])
    for ccaa, socis in socisPerCCAA.items()
    )

def mapColor(value, minValue, maxValue):
    colors = [
        '#EE0',
        '#DD0',
        '#CC0',
        '#BB0',
        '#AA0',
        '#990',
        '#880',
        '#770',
        '#660',
        ] + [
        '#440',
        ]*15
    return colors[int((len(colors)-1)*(value-minValue)/(maxValue-minValue))]


totalSocis = sum(value for value in socisPerCCAA.values())


months = (
    "Enero Febrero Marzo Abril Mayo Junio "
    "Julio Septiembre Octubre Noviembre Diciembre"
    ).split()


output = ns(
    month = months[month-1],
    year = year,
    )

step("Generant mapa amb valors absoluts")

maxSocis = max(value for value in socisPerCCAA.values())
minSocis = min(value for value in socisPerCCAA.values())
for ccaa, population in populationPerCCAA.items():
    socis = socisPerCCAA.get(ccaa,0)
    output['number_'+ccaa] = socis
    output['percent_'+ccaa] = '{:.2f}%'.format(socis*100./totalSocis)
    output['color_'+ccaa] = mapColor(socis, minSocis, maxSocis)
renderMap('SocisPerCCAA-absoluts.svg', output)

step("Generant mapa amb valors relatius")

maxRelativeSocis = max(value for value in relativeSocisPerCCAA.values())
minRelativeSocis = min(value for value in relativeSocisPerCCAA.values())

for ccaa, population in populationPerCCAA.items():
    relativeSoci = relativeSocisPerCCAA.get(ccaa,0)
    output['number_'+ccaa] = '{:.2f}'.format(relativeSoci)
    output['color_'+ccaa] = mapColor(
        relativeSoci, minRelativeSocis, maxRelativeSocis)
    output['percent_'+ccaa] = ''
renderMap('SocisPerCCAA-relatius.svg', output)

 






