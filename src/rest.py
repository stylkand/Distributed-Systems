# DISTRIBUTED SYSTEMS - NTUA ECE 2021 - 2022
# Stylianos Kandylakis
# Kitsos Orfanopoulos
# Christos Tsoufis


# --------------Online Tutorials for Flask APP--------------
# https://medium.com/@karthikeyan.ranasthala/build-a-jwt-based-authentication-rest-api-with-flask-and-mysql-5dc6d3d1cb82

# --------------Prerequisites-----------------
# pip3 install -r requirements.txt


# --------------Terminal scripts--------------
# export FLASK_APP=api.py		for windows set FLASK_APP=api.py
# export FLASK_ENV=development       !!FOR DEBUG MODE!!
# flask run -h localhost -p 8765 --cert=adhoc
# set FLASK_DEBUG=1

import requests 
import json
from flask_cors import CORS
from flask import Flask, request
import copy
import numpy as np


# ours
import block
import node
import blockchain
import transaction



# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


# AUXILIARY FUNCTION
def printAndReturn(msg, code):
	print(msg)
	return msg, code




#🟦🟦🟦🟦🟦🟦🟦🟦-- API CREATION --🟦🟦🟦🟦🟦🟦🟦🟦

app = Flask(__name__)
CORS(app)

PORT = '5000' 
NODE_COUNTER = 0 
TOTAL_NODES = 0

myNode = node.Node()	
bootstrapNodeIP = '192.168.1.1' # noob1 VM
bootstrapNodeURL = 'http://192.168.1.1:' + PORT 



#🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨-- Initialize --🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨
# Initilization Endpoint. 
# Creates first transaction and first block, register node to set of nodes
@app.route('/init/<totalNodes>', methods=['GET'])
def initConnection(totalNodes):
	global TOTAL_NODES
	global PORT
	TOTAL_NODES = int(totalNodes)
	firstTransaction = myNode.createFirstTransaction(TOTAL_NODES)
	print('Creating a cluster of ' + str(TOTAL_NODES) + ' nodes')
	myNode.ourChain.createBlockchain(firstTransaction) # also creates genesis block
	myNode.id = 0
	myNode.register_node_to_nodeData(myNode.id, bootstrapNodeIP, PORT, myNode.wallet.publicKey)

	return "Success: Bootstrap initilization\n",200


#🟧🟧🟧🟧🟧🟧🟧🟧🟧🟧🟧🟧🟧🟧-- Connect to Boostrap--🟧🟧🟧🟧🟧🟧🟧🟧🟧🟧🟧🟧🟧🟧
# Every other node (except bootstraps) uses this endpoint to request permission
# to connect to the cluster. It sends its info and the bootstraps responds (see receive below)
@app.route('/connect/<myIP>/<port>', methods=['GET'])
def connect_node_request(myIP,port):
	# sending request for connection
	myInfo = 'http://' + myIP + port
	message = {'ip':myIP, 'port':port, 'publicKey':myNode.wallet.publicKey}
	message['flag']=0 	# flag=0 if connection request
	m = json.dumps(message)
	headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
	
	# receiving and processing request
	response = requests.post(bootstrapNodeURL + "/receive", data = m, headers = headers)
	data = response.json() 
	error = 'error' in data.keys()

	if (not error) :
		# sending data to bootstrap
		potentialID = int(data.get('id'))
		currentChain = data.get('chain')
		current_utxos = data.get('utxos')
		utxos_snapshot = data.get('utxos_snapshot')
		myNode.id = potentialID
		myNode.wallet.utxos = current_utxos
		myNode.wallet.utxos_snapshot = utxos_snapshot
		myNode.addBlockListToChain(myNode.ourChain.blockList, currentChain)
		message={}
		message['flag']=1 # flag 1 for other request
		message['publicKey']=myNode.wallet.publicKey

		# second response from bootstrap
		response = requests.post(bootstrapNodeURL + "/receive", data = json.dumps(message), headers = headers)
		return "Success: Connection for IP: " + myIP + " established,\nOK\n",200
	else:
		return "Error: Connection for IP: " + myIP + " to cluster refused, too many nodes\n",403
	
	
#🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥-- Bootstrap Receive --🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥
# Endpoint that receives messages for connect (see above)
@app.route('/receive', methods=['POST'])
def receiveNodeRequest():
	global NODE_COUNTER
	global TOTAL_NODES

	receivedMsg = request.get_json()
	
	if (receivedMsg.get('flag')==0): # flag 0 for connection requsts
		senderInfo = 'http://' + receivedMsg.get('ip') + ':' + receivedMsg.get('port')
		print(senderInfo)
		newID = -1
		
		if  NODE_COUNTER < TOTAL_NODES - 1:
			NODE_COUNTER += 1
			newID = NODE_COUNTER
			myNode.register_node_to_nodeData(newID, str(receivedMsg.get('ip')), receivedMsg.get('port'), receivedMsg.get('publicKey'))
			new_data = {}
			new_data['id'] = str(newID)
			new_data['utxos'] = myNode.wallet.utxos
			new_data['utxos_snapshot'] = myNode.wallet.utxos_snapshot
			blocks = []
			for block in myNode.ourChain.blockList:
				temp=copy.deepcopy(block.__dict__)
				temp['listOfTransactions']=block.listToSerialisable()
				blocks.append(temp)
			new_data['chain'] = blocks
			message = json.dumps(new_data)

			if(NODE_COUNTER == TOTAL_NODES-1):
				# we reached total nodes, inform everyone
				myNode.broadcast_nodeData()
			return message, 200 # OK
		else:
			message = {}
			message['error'] = 1
			return json.dumps(message),403

	else: # receiving data
		receiverID = myNode.public_key_to_nodeData_id(receivedMsg.get('publicKey'))
		# a new node connected to cluster. Let's give him free money!
		myNode.create_transaction(myNode.wallet.publicKey, myNode.id, receivedMsg.get('publicKey'), receiverID, 100) 
		return "Transfered 100 NBCs to Node\n", 200 # OK




#🟪🟪🟪🟪🟪🟪🟪🟪🟪🟪🟪🟪🟪🟪-- Receive Transaction --🟪🟪🟪🟪🟪🟪🟪🟪🟪🟪🟪🟪🟪🟪
# Endpoint to receive transaction
@app.route('/receive_trans',methods=['POST']) 
def receiveTransactions():
	data = request.get_json()
	trans = transaction.Transaction(**data) # ** operator expands the tuple into separate elements (see constructor of transaction)

	# check if transaction already received
	for unrec in myNode.unreceivedTransactions:
		if(trans.id == unrec.id):
			myNode.unreceivedTransactions = [t for t in myNode.unreceivedTransactions if t.id == unrec.id]
			return # ignore received transaction
	
	# check if transaction is valid
	code = myNode.isTransactionValid(myNode.wallet.utxos,trans)
	
	if (code == 'valid'):
		isBlockMined = myNode.addTransactionToValidList(trans)
		# check for double spending
		myNode.isReceivedValid()
		
		# check if after addition mining was required
		if (isBlockMined):
			return printAndReturn('Valid transaction added to block, mining block OK\n', 200)
		else:
			return printAndReturn('Valid transaction added to block OK\n', 200)
	
	elif (code == 'received'):
		myNode.add_transaction_to_pending(trans)
		return printAndReturn('Transaction added to list and is pending for approval\n', 200)
	
	else:
		return printAndReturn('Error: Invalid Transaction\n', 403)



#🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦-- Receive Block --🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦
# Endpoint to receive a block. We call receive_block to do the rest...
@app.route('/receive_block', methods = ['POST'])
def receiveBlock():
	data = request.get_json()
	b = block.Block(index = int(data.get('index')), previousHash = data.get('previousHash'))
	b.timestamp = data.get('timestamp')
	b.nonce = data.get('nonce')
	for t in data.get('listOfTransactions'):
		temp = transaction.Transaction(**t) #** operator expands the tuple
		b.listOfTransactions.append(temp)
	b.hash = data.get('hash')
	myNode.receive_block(b)
	return "Block received\n",200



#🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩-- Get Blockchain --🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩
# Endpoint to send the whole blockchain as a JSON (dictionary with key id)
@app.route('/get_blockchain',methods=['GET'])
def getBlockchain():
	message = {}
	blocks = []
	for block in myNode.ourChain.blockList:
		temp=copy.deepcopy(block.__dict__)
		temp['listOfTransactions']=block.listToSerialisable()
		blocks.append(temp)
	message['blockchain'] = blocks
	return json.dumps(message), 200


#🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫-- New Transaction --🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫
# Endpoint to create new transaction
@app.route('/transaction/new',methods=['POST'])
def newTransaction():
	data = request.get_json()
	amount = int(data.get('amount'))
	id = int(data.get('id'))
	# ip = myNode.nodeData[id].get('ip')
	# port = myNode.nodeData[id].get('port')
	recipient_address = myNode.nodeData[id].get('publicKey')
	senderID = myNode.id
	receiverID = myNode.public_key_to_nodeData_id(recipient_address)	
	ret = myNode.create_transaction(myNode.wallet.publicKey, senderID, recipient_address, receiverID, amount)
	message = {'response':ret}
	response = json.dumps(message)
	return response, 200




