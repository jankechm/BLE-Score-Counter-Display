# Author: Marek Jankech

from app.line import HorizontalLine, VerticalLine

class Char:
	def __init__(self, hlines: list[HorizontalLine], vlines: list[VerticalLine]):
		"""
		Represents a digit defined by horizontal and vertical lines
		spreading out on top matrix and bottom matrix (2 framebuffers).
		"""

		self.hlines = hlines
		self.vlines = vlines

	def x_shift(self, x_offset: int):
		for line in self.hlines:
			line.x_shift(x_offset)

		for line in self.vlines:
			line.x_shift(x_offset)
		
	def deepcopy(self):
		hlines = []
		vlines = []

		for line in self.hlines:
			hlines.append(line.copy())

		for line in self.vlines:
			vlines.append(line.copy())

		return Char(hlines, vlines)

	def render(self, framebuf):
		for line in self.hlines:
			line.render(framebuf)

		for line in self.vlines:
			line.render(framebuf)
			