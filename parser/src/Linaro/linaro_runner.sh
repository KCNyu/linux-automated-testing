#!/bin/bash

python3 linaro_parse.py < $1 > result.txt
./linaro_send_to_lava.sh result.txt

rm result.txt