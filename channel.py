from numpy import random
from cmath import phase
import numpy as np

class channel:
	def __init__(self, modulation):
		self.modulation = modulation
		self.code_word_length = 0
		self.noise = None

	def modulate(self, m):
		modulated = []
		self.code_word_length = len(m)
		if self.modulation == 'BPSK':
			modulated = [1 if x==0 else -1 for x in m]
		elif self.modulation == 'QPSK':
			if (np.mod(len(m),2)):
				m = [0] + list(m)
			for msb, lsb in zip(m[0::2], m[1::2]):
				modulated.append(-1.0/np.sqrt(2) * (1+1j) + 2.0/np.sqrt(2) * (msb+(lsb)*1j))
		return modulated

	def hard_decode(self,c):
		decoded = []
		if self.modulation == 'BPSK':
			decoded = [1 if x < 0 else 0 for x in c]
		elif self.modulation == 'QPSK':
			for s in c:
				theta = phase(s)
				if theta >= 0 and theta < np.pi/2:
					decoded += [1,1]
				elif theta >= np.pi/2 and theta <= np.pi:
					decoded += [0,1]
				elif theta >= -np.pi and theta <= -np.pi/2:
					decoded += [0,0]
				else:
					decoded += [1,0]
			decoded = decoded[-self.code_word_length:]

		return np.array(decoded)

	def generate_noise(self, noise_power):
		if self.modulation == 'BPSK':
			self.noise = noise_power*np.random.randn(len(signal))
		elif self.modulation == 'QPSK':
			self.noise = noise_power/np.sqrt(2) * np.random.randn(len(signal)) + noise_power/np.sqrt(2) * np.random.randn(len(signal)) * 1j

	def add_noise(self, signal, noise_power):
		if self.modulation == 'BPSK':
			return signal + noise_power*np.random.randn(len(signal))
		elif self.modulation == 'QPSK':
			return signal + noise_power/np.sqrt(2) * np.random.randn(len(signal)) + noise_power/np.sqrt(2) * np.random.randn(len(signal)) * 1j


