#!/bin/bash

if [ $# -ne 1 ]; then
	echo "Usage: aggregate csv_directory"
	exit 1
fi

directory=$1

cd $directory

qtdFiles=$(ls | grep csv$ | wc -l);

echo "timestamp,"$(ls | grep csv$ | sort | sed s/\.csv//g) | sed s/\ /,/g;

#escolhe um arquivo para comecar
file_name=$(ls | grep csv$ | head -1);


#percorre as linhas do arquivo escolhido, vendo quais timestamps presentes neste arquivo também estão em todos os outros
#os timestamps que nao pertencerem a este arquivo ou que nao estiverem presentes em todos os demais serão excluidos
for t in $(tail -n +2 $file_name); do
	#pega o timestamp
	timestamp=$(echo $t | cut -d ',' -f 1);
	grep -r "^$timestamp" > /tmp/grepXFiles
	qtd=$(cat /tmp/grepXFiles | wc -l);

	if [ $qtd -eq $qtdFiles ]; then
		echo $timestamp,$(cat /tmp/grepXFiles | sort | cut -d ':' -f 2 | cut -d ',' -f 2 | sed s/\\r//g) | sed s/' '/,/g;
	fi
done;
rm /tmp/grepXFiles
exit 0
