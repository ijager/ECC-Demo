from __future__ import print_function
import numpy as np
import channel 

G2 = np.array([[1,0,1,0,1],[0,1,0,1,1]])
G4 = np.array([[1,0,0,0,1,1,1],[0,1,0,0,1,1,0],[0,0,1,0,1,0,1],[0,0,0,1,0,1,1]])

class hamming_code(object):

	def __init__(self, k, ch):
		self.ch = ch
		self.k = None
		self.G = None 
		self.d = None
		self.H = None
		self.algorithm = 'Syndrome'
		self.change(k)

	def change(self, k):
		self.k = k
		self.d = 3
		if k == 2:
			self.G = G2
			self.n = 5
		else:
			self.G = G4
			self.n = 7
		self.calc_H()


	def calc_H(self):
		shape = self.G.shape
		I = np.eye(shape[1]-shape[0])
		P = self.G[:,shape[0]:]
		self.H = np.hstack((P.T, I))

	def get_ascii(self, c):
		m = ""
		w = np.hstack([codeword[:self.k] for codeword in c])
		for i in range(0, len(w), 8):
			    m += chr(np.packbits(w[i:i+8]))
		return m

	def get_symbols(self, m):
		symbols = []
		for i in range(0,len(m),self.k):
			t = m[i:i+self.k]
			symbols.append([int(bit) for bit in t])
		return np.array(symbols)

	def encode(self, m):
		return [np.mod(np.dot(symbol, self.G),2) for symbol in m]

	def euclidean_dist(self, a,b):
		return np.linalg.norm(a-b)

	def invert_bit(self, x, n):
		y = np.copy(x)
		if y[n] == 1:
			y[n] = 0
		else:
			y[n] = 1
		return y

	def chase3_decoding(self, noisy_signal, y, H):
		#first trial
		x1 = self.syndrome_decoding(y, H, prnt=False)
		print('Trial 1: decode',y, '->',x1 )
		n1 = np.argmin(np.absolute(noisy_signal))
		n2 = np.argmin(np.absolute(np.delete(noisy_signal,n1)))
		if n2 >= n1:
			n2 += 1
		print('Flip weakest bits:', n1, n2 )
		#invert weakest bits
		y = self.invert_bit(y,n1)
		y = self.invert_bit(y,n2)
		x2 = self.syndrome_decoding(y, H, prnt=False)
		print('Trial 2: decode',y, '->',x2 )
		ch_x1 = self.ch.modulate(x1)
		ch_x2 = self.ch.modulate(x2)
		d1 = self.euclidean_dist(ch_x1, noisy_signal)
		d2 = self.euclidean_dist(ch_x2, noisy_signal)
		print('Euclidean dist 1:',d1)
		print('Euclidean dist 2:',d2)
		if d1 < d2:
			return x1
		else:
			return x2

	def syndrome_decoding(self, x, H, prnt=True):
		y = np.copy(x)
		#calculate syndrome
		syn = np.mod(np.dot(y, H.T),2)
		if syn.any():
			#look for column Kj in H which equals syn.T
			shape = H.shape
			for index, row in enumerate(H.T):
				if np.all(syn == row):
					break
			y = self.invert_bit(y, index)
			if prnt:
				print('flip bit', index)
		return y


