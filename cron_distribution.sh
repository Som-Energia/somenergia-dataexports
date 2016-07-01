#!/bin/bash

die() {
    exit -1
}
step() {
    echo -e '\033[34;1m:: '$*'\033[0m'
}

scriptpath=$(dirname $(readlink -f "$0"))
cd "$scriptpath"
 
TOOPTIONS=$(
while read r
do
    [ -n "$r" ] &&  echo "--to $r"
done < recipients-distribucio
)
date


today=$(date -I)
IFS='-' read -r year month day <<< "$today" # split date
lastMonthEnd=$(date -I -d "$year-$month-01 - 1 day") # last day of last month


IFS='-' read -r year month day <<< "${1:-$lastMonthEnd}" # split date

step "Generating reports at $year-$month-$day"
step "  Generant mapes"
./mapa.py $year $month || die
step "  Generant dades detallades"
./distribucio_de_socies.py "$year-$month-$day" > distribucion-socias-$year-$month-$day-detalle.csv || die
./distribucio_de_polissas.py "$year-$month-$day" > distribucion-contratos-$year-$month-$day-detalle.csv || die
step "  Generant dades aggregades"
sql2csv.py distribucio_de_socies.sql --data "$year-$month-$day" > distribucion-socias-$year-$month-$day-agregado.csv || die
sql2csv.py distribucio_de_polissas_aggregated.sql --date "$year-$month-$day" > distribucion-contratos-$year-$month-$day-agregado.csv || die

step "Sending results..."

TEXTOK="
# Distribución de socixs y contratos ($year-$month-$day)

Se adjuntan los ficheros con los mapas y las hojas de cálculo de la
**distribución de socixs** y **distribución de contratos** a dia **$year-$month-$day**.

Datos:

- detalle por municipios
- agregado por CCAA's, Provincias...

Mapas:

- En formatos png y svg (vectorial editable)
- Por CCAA y por provincias
- Relativos a la población y en números absolutos

**Aviso:** El mapa de províncias no está suficiente pulido para su publicación.


"

emili.py \
 --subject "Distribución socixs y contratos $year-$month-$day" \
 $TOOPTIONS \
 --from sistemes@somenergia.coop \
 --replyto david.garcia@somenergia.coop \
 --config $scriptpath/config.py \
 --format md \
 --style somenergia.css \
 "distribucion-socias-$year-$month-$day-detalle.csv" \
 "distribucion-socias-$year-$month-$day-agregado.csv" \
 "distribucion-contratos-$year-$month-$day-detalle.csv" \
 "distribucion-contratos-$year-$month-$day-agregado.csv" \
 "Mapa-distribución-socixs-$year-$month.svg" \
 "Mapa-distribución-socixs-$year-$month.png" \
 "Mapa-distribución-socixs-pob-$year-$month.svg" \
 "Mapa-distribución-socixs-pob-$year-$month.png" \
 "Mapa-distribución-contratos-$year-$month.svg" \
 "Mapa-distribución-contratos-$year-$month.png" \
 "Mapa-distribución-contratos-pob-$year-$month.svg" \
 "Mapa-distribución-contratos-pob-$year-$month.png" \
 "Mapa-distribución-socixs-provincias-$year-$month.svg" \
 "Mapa-distribución-socixs-provincias-$year-$month.png" \
 "Mapa-distribución-socixs-provincias-pob-$year-$month.svg" \
 "Mapa-distribución-socixs-provincias-pob-$year-$month.png" \
 "Mapa-distribución-contratos-provincias-$year-$month.svg" \
 "Mapa-distribución-contratos-provincias-$year-$month.png" \
 "Mapa-distribución-contratos-provincias-pob-$year-$month.svg" \
 "Mapa-distribución-contratos-provincias-pob-$year-$month.png" \
 --body "$TEXTOK" \
 || die
