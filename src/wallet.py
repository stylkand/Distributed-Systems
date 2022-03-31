# DISTRIBUTED SYSTEMS - NTUA ECE 2021 - 2022
# Stylianos Kandylakis
# Kitsos Orfanopoulos
# Christos Tsoufis

# import binascii
# import Crypto
# import hashlib
# import json
# import Crypto.Random
# from Crypto.Hash import SHA
# from Crypto.Signature import PKCS1_v1_5
# from time import time
# from urllib.parse import urlparse
# from uuid import uuid4



from Crypto.PublicKey import RSA


# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@



class Wallet:

	# 🟩🟩🟩 Constructor 🟩🟩🟩
	#  WALLET STRUCT
	# -> public/private key
	# -> UTXOs
	# -> UTXOs snapshot (current image of UTXOs of others, to check them)
	def __init__(self, utxos={}):
		# our wallet must be encrypted thus public/private keys
		rsa_key = RSA.generate(1024)
		self.privateKey = rsa_key.exportKey('PEM').decode()
		self.publicKey = rsa_key.publickey().exportKey('PEM').decode()
		self.utxos = utxos 			# set with key->public key, value->{id, to_who, amount}
		self.utxos_snapshot = {} 	# set of UTXOs of others


	# 🟦🟦🟦 Balance 🟦🟦🟦
	# Calculate NBCs of our wallet 
	def balance(self):
		temp=self.publicKey
		totalNBC=0
		for i in self.utxos[temp]:
			totalNBC=totalNBC+i['amount']
		return totalNBC
