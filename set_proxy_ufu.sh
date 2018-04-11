#!/bin/sh

if [ "$( grep 'proxy.ufu.br' /etc/profile )" = "" ]; then
	echo '
		export https_proxy="http://proxy.ufu.br:3128"
		export http_proxy="http://proxy.ufu.br:3128"
		export ftp_proxy="http://proxy.ufu.br:3128"
	' >> /etc/profile;
fi;

if [ "$( grep 'proxy.ufu.br' /etc/apt/apt.conf.d/10proxy )" = "" ]; then
	echo 'Acquire::http::Proxy "http://proxy.ufu.br:3128/";' > /etc/apt/apt.conf.d/10proxy;
fi;
