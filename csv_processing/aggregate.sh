#!/bin/bash

if [ $# -ne 2 ]; then
	echo "Usage: aggregate file_extension(txt, csv) some_file_name";
else
	qtdFiles=$(ls | grep -v aggregate | wc -l);
	count=0;
	underline="_";
	headers="timestamp";
	for t in $(ls | grep -v aggregate | sort); do
		hd=$(head -1 $t);
		OLDIFS="$IFS";
		IFS=",";
		arr=($hd);
		IFS="$OLDIFS";
		for i in $(seq 2 ${#arr[@]}); do
			pos=$((i-1));
			headerItem=${arr[$pos]};
			qtdFilesHasHeaderItem=$(head -1 $(ls | grep -v aggregate) | grep $headerItem | wc -l);
			if [ $qtdFilesHasHeaderItem -ge 2 ] && [ $count -ge 1 ]; then
				headers=$(echo $headers,$headerItem$underline$count);
			else 
				headers=$(echo $headers,$headerItem);
			fi
		done
		count=$(echo $count + 1 | bc)
	done
	echo $headers;

	for t in $(tail -n +2 $2); do 
		x=$(echo $t | cut -d ',' -f 1);
		qtd=$(cat $(ls | grep -v aggregate) | grep $x | wc -l);
		if [ $qtd -eq $qtdFiles ]; then
			line=$(echo $(cat $(ls | grep -v aggregate | sort) | grep $x) | sed s/$x,//g);
			echo $x,"${line// /,}";
		fi
	done;
fi
