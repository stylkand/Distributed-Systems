# DISTRIBUTED SYSTEMS - NTUA ECE 2021 - 2022
# Stylianos Kandylakis
# Kitsos Orfanopoulos
# Christos Tsoufis


# MAIN OBJECT FOR NODES 

from Crypto.Hash import SHA256

import json
import requests
import copy
import threading
import time
# import os

# ours 
import block
import blockchain
import transaction
import threadpool
import wallet

CAPACITY = 1	# 1 or 5 or 10
DIFFICULTY = 4	# 4 or 5
init_count = -1 		

T_startTime = None
T_endTime = None
block_time = 0

lock = threading.Lock()

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@



class Node: 

	# 🟩🟩🟩 Constructor 🟩🟩🟩
	def __init__(self,NUM_OF_NODES=None):
		self.wallet = wallet.Wallet()			# create wallet
		self.id = -1 							# set id to -1 (bootstrap procedure will give us the correct one)
		self.ourChain = blockchain.Blockchain()	# create chainblock		
		self.nodeData = {} 						# set node data {id, (ip:port), publick ey, balance}
		self.pool = threadpool.Threadpool()		# create threadpool (1 or 2 threads for 5 or 10 nodes respectively)	
		self.receivedTransactions = []			# list of received transactions (not yet valid)
		self.unreceivedTransactions = []		# list of transactions that are known because of a received block, they are not received individually
		self.validTransactions = []				# list of valid transactions for new block
		self.oldTransactions = []				# list of old valid transactions (miner may empties them while mining)



	# 🟨🟨 SIMPLE "GETTERS" 🟨🟨


	# 🟨🟨
	# get startTime and endTime of transaction
	def trans_timer(self):
		global T_endTime, T_startTime
		return T_startTime, T_endTime

	# 🟨🟨🟨🟨
	# avg time per block
	def block_timer(self):
		global block_time
		return block_time/len(self.ourChain.blockList)

	# 🟨🟨🟨🟨🟨🟨
	# get number of total transactions
	def numBlocks(self):
		return CAPACITY*len(self.ourChain.blockList)

	# 🟨🟨🟨🟨🟨🟨🟨🟨
	# get index of a node, given its public key
	def public_key_to_nodeData_id(self, publicKey):
		for i in self.nodeData:
			data = self.nodeData[i]
			if data['publicKey'] == publicKey:
				return i




