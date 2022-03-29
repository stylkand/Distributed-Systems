# DISTRIBUTED SYSTEMS - NTUA ECE 2021 - 2022
# Stylianos Kandylakis
# Kitsos Orfanopoulos
# Christos Tsoufis

# --------------Prerequisites-----------------
# pip install -r requirements.txt


# --------------Terminal scripts--------------
#export FLASK_APP=api.py		for windows set FLASK_APP=api.py
#export FLASK_ENV=development       !!FOR DEBUG MODE!!
#flask run -h localhost -p 8765 --cert=adhoc
#set FLASK_DEBUG=1

# --------------Online Tutorials--------------
# https://medium.com/@karthikeyan.ranasthala/build-a-jwt-based-authentication-rest-api-with-flask-and-mysql-5dc6d3d1cb82


import datetime;
from collections import OrderedDict
from Crypto.Hash import SHA256
import json

class Block:
	# 🟩🟩🟩
	# create a BLOCK struct
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
		print('Nonce: \t\t' + str(self.nonce))
		print('Transactions: \t')
		for t in self.listOfTransactions:
			print('\t\tSender ID: ' + str(t.senderID) + ' \t\tReceiver ID: '+ str(t.receiverID) + ' \t\tAmount: '+ str(t.amount)+'nc')
			print('\t\Hash: ' + str(t.id))
		print('Current hash: \t\t' + str(self.hash))
		print('Previous Hash: \t' + str(self.previousHash))
