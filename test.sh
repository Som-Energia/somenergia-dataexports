#!/bin/bash

./mchimp_generationsocis-sql.py >res 2>reserr; diff ref res && diff referr reserr && echo -e '\033[32mOK\033[0m' || echo -e '\033[31mKO\033[0m'

