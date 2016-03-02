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
./mapa_socis.py $year $month || die
step "  Generant dades detallades"
./distribucio_de_socies.py "$year-$month-$day" > distribucion-socias-$year-$month-$day-detalle.csv || die
step "  Generant dades aggregades"
./sql2csv.py distribucio_de_socies.sql --data "$year-$month-$day" > distribucion-socias-$year-$month-$day-agregado.csv || die

step "Sending results..."

TEXTOK="
# Distribución de socixs ($year-$month-$day)

Se adjuntan los ficheros con los mapas y las hojas de cálculo de la
**distribución de socixs** a dia **$year-$month-$day**.

Datos:

- detalle por municipios
- agregado por CCAA's, Provincias...

Mapas:

- En formatos png y svg (vectorial editable)
- Por CCAA y por províncias
- Relativos a la poblacio y en números absolutos

**Aviso:** El mapa de províncias no está suficiente pulido para su publicación.

"

emili.py \
    --subject "Distribución socixs $year-$month-$day" \
    $TOOPTIONS \
    --from sistemes@somenergia.coop \
    --replyto david.garcia@somenergia.coop \
    --config $scriptpath/config.py \
    --format md \
    --style somenergia.css \
    "distribucion-socias-$year-$month-$day-detalle.csv" \
    "distribucion-socias-$year-$month-$day-agregado.csv" \
    "SocisPerCCAA-absoluts-$year-$month.svg" \
    "SocisPerCCAA-absoluts-$year-$month.png" \
    "SocisPerCCAA-relatius-$year-$month.svg" \
    "SocisPerCCAA-relatius-$year-$month.png" \
    "SocisPerProvincies-absoluts-$year-$month.svg" \
    "SocisPerProvincies-absoluts-$year-$month.png" \
    "SocisPerProvincies-relatius-$year-$month.svg" \
    "SocisPerProvincies-relatius-$year-$month.png" \
    --body "$TEXTOK" \
    || die


