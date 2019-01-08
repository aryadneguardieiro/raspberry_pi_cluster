#!/bin/bash

qtdFiles=$(ls | grep csv$ | wc -l);
headers="timestamp";
for t in $(ls | grep csv$ | sed s/\.csv//g | sort); do
	headers="$headers,$t";
done
echo $headers;

file_name=$(ls | grep csv$ | head -1);

for t in $(tail -n +2 $file_name); do 
	x=$(echo $t | cut -d ',' -f 1);
	qtd=$(cat $(ls | grep csv$) | grep $x | wc -l);
	if [ $qtd -eq $qtdFiles ]; then
		line=$(echo $(cat $(ls | grep csv$ | sort) | grep $x) | sed s/$x,//g);
		echo $x,"${line// /,}";
	fi
done;
