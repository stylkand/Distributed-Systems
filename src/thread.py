# DISTRIBUTED SYSTEMS - NTUA ECE 2021 - 2022
# Stylianos Kandylakis
# Kitsos Orfanopoulos
# Christos Tsoufis

from time import sleep
from concurrent.futures import ThreadPoolExecutor


# pool of threads (use for mining, broadcast, etc)
class Thread:
	# default threads is 1, thus at first we start with 5 nodes, then with 10.
	def __init__(self, NUM_OF_THREADS = 1):
		self.executor = ThreadPoolExecutor(NUM_OF_THREADS)

	def submitTask(self, f, tmp, utxos):
		future = self.executor.submit(f, tmp, utxos)
		return future