# 🟧🟧 BROADCAST 🟧🟧
	
	# 🟧🟧
	# creates URL
	def toURL(self,nodeID):
		url = "http://%s:%s"%(self.nodeData[nodeID]['ip'],self.nodeData[nodeID]['port'])
		return url

	# 🟧🟧🟧🟧
	# main broadcast function, broadcasts a general message to every other node
	def broadcast(self,message, URLparameter):
		m = json.dumps(message) # convert to json
		headers = {'Content-type': 'application/json', 'Accept': 'text/plain'} # headers of http post request
		for nodeID in self.nodeData:	 		# nodeData has as many object as the nodes
			if (nodeID != self.id):				# exclude current node
				nodeURL = self.toURL(nodeID) 	# creates URL for target node
				requests.post(nodeURL+"/"+URLparameter, data = m, headers = headers) # create post request
		return

	# 🟧🟧🟧🟧🟧🟧
	# this functions utilizes the broadcast() to broadcast one transaction
	def broadcast_transaction(self, transaction):
		URLparameter = "receive_trans"
		message = copy.deepcopy(transaction.__dict__)
		self.broadcast(message,URLparameter)
		return

	# 🟧🟧🟧🟧🟧🟧🟧🟧
	# this functions utilizes the broadcast() one to broadcast one block
	def broadcast_block(self, block):
		URLparameter = "receive_block"
		message = copy.deepcopy(block.__dict__)
		message['listOfTransactions'] = block.listToSerialisable()
		self.broadcast(message, URLparameter)
		return

	# 🟧🟧🟧🟧🟧🟧🟧🟧🟧🟧
	# this functions utilizes the broadcast() to broadcast nodeData (usefull for bootstrap)
	def broadcast_nodeData(self):
		print(self.nodeData)
		url="connect/nodeData" 
		message=self.nodeData
		self.broadcast(message,url)






	# 🟪🟪 NODES AND BOOTSTRAP 🟪🟪

	# 🟪🟪
	# This function takes a blockList of JSON block objects and creates a chainblock, with list of objects
	def addBlockListToChain(self,ourChain_list, blockList):
		# reads blocks from blockList (as JSON) and creates blockChain
		for data in blockList:
			newBlock = block.Block(index = data.get('index'), previousHash = data.get('previousHash'))
			newBlock.nonce = data.get('nonce')
			newBlock.hash = data.get('hash')
			newBlock.timestamp = data.get('timestamp')
			newBlock.listOfTransactions = []		
			for t in data.get('listOfTransactions'):
				newBlock.listOfTransactions.append(transaction.Transaction(**t))
			ourChain_list.append(newBlock)
		return

	# 🟪🟪🟪🟪
	# Create first transaction (giving free money to bootstrap)
	def create_genesis_transaction(self,totalNodes):
		sender=self.wallet.publicKey # get public key from bootstrap node
		initialAmount=100*totalNodes # initial balance of bootstrap

		# initialize first transaction arguments
		data={}
		data['receiver']=data['sender']=sender
		data['transaction_inputs']=[]
		data['transaction_outputs']=[]
		data['transaction_outputs'].append(outpt_sender)
		data['transaction_outputs'].append(outpt_receiver)
		outpt_sender = outpt_receiver = {"id":0,"to_who":sender,"amount":initialAmount}
		data['amount']=initialAmount
		data['id']=0
		data['senderID']=0
		data['receiverID']=0
		data['signature']=None
		trans = transaction.Transaction(**data) # ** operator expands the tuple into separate elements (see constructor of transaction)

		# add first transaction UTXO to wallet
		init_utxos={}
		init_utxos[sender]=[{"id":0,"to_who":sender,"amount":initialAmount}]
		self.wallet.utxos=init_utxos # bootstrap wallet has 100*n NBCs
		self.wallet.utxos_snapshot=copy.deepcopy(init_utxos)
		return trans

	# 🟪🟪🟪🟪🟪🟪
	# Add node to nodeData set. Only bootstrap can do this
	# Bootstrap node broadcast the registation to all other nodes and gives the new node an ID and 100 NBCs
	def register_node_to_nodeData(self, nodeID, ip, port, publicKey):
		if self.id == 0:
			self.nodeData[nodeID] = {'ip': ip,'port': port,'publicKey': publicKey}
			if(self.id!=nodeID):
				self.wallet.utxos[publicKey]=[] # initialize utxos of other nodes
		else:
			print("Error-register: this node is not boostrap")
		return





	# 🟦🟦 TRANSACTIONS 🟦🟦

	# 🟦🟦
	# This function checks if a transaction is valid and return a corresponding message
	def isTransactionValid(self, walletUTXOs, t): 
		try:
			# check signature
			if not t.verify_signature():
				raise Exception('Error: invalid signature')

			# check if sender == receiver
			if t.sender == t.receiver:
				raise Exception('sender must be different from recepient')

			# check if amount is negative
			if t.amount <= 0:
				raise Exception('Error: negative amount?')

			# We check if the sender has indeed the amount of noobcash that he says
			senderUTXOs= copy.deepcopy(walletUTXOs[t.sender])
			senderTotalMoney=0
			# calculate senderTotalMoney
			for transactionID in t.transaction_inputs:
				found=False
				for utxo in senderUTXOs:
					if utxo['id']== transactionID and utxo['to_who']==t.sender:
						found=True # found one output which has the sender
						senderTotalMoney += utxo['amount']
						senderUTXOs.remove(utxo)
						break # maybe not usefull
				
				# if we didn't find any output we shall wait, thus 'pending'
				if not found:
					return 'pending'

			temp = []
			# has no outputs "header"
			if (temp != t.transaction_outputs):
				raise Exception('Wrong outputs')

			if (senderTotalMoney >= t.amount): # correct amount, add transaction to temp to check
				temp.append({'id': t.id, 'to_who': t.sender, 'amount': senderTotalMoney - t.amount })
				temp.append({'id': t.id, 'to_who': t.receiver, 'amount':  t.amount })
			
			# no transaction has been made with receiver, initialize his wallet
			if(t.receiver not in walletUTXOs.keys()):
				walletUTXOs[t.receiver]=[]
			
			# only two nodes take part in each transaction, thus outputs=2
			if(len (t.transaction_outputs) == 2):
				senderUTXOs.append(t.transaction_outputs[0]) #removed old utxos , added
				walletUTXOs[t.sender]=senderUTXOs	
				walletUTXOs[t.receiver].append(t.transaction_outputs[1])
			else:
				walletUTXOs[t.sender]=senderUTXOs
				walletUTXOs[t.receiver].append(t.transaction_outputs[0])
			return 'valid'

		except Exception as e:
			print(f"validate transaction: {e.__class__.__name__}: {e}")
			return 'error'


	# 🟦🟦🟦🟦
	# Add a transaction to validTransactions block list and check it that is full
	def add_transaction_to_validated(self, transaction):
		global CAPACITY
		self.oldTransactions.append(transaction)
		self.validTransactions.append(transaction)
		if len(self.validTransactions) == CAPACITY: # did we reach max capacity 
			temp = copy.deepcopy(self.validTransactions) 					
			self.validTransactions = []									
			future = self.pool.submitTask(self.createBlockAndMine, temp, copy.deepcopy(self.wallet.utxos)) # start mining, see below
			return True				
		else:
			return False

	# 🟦🟦🟦🟦🟦🟦
	def create_transaction(self, senderPublicKey, senderID, receiverPublicKey, receiverID, amount):
		sum = 0
		inputs = []
		
		# update startTime of transaction
		global T_startTime
		if (not T_startTime):
			T_startTime = time.gmtime(time.time())

		try:
			if(self.wallet.balance() < amount):
				raise Exception("Error: not enough NBCs!")
			key = senderPublicKey
			for utxo in self.wallet.utxos[key]:
				inputs.append(utxo['id'])
				sum = sum + utxo['amount']
				if (amount <= sum):
					break
			newTransaction = copy.deepcopy(transaction.Transaction(senderPublicKey, senderID, receiverPublicKey, receiverID, amount, inputs))
			newTransaction.sign_transaction(self.wallet.privateKey) #set id & signature
			newTransaction.transaction_outputs.append({'id': newTransaction.id, 'to_who': newTransaction.sender, 'amount': sum-newTransaction.amount})
			newTransaction.transaction_outputs.append({'id': newTransaction.id, 'to_who':newTransaction.receiver, 'amount': newTransaction.amount})

			if(self.isTransactionValid(self.wallet.utxos,newTransaction) == 'valid'): # Node validates the newTransaction it created
				self.add_transaction_to_validated(newTransaction)
				self.broadcast_transaction(newTransaction)
				return "Created new transaction!"
			else:
				return "Error: Transaction not created"
		
		except Exception as e:
			print(f"create_transaction: {e.__class__.__name__}: {e}")
			return "Error: not enough NBCs!"


	# 🟦🟦🟦🟦🟦🟦🟦🟦
	# Check if any of the received transactions can be validated
	def isReceivedValid(self):
		for t in self.receivedTransactions:
			if self.isTransactionValid(self.wallet.utxos, t) == 'valid':
				self.receivedTransactions = [t for t in self.receivedTransactions if t.id not in self.receivedTransactions]
				self.add_transaction_to_validated(t)

	# 🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦
	# add transaction to receivedTransactions
	def add_transaction_to_pending(self, t):
		self.receivedTransactions.append(t)


	# 🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦
	# remove transaction from oldTransactions
	def removeFromOldTransactions(self, targetTransaction):
		self.oldTransactions = [trans for trans in self.oldTransactions if trans not in targetTransaction]





	# 🟫🟫 BLOCKS 🟫🟫
	# We will use threads, one thread = 1 node. 
	# Thus received-sending blocks is managed by threads/nodes
	# Some of the functions below are thread-based


	# 🟫🟫
	# Check if previous hash of the block is the same with "our" previous hash
	# Also check if given hash code is the same with what we find if we hash the block
	def isBlockValid(self, targetBlock):
		return targetBlock.previousHash == self.ourChain.blockList[-1].hash and targetBlock.hash == targetBlock.myHash()

	# 🟫🟫🟫🟫
	# This function used when a block is received
	def receive_block(self, block):
		global lock, T_endTime

		tempUTXOs = copy.deepcopy(self.wallet.utxos_snapshot)
		# we must REDO all the transactions of th block to check if it is valied (we do not trust the sender)
		if self.blockREDO(block, tempUTXOs):
			# @@@@@@@  LOCK  @@@@@@
			# due to multiple threads we must lock before adding another block to blockchain
			lock.acquire()
			if self.isBlockValid(block):
				self.ourChain.addBlock(block)
				
				global block_time, totalBlocks
				T_endTime = time.gmtime(time.time())
				
				self.wallet.utxos_snapshot = copy.deepcopy(tempUTXOs)
				self.wallet.utxos = copy.deepcopy(tempUTXOs)

				
				lock.release()
				
				# remove from receivedTransactions every transacton that was in the block
				self.receivedTransactions = [trans for trans in self.receivedTransactions if trans not in block.listOfTransactions]
				
				# ad# @@@@@@@ UNLOCK @@@@@@d to unreceived
				new_unreceived = [trans for trans in block.listOfTransactions if trans not in (self.oldTransactions and self.receivedTransactions)]
				for t in new_unreceived:
					self.unreceivedTransactions.append(t)
				
				# update valid Transactions
				new_valid = [trans for trans in self.oldTransactions if trans not in block.listOfTransactions]
				self.validTransactions = []
				# remove current from old list
				self.removeFromOldTransactions(block.listOfTransactions)

				for t in new_valid:
					self.add_transaction_to_validated(t)
				# Try validate received
				self.isReceivedValid() 			

			else: # if block is not valid
				# @@@@@@@ UNLOCK @@@@@@
				lock.release()

				self.resolveBlock()
		else:
			self.resolveBlock()


	# 🟫🟫🟫🟫🟫🟫
    # Function that created a new block, given a list of valid transactions
	def createNewBlock(self, validTransactions):	 
		if len(self.ourChain.blockList) == 0: # if this block is the first one
			index = 0
			prevHash = 0
		else:
			prevBlock = self.ourChain.blockList[-1]
			index = prevBlock.index + 1
			prevHash = prevBlock.hash
		newBlock = block.Block(index = index, previousHash = prevHash)
		newBlock.listOfTransactions = validTransactions
		return newBlock


	# 🟫🟫🟫🟫🟫🟫🟫🟫
	# MINE! Or in simple words lose your time guessing the correct nonce
	def mineBlock(self, block, difficulty = DIFFICULTY):
		guess = block.myHash() # nonce is initialized to 0
		while guess[:difficulty]!=('0'*difficulty): # not enough zeros at hashing
			block.nonce += 1 # try the next nonce
			guess = block.myHash() 
		block.hash = guess
		return


	# 🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫
	# Function that creates a block and starts mining
	def createBlockAndMine(self, validTransactions, current_utxos):

		global lock, T_endTime, block_time

		newBlock = self.createNewBlock(validTransactions)
		tempUTXOs = copy.deepcopy(self.wallet.utxos_snapshot)
		if not self.blockREDO(newBlock, tempUTXOs):
			return
		self.mineBlock(newBlock)


		lock.acquire()
		# @@@@@@@  LOCK  @@@@@@
		# due to multiple threads we must lock before adding another block to blockchain
		if self.isBlockValid(newBlock):
			self.ourChain.addBlock(newBlock)
			T_endTime = time.gmtime(time.time())
			
			self.removeFromOldTransactions(validTransactions)
			self.wallet.utxos_snapshot = tempUTXOs

			# @@@@@@@ UNLOCK @@@@@@
			lock.release()
			block_time+=time.thread_time()
			self.broadcast_block(newBlock)
		else:
			# @@@@@@@ UNLOCK @@@@@@
			lock.release()





	# 🟥🟥 CONSENSUS 🟥🟥

	# 🟥🟥
	# Redo all the transactions in a block and check if they are valid
	def blockREDO(self, block, UTXOs):
		for trans in block.listOfTransactions:
			if (self.isTransactionValid(UTXOs, trans) != 'valid'):
				print("Failed Transaction: ")
				print('\t\tsender id: ' + str(trans.senderID) + ' \t\treceiver id: '+ str(trans.receiverID) + ' \t\tamount: '+ str(trans.amount))
				return False
		return True

	# 🟥🟥🟥🟥
	# check if hashes of every block are valid
	def isChainHashesValid(self,chain):
		ourPreviousHash = chain[0].hash

		for block in chain[1:]:
			if(block.previousHash != ourPreviousHash or block.hash != block.myHash()):
				return False
			ourPreviousHash = block.hash
		return True

	# 🟥🟥🟥🟥🟥🟥
	# validates and returns list of block objects
	def isChainValid(self, blocklist):
		
		chain = []
		# initialize received and unreceived transactions
		received = copy.deepcopy(self.receivedTransactions) # we will use these lists just for validation and
		valid = copy.deepcopy(self.validTransactions)
		received += valid
		unreceived = copy.deepcopy(self.unreceivedTransactions)	# then we will add them to node's lists
		tempUTXOs = {}

		# REDO bootstrap's UTXOs which are not valid
		btstrp_public_k = self.nodeData[0]['publicKey']
		amount = len(self.nodeData.keys())*100 # number of nodes * 100 NBCs
		tempUTXOs[btstrp_public_k] = [{"id":0,"to_who":btstrp_public_k,"amount":amount}]

		self.addBlockListToChain(chain,blocklist)

		if not self.isChainHashesValid(chain):
			print("Error: chains has invalid hashes")
			return False

		count = 1 # index to new chain
		# i is our old block, j the block from new blockchain
		for i, j in zip(self.ourChain.blockList[1:], chain[1:]):

			oldTransaction = i.listOfTransactions
			newTransaction = j.listOfTransactions
			A = [t for t in oldTransaction if t not in newTransaction]
			B = [t for t in newTransaction if t not in oldTransaction]
			# if received transactions in new block, remove them, and add received from i
			tempReceived = [t for t in received if t not in B] + [t for t in A if t not in unreceived]
			# if unreceived transactions in i, remove them, and add unreceived from j
			tempUnreceived = [t for t in unreceived if t not in A] + [t for t in B if t not in received]

			# REDO block and check its validity
			if( not self.blockREDO(j,tempUTXOs)):
				# print("Chain invalid!")
				return False,None,None

			received = tempReceived
			unreceived = tempUnreceived
			count+=1

		# continue validating chain
		for j in chain[count:]:

			newTransaction = j.listOfTransactions
			tempReceived = [t for t in received if t not in newTransaction]
			tempUnreceived = unreceived + [t for t in newTransaction if t not in received]

			if( not self.blockREDO(j,tempUTXOs) ):
				return False,None,None

			print("valid")
			received = tempReceived
			unreceived = tempUnreceived

		# It is valid
		self.receivedTransactions = copy.deepcopy(received)
		self.unreceivedTransactions = copy.deepcopy(unreceived)
		self.oldTransactions = []
		self.validTransactions = []
		return True, chain, tempUTXOs


	# 🟥🟥🟥🟥🟥🟥🟥🟥 
	def resolveBlock(self):
		#resolve correct chain
		maxLength = len(self.ourChain.blockList)
		maxID = self.id
		maxIP= self.nodeData[maxID]['ip']
		maxPort= self.nodeData[maxID]['port']
		#check if someone has longer blockchain
		try:
			for key in self.nodeData:
				node=self.nodeData[key]
				if node['publicKey'] == self.wallet.publicKey:
					continue
				n_id= key
				n_ip = node['ip']
				n_port = node['port']
				url = f'http://{n_ip}:{n_port}/chain_length'
				response = requests.get(url)
				if response.status_code != 200:
					raise Exception('Invalid blockchain length response')

				receivedBlockchainLength = int(response.json()['length'])
				if receivedBlockchainLength > maxLength:
					print(f'consensus.{n_id}: Found longer blockchain => {receivedBlockchainLength}')
					maxLength = receivedBlockchainLength
					maxPort = n_port
					maxIP = n_ip
					maxID = n_id

			if(maxLength == len(self.ourChain.blockList)):
				return "Tie, keep existing blockchain\n"
			# request max blockchain
			url = f'http://{maxIP}:{maxPort}/get_blockchain'
			response = requests.get(url)
			if response.status_code != 200:
				raise Exception('Invalid blockchain response')
			receivedBlocklist = response.json()['blockchain']
			valid, new_blockchain, new_utxos = self.isChainValid(receivedBlocklist)
			if not valid:
					raise Exception('received invalid chain')
			
			# Check if all transactions are valid 
			self.wallet.utxos = copy.deepcopy(new_utxos)
			self.wallet.utxos_snapshot = copy.deepcopy(new_utxos)
			self.ourChain.blockList = new_blockchain
			self.isReceivedValid()
			self.ourChain.printChain()
		except Exception as e:
			print(f'consensus.{n_id}: {e.__class__.__name__}: {e}')