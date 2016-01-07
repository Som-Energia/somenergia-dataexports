#!/bin/bash

./mchimp_generationsocis-sql.py >ref 2>referr

for a in b2bdata/*result*
do
    mv $a ${a/result.csv/expected.csv}
done

