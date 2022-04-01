# DISTRIBUTED SYSTEMS - NTUA ECE 2021 - 2022
# Stylianos Kandylakis
# Kitsos Orfanopoulos
# Christos Tsoufis

import block

class Blockchain:

	# 🟩🟩🟩 
	def __init__(self):
		self.blockList = [] # blockchain, a list of blocks
	

	# 🟩🟩🟩🟩
	def createBlockchain(self, initialTransactions):
		# first we create the first block 
		bootstrap = block.Block(index = 0, previousHash = 1)
		# we add the initialTransactions to this block and we found its hash
		bootstrap.listOfTransactions.append(initialTransactions)
		bootstrap.hash = bootstrap.myHash()
		# note that for bootstrap we don't have to check the block (its previous hash etc)
		self.addBlock(bootstrap) #



	# 🟩🟩🟩🟩🟩
	# adds a block to the blockchain
	def addBlock(self, newBlock):
		self.blockList.append(newBlock)
		print('Current blockchain lenght: \t' + str(len(self.blockList)))
		print('The blocks are: \t' + str(len(self.blockList)))
		self.printChain()


	# 🟩🟩🟩🟩🟩🟩
	# calls printBlock for every block in the blockchain
	def printChain(self):
		print("\n ------------------\n")
		for block in self.blockList:
			block.printBlock()

