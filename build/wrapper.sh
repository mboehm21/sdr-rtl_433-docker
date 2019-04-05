#!/bin/bash

#rtl_433 -M newmodel -G -F json 2> /dev/null | \
rtl_433 $SDR_PARAMS -M newmodel -F json 2> /dev/null | \
while read i
do
	./to_influx.py $i
done
