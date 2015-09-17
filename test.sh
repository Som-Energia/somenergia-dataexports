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

for data in 2015-02-01 2014-12-01 2014-11-01;
do
    result=b2bdata/pere-$data-result.csv
    expect=${result/result.csv/expected.csv}
    step Running ./sql2csv.py distribucio_de_socies.sql --data "${data}"
    rm -f "$result"
    ./sql2csv.py distribucio_de_socies.sql --data "${data}" > "$result" 2>&1 && diff "$expect" "$result" && ok "$result" || ko "$result"
done

for data in 2015-02-01 2014-12-01 2014-11-01;
do
    result=b2bdata/distribucio-$data-result.csv
    expect=${result/result.csv/expected.csv}
    step Running ./distribucio_de_socies.py "${data}"
    rm -f "$result"
    ./distribucio_de_socies.py "${data}" > "$result" 2>&1 && diff "$expect" "$result" && ok "$result" || ko "$result"
done

#./mchimp_generationsocis-sql.py >res 2>reserr; diff ref res && diff referr reserr && ok || ko


