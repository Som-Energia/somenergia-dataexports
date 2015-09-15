#!/usr/bin/env python
#-*- coding: utf8 -*-

from namespace import namespace as ns
import math

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
        if keyValue is "None":
            keyValue = None
        previousCount = result.get(keyValue,0)
        result[keyValue] = previousCount + int(line.quants)
    return result


populationPerCCAA = dict(
    (line.code, int(line.population_2014_01))
    for line in readCsvNs('poblacio_ccaa.csv')
    )

distribucioSocis = readCsvNs("distribucio.csv")

socisPerCCAA = countBy('codi_ccaa', distribucioSocis, noneValue='00')
socisPerProvincia = countBy('codi_provincia', distribucioSocis, noneValue='00')
socisPerMunicipi = countBy('codi_ine', distribucioSocis, noneValue='00000')

totalSocis = sum(value for value in socisPerCCAA.values())
maxSocis = max(value for value in socisPerCCAA.values())
minSocis = 0 #min(value for value in socisPerCCAA.values())

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
    '#440',
    '#440',
    '#440',
    '#440',
    '#440',
    '#440',
    '#440',
    '#440',
    '#440',
    '#440',
    '#440',
    '#440',
    '#440',
    '#440',
    '#440',
    '#440',
    '#440',
    '#440',
    '#440',
    '#440',
    '#440',
    '#440',
    '#440',
    '#440',
    '#440',
    '#440',
    '#440',
]


def mapColor(value, minValue, maxValue):
    print value, minValue, maxValue
    return colors[int((len(colors)-1)*(value-minValue)/(maxValue-minValue))]


with open("MapaSocios-template.svg") as svgTemplateFile:
    svgTemplate = svgTemplateFile.read()

output = ns(
    month = 'Marzo',
    year=2015,
    )

for ccaa, population in populationPerCCAA.items():
    socis = socisPerCCAA.get(ccaa,0)
    output['number_'+ccaa] = socis
    output['relative_'+ccaa] = '{:.2f}'.format(socis*10000./population)
    output['percent_'+ccaa] = '{:.2f}'.format(socis*100./totalSocis)
    output['color_'+ccaa] = mapColor(socis, minSocis, maxSocis)

print output

with open('SocisPerCCAA-absoluts.svg','w') as svgAbsolut:
    svgAbsolut.write(svgTemplate.format(**output))

for ccaa, population in populationPerCCAA.items():
    output['number_'+ccaa] = output['relative_'+ccaa]

with open('SocisPerCCAA-relatius.svg','w') as svgRelatiu:
    svgRelatiu.write(svgTemplate.format(**output))
    