#🟦⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🟦-- Get Chain Length --🟦⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🟦
# Endpoint to get blockchain length
@app.route('/chain_length',methods=['GET'])
def getChainLength():
	message = {}
	message['length']= len(myNode.ourChain.blockList)
	return json.dumps(message), 200



#🟦🟦⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🟦🟦-- Show Balance --🟦🟦⬜⬜⬜⬜⬜⬜⬜⬜⬜🟦🟦
# Endpoint to get balance of wallet
@app.route('/show_balance', methods=['GET'])
def showBalance():
	balance = myNode.wallet.balance()
	response = {'Balance': balance}
	return json.dumps(response)+"\n", 200



#🟦🟦🟦⬜⬜⬜⬜⬜⬜⬜⬜🟦🟦🟦-- Get Transactions --🟦🟦🟦⬜⬜⬜⬜⬜⬜⬜⬜🟦🟦🟦
# Endpoint to get all transactions of the blockchain
@app.route('/transactions/get', methods=['GET'])
def getTransactions():
	transactions = blockchain.transactions
	response = {'transactions': transactions}
	return json.dumps(response)+"\n", 200



#🟦🟦🟦🟦⬜⬜⬜⬜⬜⬜🟦🟦🟦🟦-- View Transactions --🟦🟦🟦🟦⬜⬜⬜⬜⬜⬜🟦🟦🟦🟦
# Endpoint to view transactions
@app.route('/transactions/view', methods=['GET'])
def viewTransactions():
	last_transactions = myNode.ourChain.blockList[-1].listOfTransactions
	response = {}
	for t,i in zip(last_transactions,np.arange(len(last_transactions))):
		print(t)
		senderPublicKey = t.sender
		receiverPublicKey = t.receiver
		for id, info in myNode.nodeData.items():
			if info['publicKey'] == senderPublicKey:
				sender_id = id
			if info['publicKey'] == receiverPublicKey:
				receiver_id = id
		temp={}
		temp['sender_id']=sender_id
		temp['receiver_id']=receiver_id
		temp['amount']=t.amount
		response[str(i)] = temp
	return json.dumps(response)+"\n", 200


#🟦🟦🟦🟦🟦⬜⬜⬜⬜🟦🟦🟦🟦🟦-- View Blockchain --🟦🟦🟦🟦🟦⬜⬜⬜⬜🟦🟦🟦🟦🟦
# Endpoint to view the whole blockchains
@app.route('/blockchain/view', methods=['GET'])
def viewBlockchain():
	myNode.ourChain.printChain()
	return "OK",200


#🟦🟦🟦🟦🟦🟦⬜⬜🟦🟦🟦🟦🟦🟦-- Get Avg BlockTime --🟦🟦🟦🟦🟦🟦⬜⬜🟦🟦🟦🟦🟦🟦
# Endpoint to get the average block time 
@app.route('/time/block', methods=['GET'])
def getBlockTime():
	average = myNode.block_timer()
	response={}
	response['Average block time'] = average
	return json.dumps(response), 200


#🟦🟦🟦🟦🟦🟦🟥🟥🟦🟦🟦🟦🟦🟦-- Transactions Time --🟦🟦🟦🟦🟦🟦🟥🟥🟦🟦🟦🟦🟦🟦
# Endpoint to get transaction start and end times
@app.route('/time/transaction', methods=['GET'])
def transactionsTime():
	start, end = myNode.trans_timer()
	response = {}
	response['start'] = f'{start[3]}:{start[4]}:{start[5]}:{start[6]}:{start[7]}:{start[8]}'
	response['end'] = f'{end[3]}:{end[4]}:{end[5]}:{end[6]}:{end[7]}:{end[8]}'
	response['# transactions'] = myNode.numBlocks()
	return json.dumps(response), 200




#🟦🟥🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟥🟦-- nodeData --🟦🟥🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟥🟦
# Auxiliary Endpoint post nodeData info, a JSON with info for every node
@app.route('/connect/nodeData',methods=['POST'])
def get_ring():
	data = request.get_json()
	nodeData = {}
	for nodeID in data:
		temp = int(nodeID)
		nodeData[temp] = copy.deepcopy(data[nodeID])
	myNode.nodeData = nodeData
	return "OK",200


# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@- MAIN -@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# Main is called for each node to start a flask server
# User may give --port argument
if __name__ == '__main__':
	from argparse import ArgumentParser
	parser = ArgumentParser()
	parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
	args = parser.parse_args()
	port = args.port
	app.run(host='0.0.0.0', port=port)

