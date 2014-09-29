from __future__ import print_function
import numpy as np
import itertools
from channel import *
from math import copysign
from code import hamming_code
import gui

sign = lambda x: copysign(1,x)

#global variables
selected = None
input_string = ''
init_done = False
algorithm = 'Syndrome'
noise_power = 0
ch = None
modulated = np.array([])
noisy_signal = []
m = np.array([])
c = np.array([])
view = None
index = -1

def set_modulation(label):
	ch.modulation = label
	view.reset_indicators(label)
	if init_done:
		process_input()
		update()

def set_noise(val):
	global noise_power, noisy_signal
	noise_power = val
	noisy_signal = [ch.add_noise(modulated_sym,noise_power) for modulated_sym in modulated]
	update()

def set_ecc(val):
	global code
	code.algorithm = val

def set_code(val):
	global code, init_done, index, selected
	if val == "(5,2,3)":
		code.change(2)
	else:
		code.change(4)
	print('G:\n',code.G)
	print('H:\n',code.H)
	deselect_symbol(None)
	process_input()
	update()

def get_input(event):
	global input_string
	input_string = raw_input('Please enter a message to send over the channel\n>>')
	process_input()

def process_input():
	global input_string, m, c, modulated, noisy_signal, noise_power
	binary_string = ''
	for char in input_string:
		binary_string += (format(ord(char), '08b'))
	m = code.get_symbols(binary_string)
	c = code.encode(m)
	modulated = [ch.modulate(c_symbol) for c_symbol in c]
	noisy_signal = [ch.add_noise(modulated_sym,noise_power) for modulated_sym in modulated]

def calculate_colors():
	one = (1,0,0,1)
	two = (0,1,0,1)
	three = (1,0,1,1)
	four = (0,0,1,1)
	black = (0.5,0.5,0.5,0.1)
	colors = []
	for i,symbol in enumerate(modulated):
		if not (selected == None) and not (i == index):
			for e in symbol:
				colors.append(black)
		else:
			for e in symbol:
				if e.real >= 0 and e.imag >= 0:
					colors.append(one)
				elif e.real >= 0 and e.imag < 0:
					colors.append(two)
				elif e.real < 0 and e.imag < 0:
					colors.append(three)
				else:
					colors.append(four)
	return colors	

def update():
	global noise_power, noisy_signal, ch, init_done, view
	if init_done == True:
		xdata = [x.real for x in list(itertools.chain(*noisy_signal))]
		ydata = [y.imag for y in list(itertools.chain(*noisy_signal))]
		colors = calculate_colors()
		view.new_data(xdata, ydata, colors)
		if selected:
			print_selected()
	
def decode_symbol():
	dec = ch.hard_decode(noisy_signal[index])
	x = None
	if (selected == None):
		print('codeword:\t', c[index])
		print('Modulated:\t', modulated[index])
		print('Channel output:\t', noisy_signal[index])
	if code.algorithm == "Syndrome":
		print('Syndrome decoding...')
		print('Hard Decode:', dec)
		x = code.syndrome_decoding(dec, code.H)
	elif code.algorithm == "Chase":
		print('Chase 3 decoding...')
		print('Hard Decode:', dec)
		x = code.chase3_decoding(noisy_signal[index], dec ,code.H) 
	print('Result:', x)
	print('\n')
	return x

def select_symbol(event):
	global index, selected
	index += 1
	selected = modulated[index]
	if index >= len(c):
		index = -1
	update()

def print_selected():
	print('\nselected message:', m[index])
	print('codeword:\t', c[index])
	print('Modulated:\t', modulated[index])
	print('Channel output:\t', noisy_signal[index])
	print('\n')

def deselect_symbol(event):
	global selected, index
	index = -1
	selected = None
	update()

def decode_all():
	global index
	x = []
	for index in range(len(modulated)):
		x.append(decode_symbol())
	print('corrected codeword:\n', code.get_ascii(x))
	index = -1

def decode_now(event):
	if selected:
		decode_symbol()
	else:
		decode_all()

def custom_noise(event):
	global noisy_signal
	print('Current values: ', noisy_signal[index])
	input_string = raw_input('Enter soft values\n>>')
	input_list = input_string.split()
	if (len(input_list) == len(noisy_signal[index])):
		noisy_signal[index] = np.array([complex(a) for a in input_list])
		update()
	else:
		print('error: please give [', len(noisy_signal[index]), '] soft values')
		custom_noise(None)

def main():
	global ch, code, view, init_done
	ch = channel('BPSK')
	code = hamming_code(2, ch)
	get_input(None)
	view = gui.gui()
	view.add_radio_button([0.0, 0.0, 0.18, 0.15], ('BPSK', 'QPSK'), set_modulation)
	view.add_radio_button([0.0, 0.15, 0.18, 0.15], ('Syndrome', 'Chase'), set_ecc)
	view.add_radio_button([0.0, 0.30, 0.18, 0.15], ('(5,2,3)', '(7,4,3)'), set_code)
	view.add_button([0.0, 0.90, 0.18, 0.1], 'Decode', decode_now)
	view.add_button([0.0, 0.80, 0.18, 0.1], 'New Input', get_input)
	view.add_button([0.0, 0.70, 0.18, 0.1], 'Select Symbol', select_symbol)
	view.add_button([0.0, 0.60, 0.18, 0.1], 'Deselect Symbol', deselect_symbol)
	view.add_button([0.0, 0.50, 0.18, 0.1], 'Cust. Soft Values', custom_noise)
	view.add_slider([0.25, 0.05, 0.65, 0.08], 'Noise', (0, 3.0), set_noise)
	set_modulation('BPSK')
	init_done = True
	update()
	view.go()
	return
	
if __name__ == "__main__":
	main()

