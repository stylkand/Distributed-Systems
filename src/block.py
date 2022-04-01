# DISTRIBUTED SYSTEMS - NTUA ECE 2021 - 2022
# Stylianos Kandylakis
# Kitsos Orfanopoulos
# Christos Tsoufis



import datetime;
from collections import OrderedDict
from Crypto.Hash import SHA256
import json

class Block:
	# 🟩🟩🟩
	#  BLOCK STRUCT
	# -> index
	# -> timestamp
	# -> transactions list
	# -> nonce
	# -> current_hash
	# -> previous_hash
	def __init__(self, index = -1, previousHash = None):
		self.index = index
		self.previousHash = previousHash
		self.timestamp = datetime.datetime.now().timestamp()
		self.nonce = 0
		self.listOfTransactions=[]
		self.hash = None


	# 🟩🟩🟩🟩
	# auxiliary functin to crete dictionary (set) from a list
	def listToSerialisable(self):
		final = []
		for trans in self.listOfTransactions:
			final.append(trans.__dict__)
		return final


	# 🟩🟩🟩🟩🟩
	def myHash(self):
		# we add all the data of the block to an ordered dictionary
		dictData = OrderedDict([('index',self.index),('prev',self.previousHash),('tmsp',self.timestamp), ('nonce',self.nonce),('transactions',self.listToSerialisable())])
		temp = json.dumps(dictData) # create JSON (needed to hash)
		return SHA256.new(temp.encode()).hexdigest()


	# 🟩🟩🟩🟩🟩🟩
	def printBlock(self):
		print('\n__Block no:' + str(self.index) + '__')
		print('Timestamp: \t' + str(self.timestamp))
		print('Nonce: \t' + str(self.nonce))
		print('Transactions: \t')
		for t in self.listOfTransactions:
			print('\t\tSender ID: ' + str(t.senderID) + ' \t\tReceiver ID: '+ str(t.receiverID) + ' \t\tAmount: '+ str(t.amount)+'NBCs')
			print('\t\Hash: ' + str(t.id))
		print('Current hash: \t\t' + str(self.hash))
		print('Previous Hash: \t' + str(self.previousHash))
