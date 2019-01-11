#!/bin/bash

if [ $# -ne 2 ]; then
	echo "Usage: filter_timestamp y_file x_file";
else
	y_name="$1";
	unified_csv="$2";

	echo $(head -n 1 $y_name) > y_csv_file.csv;
	echo $(head -n 1 $unified_csv) > x_csv_file.csv;

	for t in $(tail -n +2 $y_name); do
		timestamp=$(echo $t | cut -d ',' -f 1);
		search=$(cat $unified_csv | grep -m 1 $timestamp);
		if [ "$search" != "" ]; then
			echo $t >> y_csv_file.csv;
			echo $search >> x_csv_file.csv;
		fi
	done
fi
