import matplotlib.pyplot as plt
from misc import center_spines
import matplotlib
from matplotlib.widgets import Slider, Button, RadioButtons
from matplotlib import collections as mc
import numpy as np

class gui(object):


	def new_data(self, x, y, c):
		self.scatter.set_offsets([(xx,yy) for xx,yy in zip(x,y)])
		self.scatter.set_color(c)
		m = 0.5
		maxX = m + max([np.max(x), np.absolute(np.min(x)), 2])
		maxY = m + max([np.max(y), np.absolute(np.min(y)), 2])
		self.ax.axis([-maxX, maxX, -maxY, maxY])
		self.fig.canvas.draw()


	def go_now(self, event):
		x = 4*np.random.randn(10)
		self.ax.lines[0].set_ydata(x)
		self.ax.axis([-10, 10, -10, 10])
		self.fig.canvas.draw()

	def reset_indicators(self, name):
		self.remove_indicators()
		length = 0.2
		l = []
		colors = []
		if name == "QPSK":
			loc = np.sqrt(2)/2
			l.append((loc,loc))
			l.append((loc,-loc))
			l.append((-loc,-loc))
			l.append((-loc,loc))
			colors = [(1,0,0,1), (0,1,0,1), (1,0,1,1), (0,0,1,1)]
		elif name == "BPSK":
			l = [(-1,0), (1,0)]
			colors = [(0,0,1,1), (1,0,0,1)]
			length = 0.5
		self.add_indicators(l, colors = colors, length = length)

	def remove_indicators(self):
		for c in self.ax.collections[:]:
			if type(c) == matplotlib.collections.LineCollection:
				self.ax.collections.remove(c)

	def add_indicators(self, locations, colors=(0,0,0,1), length=0.2):
		for l, c in zip(locations, colors):
			self.add_cross(l, length, c)

	def add_cross(self, origin, length, color):
		lines = [[(origin[0] - length/2, origin[1]), (origin[0] + length/2, origin[1])], [(origin[0], origin[1] - length/2), (origin[0], origin[1] + length/2)]]
		lc = mc.LineCollection(lines, colors=color, linewidths=3)
		self.ax.add_collection(lc)

	def add_slider(self, coords, label, slider_range, cb):
		axes = plt.axes(coords)
		slider = Slider(axes, label, slider_range[0], slider_range[1], valinit=0)
		slider.on_changed(cb)
		self.sliders.append(slider)

	def add_radio_button(self, coords, labels, cb):
		axes = plt.axes(coords)
		radio = RadioButtons(axes, labels)
		radio.on_clicked(cb)
		self.radio_buttons.append(radio)
	
	def add_button(self, coords, label, cb):
		axes = self.fig.add_axes(coords)
		button = Button(axes, label)
		button.on_clicked(cb)
		self.buttons.append(button)

	def go(self):
		plt.show()

	def __init__(self):
		self.buttons = []
		self.radio_buttons = []
		self.sliders = []
		self.fig = plt.figure()
		self.ax = plt.axes([0.2,0.2,0.8,0.8])
		

		self.ax.axis([-3, 3, -3, 3])
		center_spines(ax=self.ax)
		self.scatter = self.ax.scatter(0,0,marker='o', s = 75)



