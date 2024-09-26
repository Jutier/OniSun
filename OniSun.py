from pykml import parser
from math import pi, atan
from matplotlib import pyplot as plt
import numpy as np


def parse(file):
	with open(file) as f:
		doc = parser.parse(f).getroot().Document

	def xy(S):
		x, y, _ = S.split(',')
		return (float(x), float(y))

	for pm in doc.iterchildren():
		if hasattr(pm, 'LineString'):
			return list(map(xy, str(pm.LineString.coordinates).split()))
	else:
		raise Exception("Couldn't find any coordinates on KML file.")


def arc(P1,P2):
	if P1[0] == P2[0]:
		A = pi/2
	else:
		A = atan((P1[1] - P2[1])/(P1[0] - P2[0]))

	if P1[0] < P2[0]:
		return A + pi
	elif not P1[1] < P2[1]:
		return A
	elif P1[0] == P2[0]:
		return -A
	else:
		return A + 2*pi


class Bus:
	def __init__(self, time, zone):
		self.head = (-46.624085, -23.502508)
		self.tail = 0
		self.time = time # Determines the aproximate Sun position
		self.zone = zone
		self.SunList = [0] # Determines wich side the Sun would be facing
		self.Right = 0 # Count how many points had the Sun on each side
		self.Left = 0

	@property
	def Sun(self): # Sun angle
		x = 180 - ((self.time - self.zone)/24)*360
		r = self.Angle - arc((x, 0), self.tail)
		return (r + 2*pi if r < 0 else r)
	@property
	def Angle(self): # Relative to equator
		return arc(self.head, self.tail)

	def move(self, pos):
		self.tail = self.head
		self.head = pos

	def checkSun(self, margin=0.1):
		if self.Sun > (margin) and self.Sun < (pi - margin): # Right
			self.SunList.append(1)
			self.Right += 1
		elif self.Sun > (pi + margin) and self.Sun < (2*pi - margin): # Left
			self.SunList.append(2)
			self.Left += 1
		else:
			self.SunList.append(0)
	
	def go(self, PATH, *margin):
		self.move(PATH[0])
		for P in PATH[1:]:
			self.move(P)
			self.checkSun(*margin)
		self.report(PATH)

	def report(self, PATH):
		plt.title(f'Left = {self.Left}/{len(self.SunList)}\nRight = {self.Right}/{len(self.SunList)}')
		colormap = np.array(['#646464', '#04ade0', '#d90021']) # Gray, Blue, Red
		plt.scatter(*zip(*PATH), c=colormap[self.SunList])

		sunX = (180 - ((self.time - self.zone)/24)*360)
		sunY = 0
		axis = plt.axis()
		# Makes the Sun sit in the corner if it's not in the viewport
		if sunX < axis[0]:
			sunX = axis[0]
		elif sunX > axis[1]:
			sunX = axis[1]
		if sunY < axis[2]:
			sunY = axis[2]
		elif sunY > axis[3]:
			sunY = axis[3]

		plt.scatter(sunX, sunY, color=colormap[2], label='Left') # Just points under the sun, used for the labels
		plt.scatter(sunX, sunY, color=colormap[1], label='Right')
		plt.scatter(sunX, sunY, s=1000, color='#fca800') # The Sun
		plt.axis(axis) # Set the axis back to before the Sun
		plt.legend()
		plt.show()


if __name__ == "__main__":
	B = Bus(8, -3)
	path = parse('Circle.kml')
	B.go(path)
