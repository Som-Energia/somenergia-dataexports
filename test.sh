#!/bin/bash

ok() {
    echo -e '\033[32mOK\033[0m'
    rm -f "$result"
}
ko() {
    echo -e '\033[31mKO See '$1'\033[0m'
}
step() {
    echo -e '\033[34;1m:: '$*'\033[0m'
} 

for data in 2015-01-31 2014-11-30 2014-10-31;
do
    result=b2bdata/aggregated-$data-result.csv
    expect=${result/result.csv/expected.csv}
    step Running sql2csv.py -C config.py distribucio_de_socies.sql --date "${data}"
    rm -f "$result"
    sql2csv.py -C config.py distribucio_de_socies.sql --date "${data}" > "$result" 2>&1 && diff "$expect" "$result" && ok "$result" || ko "$result"
done

for data in 2015-01-31 2014-11-30 2014-10-31;
do
    input=b2bdata/aggregated-$data-expected.csv
    result=b2bdata/sorted-$data-result.csv
    expect=${result/result.csv/expected.csv}
    step Running sql2csv.py -C config.py distribucio_de_socies.sql --date "${data}"
    rm -f "$result"
    python sort-csv.py --f "$input" --s order.txt --tab --c 3 --e exclude.txt --o "$result" 2>&1 && diff "$expect" "$result" && ok "$result" || ko "$result"
done

for data in 2015-01-31 2014-11-30 2014-10-31;
do
    result=b2bdata/aggregated-polisses-$data-result.csv
    expect=${result/result.csv/expected.csv}
    step Running sql2csv.py -C config.py distribucio_de_polissas.sql --date "${data}"
    rm -f "$result"
    sql2csv.py -C config.py distribucio_de_polissas.sql --date "${data}" > "$result" 2>&1 && diff "$expect" "$result" && ok "$result" || ko "$result"
done

for data in 2015-01-31 2014-11-30 2014-10-31;
do
    result=b2bdata/distribucio-$data-result.csv
    expect=${result/result.csv/expected.csv}
    step Running ./distribucio_de_socies.py "${data}"
    rm -f "$result"
    ./distribucio_de_socies.py "${data}" > "$result" 2>&1 && diff "$expect" "$result" && ok "$result" || ko "$result"
done

function allmaps() {
	year=$1
	month=$2
	for subject in socixs contratos
	do
		for ambit in '' '-pob' '-provincias' '-provincias-pob'
		do
			echo "Mapa-distribución-$subject$ambit-$year-$month"
		done
	done
}

year=2015
month=04
step Running ./mapa.py ${year} ${month}
allmaps $year $month | while read map
do
	rm -f "./$map.svg"
	rm -f "./$map.png"
done
./mapa.py $year $month || ko "generacio de mapes"

allmaps $year $month | while read map
do
	result=b2bdata/$map-result.svg
	expect=${result/result.svg/expected.svg}
	mv "$map".svg "$result"
	diff "$expect" "$result" && ok "$result" || ko "$result"
done
allmaps $year $month | while read map
do
	rm -f "./$map.png"
done


#./mchimp_generationsocis-sql.py >res 2>reserr; diff ref res && diff referr reserr && ok || ko


