#!/bin/bash

./mchimp_generationsocis-sql.py >ref 2>referr

for a in b2bdata/*result.csv
do
    mv $a ${a/result.csv/expected.csv}
done

for a in b2bdata/*result.svg
do
    mv $a ${a/result.svg/expected.svg}
done

