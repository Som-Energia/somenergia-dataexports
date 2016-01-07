#!/bin/bash

die() {
    exit -1
}
step() {
    echo -e '\033[34;1m:: '$*'\033[0m'
}

 
TOOPTIONS=$(
while read r
do
    [ -n "$r" ] &&  echo "--to $r"
done < recipients-distribucio
)

echo $TOOPTIONS


today=$(date -I)
IFS='-' read -r year month day <<< "$today" # split date
lastMonthEnd=$(date -I -d "$year-$month-01 - 1 day") # last day of last month


IFS='-' read -r year month day <<< "${1:-$lastMonthEnd}" # split date

step "Generating reports at $year-$month-$day"

./mapa_socis.py $year $month || die
./distribucio_de_socies.py "$year-$month-$day" > distribucion-socias-$year-$month-$day-detalle.csv || die
./sql2csv.py distribucio_de_socies.sql --data "$year-$month-$day" > distribucion-socias-$year-$month-$day-agregado.csv || die

./sendmail.py \
    --subject "Distribución socixs $year-$month-$day" \
    $TOOPTIONS \
    --from sistemes@somenergia.coop \
    --cc david.garcia@somenergia.coop \
    --replyto david.garcia@somenergia.coop \
    --body "Adjuntos van los ficheros de la distribución de socixs a día $year-$month-$day" \
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
    || die
    


