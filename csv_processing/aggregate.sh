#!/bin/bash

qtdFiles=$(ls | grep csv | wc -l);
count=1;
underline="_";
headers="timestamp";
for t in $(ls | grep csv | sort); do
	hd=$(head -1 $t);
	OLDIFS="$IFS";
	IFS=",";
	arr=($hd);
	IFS="$OLDIFS";
	for i in $(seq 2 ${#arr[@]}); do
		pos=$((i-1));
		headerItem=${arr[$pos]};
		headers=$(echo $headers,$headerItem$underline$count);
	done
	count=$((count + 1))
done
echo $headers;

file_name=$(ls | grep csv | head -1);

for t in $(tail -n +2 $file_name); do 
	x=$(echo $t | cut -d ',' -f 1);
	qtd=$(cat $(ls | grep csv) | grep $x | wc -l);
	if [ $qtd -eq $qtdFiles ]; then
		line=$(echo $(cat $(ls | grep csv | sort) | grep $x) | sed s/$x,//g);
		echo $x,"${line// /,}";
	fi
done;
