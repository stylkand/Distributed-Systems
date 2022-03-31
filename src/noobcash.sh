#!/bin/bash

# DISTRIBUTED SYSTEMS - NTUA ECE 2021 - 2022
# Stylianos Kandylakis
# Kitsos Orfanopoulos
# Christos Tsoufis

func=$1
port=$2

if [ "$#" -lt 2 ] # if arguments are less than two then print usage error
then
	echo "$(tput setaf 6)Usage: ./noobcash.sh <action/help> $(tput bold)PORT$(tput sgr0)"
else
	case $func in
		start)
			pip3 install requirements.txt
			export FLASK_APP=rest.py
			export FLASK_DEBUG=1
			flask run --host=0.0.0.0 --port=$port
			;;
		init)
			if [ "$#" -ne 3 ] # if arguments for init are not 3 print usage error
			then
				echo "$(tput setaf 6)Usage: ./noobcash.sh init $(tput bold)PORT num_of_nodes$(tput sgr0)"
			else
				totalNodes=$3
				curl http://localhost:$port/init/$totalNodes
			fi
			;;
		connect)
			if [ "$#" -ne 3 ] # if arguments for connect are not 3 print usage error
			then
				echo "$(tput setaf 6)Usage: ./noobcash.sh connect $(tput bold)PORT IP$(tput sgr0)"
			else
				ip=$3
				curl http://localhost:$port/connect/$ip/$port
			fi
			;;
		*)
	esac
fi

