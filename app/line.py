# Author: Marek Jankech

class HorizontalLine:
	def __init__(self, start_x: int, start_y: int, width: int):
		"""
		Represents a horizontal line on a matrix defined
		by starting coordinate [x,y] and width.
		Width is expanding to the right.
		"""

		self.x = start_x
		self.y = start_y
		self.width = width

	def copy(self):
		return HorizontalLine(self.x, self.y, self.width)

	def x_shift(self, x_offset: int):
		self.x += x_offset

	def render(self, framebuf):
		framebuf.hline(self.x, self.y, self.width, 1)


class VerticalLine:
	def __init__(self, start_x: int, start_y: int, height: int):
		"""
		Represents a vertical line on a matrix defined
		by starting coordinate [x,y] and height.
		Height is expanding to the bottom.
		"""

		self.x = start_x
		self.y = start_y
		self.height = height

	def copy(self):
		return VerticalLine(self.x, self.y, self.height)

	def x_shift(self, x_offset: int):
		self.x += x_offset

	def render(self, framebuf):
		framebuf.vline(self.x, self.y, self.height, 1)
