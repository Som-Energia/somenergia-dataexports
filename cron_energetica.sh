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
done < recipients-energetica
)
date


today=$(date -I)
IFS='-' read -r year month day <<< "$today" # split date
lastMonthEnd=$(date -I -d "$year-$month-01 - 1 day") # last day of last month
IFS='-' read -r year month day <<< "${1:-$lastMonthEnd}" # split date

step "Generant resum del $year-$month-$day"
sql2csv.py resum_energeticacoop.sql > resumen-contratos-energeticacoop-$year-$month-${day}.csv || die

step "Enviant resultats..."

TEXTOK="
# Contratos comercializados para EnergEtica.coop ($year-$month-$day)

Se adjuntan los ficheros con la relación de contratos
comercializados por SomEnergia para EnergEtica
a dia **$year-$month-$day**.

"

emili.py \
    --subject "Contratos EnergEtica, $year-$month-$day" \
    $TOOPTIONS \
    --from sistemes@somenergia.coop \
    --replyto david.garcia@somenergia.coop \
    --config $scriptpath/config.py \
    --format md \
    --style somenergia.css \
    "resumen-contratos-energeticacoop-$year-$month-${day}.csv" \
    --body "$TEXTOK" \
    || die


