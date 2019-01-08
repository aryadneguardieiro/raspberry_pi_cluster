#!/bin/bash

qtdFiles=$(ls | grep csv$ | wc -l);
headers="timestamp";

#percorre os arquivos terminados em csv, montando o cabecalho apenas com o nome do arquivo sem extensao
for t in $(ls | grep csv$ | sed s/\.csv//g | sort); do
	headers="$headers,$t";
done
echo $headers;

#escolhe um arquivo para comecar
file_name=$(ls | grep csv$ | head -1);


#percorre as linhas do arquivo escolhido, vendo quais timestamps presentes neste arquivo também estão em todos os outros
#os timestamps que nao pertencerem a este arquivo ou que nao estiverem presentes em todos os demais serão excluidos
for t in $(tail -n +2 $file_name); do 
	#pega o timestamp
	x=$(echo $t | cut -d ',' -f 1);
	#pega a quantidade de arquivos que contem o timestamp recuperado
	qtd=$(cat $(ls | grep csv$) | grep $x | wc -l);
	#se essa quantidade for igual a quantidade de arquivos csv, entao o timestamp esta presente em todos os arquivos do diretorio
	if [ $qtd -eq $qtdFiles ]; then
		#seleciona as linhas que contem o timestamp recuperado considerando para todos os arquivos, e substitui o timestamp por uma string vazia
		line=$(echo $(cat $(ls | grep csv$ | sort) | grep $x) | sed s/$x,//g);
		#printa o timestamp recuperado, seguido das informações das linhas, substituindo espaco por virgula
		echo $x,"${line// /,}";
	fi
done;
