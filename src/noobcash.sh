#!/bin/bash

# DISTRIBUTED SYSTEMS - NTUA ECE 2021 - 2022
# Stylianos Kandylakis
# Kitsos Orfanopoulos
# Christos Tsoufis


function=$1

echo "$(tput setaf 7)Enter <help> for options"
echo "<Running: "$function">$(tput sgr0)"

functions=( "start" "init" "connect" "new_transaction" "view_transactions" "show_balance" )

expl=(	'start flask server'
		'initialize network with bootstrap node'
		'connect node to network'
		'create a transaction'
		"view transactions in last validated block"
		"view node\'s balance")

use=(	'use: ./noobcash.sh start <PORT>'
		'use: ./noobcash.sh init <PORT> <number of nodes>'
		'use: ./noobcash.sh connect <IP> <PORT>'
		'use: ./noobcash.sh new_transaction <PORT> <ID> <amount>'
		'use: ./noobcash.sh view_transactions <PORT>'
		'use: ./noobcash.sh balance <PORT>')

case $function in
	start)
		port=$2
		pip install termcolor
		pip install flask_cors
		pip install flask
		pip install requests
		pip install numpy
		pip install pycrypto


		export FLASK_APP=rest.py
		export FLASK_DEBUG=1
		flask run --host=0.0.0.0 --port=$port
		;;
	init)
		port=$2
		num_of_nodes=$3
		# use: ./noobcash.sh init <PORT> <number of nodes> 
		curl http://localhost:$port/init/$num_of_nodes
		;;
	connect)
		ip=$2
		port=$3
		# use: ./noobcash.sh connect <IP> <PORT>
		# IP format: 192.168.1.<num>
		curl http://localhost:$port/connect/$ip/$port
		;;
	new_transaction)
		port=$2
		id=$3
		amount=$4
		data="{\"id\":\"$id\",\"amount\":$amount}"
		# use ./noobcash.sh new_transaction <PORT> <ID> <amount>
		curl -d $data -H "Content-Type: application/json" -X POST http://localhost:$port/transaction/new
		;;
	view_transactions)
		port=$2
		# use ./noobcash.sh view_transactions <PORT>
		curl http://localhost:$port/transactions/view
		;;
	show_balance)
		port=$2
		# use ./noobcash.sh balance <PORT>
		curl http://localhost:$port/show_balance
		;;
	help)
		for i in {0..5}
		do
			echo "$(tput setaf 3)"
			echo "$(tput setaf 6)${functions[$i]}$(tput setaf 3):  ${expl[$i]}"
			echo "${use[$i]}"
			echo "$(tput setaf 4)~~~~~~~~~~"
		done
		;;
	*)
esac

echo ""
echo "$(tput setaf 6)<Done>$(tput sgr0)"