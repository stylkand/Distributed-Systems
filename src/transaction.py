# DISTRIBUTED SYSTEMS - NTUA ECE 2021 - 2022
# Stylianos Kandylakis
# Kitsos Orfanopoulos
# Christos Tsoufis

from collections import OrderedDict
from Crypto.Hash import SHA384
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
import base64
import json

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


class Transaction:
	# 🟩🟩🟩 Constructor 🟩🟩🟩
    #  TRANSACTION STRUCT
	# -> senderPK,    senderID
	# -> receiverPK,  receiverID
	# -> amount
	# -> transaction_inputs
	# -> transaction_outputs
	# -> id
	# -> amount
    def __init__(self, sender, senderID, receiver, receiverID, amount, transaction_inputs, transaction_outputs = [], id = None, signature = None):
        self.sender = sender                                # public key 
        self.receiver = receiver                            # public key 
        self.senderID = senderID                           
        self.receiverID = receiverID
        self.amount = amount                                
        self.id = id                                       
        self.transaction_inputs = transaction_inputs        
        self.transaction_outputs = transaction_outputs      
        self.signature = signature


	# 🟨🟨 
    # If the has is the same then the two transactions are equal
    def __eq__(self, otherTransaction):    
        if not isinstance(otherTransaction, Transaction): # not same 
            return NotImplemented
        return self.id == otherTransaction.id

	# 🟨🟨🟨🟨
    # custom hash function for transaction, excluding outputs, signature
    def hash(self):
        transaction = OrderedDict([('sender', self.sender), ('receiver', self.receiver), ('amount', self.amount), ('transaction_inputs', self.transaction_inputs)])
        temp=json.dumps(transaction) 
        return SHA384.new(temp.encode())


	# 🟨🟨🟨🟨🟨🟨 
    # Auxiliary function to convert set to dictionary
    def to_dict(self):
        return OrderedDict([('sender', self.sender), ('receiver', self.receiver), ('amount', self.amount), ('transaction_inputs', self.transaction_inputs), ('transaction_outputs', self.transaction_outputs), ('id', self.id), ('signature', self.signature)])


	# 🟨🟨🟨🟨🟨🟨🟨🟨
    # creates signature of the transaction
    def signTransaction(self, senderPrivateKey):
        hashed = self.hash() 
        privateKey = RSA.importKey(senderPrivateKey) 
        signer = PKCS1_v1_5.new(privateKey)
        self.id = hashed.hexdigest() 
        self.signature = base64.b64encode(signer.sign(hashed)).decode()
        return self.signature

	# 🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨 
    def verify_signature(self):
        # Check if public key is true: can it decode something encoded with private key?
        RSAkey = RSA.importKey(self.sender.encode()) #sender public key
        verifier = PKCS1_v1_5.new(RSAkey) 
        hashed = self.hash()
        return verifier.verify(hashed, base64.b64decode(self.signature)) 