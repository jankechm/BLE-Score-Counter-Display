# Author: Marek Jankech

from app.char import Char
from app.line import VerticalLine, HorizontalLine

class BigDigit:
	def __init__(self):
		"""
		Represents a font of digits 0-9 which take
		8 points by width and 16 points by height.
		"""
		self.digits = [	
			# [0]
			Char(
				hlines = [
					HorizontalLine(1,0,6),
					HorizontalLine(0,1,8),
					HorizontalLine(0,14,8),
					HorizontalLine(1,15,6)
				],
				vlines = [
					VerticalLine(0,1,14),
					VerticalLine(1,0,16),
					VerticalLine(6,0,16),
					VerticalLine(7,1,14)
				]
			),

			# [1]
			Char(
				hlines = [],
				vlines = [
					VerticalLine(0,0,16),
					VerticalLine(1,0,16)
				]
			),

			# [2]
			Char(
				hlines = [
					HorizontalLine(0,0,8),
					HorizontalLine(0,1,8),
					HorizontalLine(0,7,8),
					HorizontalLine(0,8,8),
					HorizontalLine(0,14,8),
					HorizontalLine(0,15,8)
				],
				vlines = [
					VerticalLine(6,0,8),
					VerticalLine(7,0,8),
					VerticalLine(0,8,8),
					VerticalLine(1,8,8)
				]
			),

			# [3]
			Char(
				hlines = [
					HorizontalLine(0,0,8),
					HorizontalLine(0,1,8),
					HorizontalLine(0,7,8),
					HorizontalLine(0,8,8),
					HorizontalLine(0,14,8),
					HorizontalLine(0,15,8)
				],
				vlines = [
					VerticalLine(6,0,16),
					VerticalLine(7,0,16)
				]
			),

			# [4]
			Char(
				hlines = [
					HorizontalLine(0,7,8),
					HorizontalLine(0,8,8)
				],
				vlines = [
					VerticalLine(0,0,8),
					VerticalLine(1,0,8),
					VerticalLine(6,0,16),
					VerticalLine(7,0,16)
				]
			),

			# [5]
			Char(
				hlines = [
					HorizontalLine(0,0,8),
					HorizontalLine(0,1,8),
					HorizontalLine(0,7,8),
					HorizontalLine(0,8,8),
					HorizontalLine(0,14,8),
					HorizontalLine(0,15,8)
				],
				vlines = [
					VerticalLine(0,0,8),
					VerticalLine(1,0,8),
					VerticalLine(6,8,8),
					VerticalLine(7,8,8)
				]
			),

			# [6]
			Char(
				hlines = [
					HorizontalLine(0,0,8),
					HorizontalLine(0,1,8),
					HorizontalLine(0,7,8),
					HorizontalLine(0,8,8),
					HorizontalLine(0,14,8),
					HorizontalLine(0,15,8)
				],
				vlines = [
					VerticalLine(0,0,16),
					VerticalLine(1,0,16),
					VerticalLine(6,8,8),
					VerticalLine(7,8,8)
				]
			),

			# [7]
			Char(
				hlines = [
					HorizontalLine(0,0,8),
					HorizontalLine(0,1,8)
				],
				vlines = [
					VerticalLine(6,0,16),
					VerticalLine(7,0,16)
				]
			),

			# [8]
			Char(
				hlines = [
					HorizontalLine(0,0,8),
					HorizontalLine(0,1,8),
					HorizontalLine(0,7,8),
					HorizontalLine(0,8,8),
					HorizontalLine(0,14,8),
					HorizontalLine(0,15,8)
				],
				vlines = [
					VerticalLine(0,0,16),
					VerticalLine(1,0,16),
					VerticalLine(6,0,16),
					VerticalLine(7,0,16)
				]
			),

			# [9]
			Char(
				hlines = [
					HorizontalLine(0,0,8),
					HorizontalLine(0,1,8),
					HorizontalLine(0,7,8),
					HorizontalLine(0,8,8),
					HorizontalLine(0,14,8),
					HorizontalLine(0,15,8)
				],
				vlines = [
					VerticalLine(0,0,8),
					VerticalLine(1,0,8),
					VerticalLine(6,0,16),
					VerticalLine(7,0,16)
				]
			)
		]

	def get(self, idx: int):
		# Copy Char for further modifications
		return self.digits[idx].deepcopy()


class MediumDigit:
	def __init__(self):
		"""
		Represents a font of digits 0-9 which take
		6 points by width and 14 points by height.
		"""
		self.digits = [	
			# [0]
			Char(
				hlines = [
					HorizontalLine(1,1,4),
					HorizontalLine(0,2,6),
					HorizontalLine(0,13,6),
					HorizontalLine(1,14,4)
				],
				vlines = [
					VerticalLine(0,2,12),
					VerticalLine(1,1,14),
					VerticalLine(4,1,14),
					VerticalLine(5,2,12)
				]
			),

			# [1]
			Char(
				hlines = [],
				vlines = [
					VerticalLine(0,1,14),
					VerticalLine(1,1,14)
				]
			),

			# [2]
			Char(
				hlines = [
					HorizontalLine(0,1,6),
					HorizontalLine(0,2,6),
					HorizontalLine(0,7,6),
					HorizontalLine(0,8,6),
					HorizontalLine(0,13,6),
					HorizontalLine(0,14,6)
				],
				vlines = [
					VerticalLine(4,1,7),
					VerticalLine(5,1,7),
					VerticalLine(0,8,7),
					VerticalLine(1,8,7)
				]
			),

			# [3]
			Char(
				hlines = [
					HorizontalLine(0,1,6),
					HorizontalLine(0,2,6),
					HorizontalLine(0,7,6),
					HorizontalLine(0,8,6),
					HorizontalLine(0,13,6),
					HorizontalLine(0,14,6)
				],
				vlines = [
					VerticalLine(4,1,14),
					VerticalLine(5,1,14)
				]
			),

			# [4]
			Char(
				hlines = [
					HorizontalLine(0,7,6),
					HorizontalLine(0,8,6)
				],
				vlines = [
					VerticalLine(0,1,7),
					VerticalLine(1,1,7),
					VerticalLine(4,1,14),
					VerticalLine(5,1,14)
				]
			),

			# [5]
			Char(
				hlines = [
					HorizontalLine(0,1,6),
					HorizontalLine(0,2,6),
					HorizontalLine(0,7,6),
					HorizontalLine(0,8,6),
					HorizontalLine(0,13,6),
					HorizontalLine(0,14,6)
				],
				vlines = [
					VerticalLine(0,1,8),
					VerticalLine(1,1,8),
					VerticalLine(4,8,7),
					VerticalLine(5,8,7)
				]
			),

			# [6]
			Char(
				hlines = [
					HorizontalLine(0,1,6),
					HorizontalLine(0,2,6),
					HorizontalLine(0,7,6),
					HorizontalLine(0,8,6),
					HorizontalLine(0,13,6),
					HorizontalLine(0,14,6)
				],
				vlines = [
					VerticalLine(0,1,14),
					VerticalLine(1,1,14),
					VerticalLine(4,8,7),
					VerticalLine(5,8,7)
				]
			),

			# [7]
			Char(
				hlines = [
					HorizontalLine(0,1,6),
					HorizontalLine(0,2,6)
				],
				vlines = [
					VerticalLine(4,1,14),
					VerticalLine(5,1,14)
				]
			),

			# [8]
			Char(
				hlines = [
					HorizontalLine(0,1,6),
					HorizontalLine(0,2,6),
					HorizontalLine(0,7,6),
					HorizontalLine(0,8,6),
					HorizontalLine(0,13,6),
					HorizontalLine(0,14,6)
				],
				vlines = [
					VerticalLine(0,1,14),
					VerticalLine(1,1,14),
					VerticalLine(4,1,14),
					VerticalLine(5,1,14)
				]
			),

			# [9]
			Char(
				hlines = [
					HorizontalLine(0,1,6),
					HorizontalLine(0,2,6),
					HorizontalLine(0,7,6),
					HorizontalLine(0,8,6),
					HorizontalLine(0,13,6),
					HorizontalLine(0,14,6)
				],
				vlines = [
					VerticalLine(0,1,7),
					VerticalLine(1,1,7),
					VerticalLine(4,1,14),
					VerticalLine(5,1,14)
				]
			)
		]

	def get(self, idx: int):
		# Copy Char for further modifications
		return self.digits[idx].deepcopy()

class Medium:
	def __init__(self):
		"""
		Represents a font of alphanumeric characters, which take
		6 points by width and 14 points by height.
		"""
		self.chars = {
			"0": Char(
				hlines = [
					HorizontalLine(1,1,4),
					HorizontalLine(0,2,6),
					HorizontalLine(0,13,6),
					HorizontalLine(1,14,4)
				],
				vlines = [
					VerticalLine(0,2,12),
					VerticalLine(1,1,14),
					VerticalLine(4,1,14),
					VerticalLine(5,2,12)
				]
			),
			"1": Char(
				hlines = [],
				vlines = [
					VerticalLine(3,1,14),
					VerticalLine(4,1,14)
				]
			),
			"2": Char(
				hlines = [
					HorizontalLine(0,1,6),
					HorizontalLine(0,2,6),
					HorizontalLine(0,7,6),
					HorizontalLine(0,8,6),
					HorizontalLine(0,13,6),
					HorizontalLine(0,14,6)
				],
				vlines = [
					VerticalLine(4,1,7),
					VerticalLine(5,1,7),
					VerticalLine(0,8,7),
					VerticalLine(1,8,7)
				]
			),
			"3": Char(
				hlines = [
					HorizontalLine(0,1,6),
					HorizontalLine(0,2,6),
					HorizontalLine(0,7,6),
					HorizontalLine(0,8,6),
					HorizontalLine(0,13,6),
					HorizontalLine(0,14,6)
				],
				vlines = [
					VerticalLine(4,1,14),
					VerticalLine(5,1,14)
				]
			),
			"4": Char(
				hlines = [
					HorizontalLine(0,7,6),
					HorizontalLine(0,8,6)
				],
				vlines = [
					VerticalLine(0,1,7),
					VerticalLine(1,1,7),
					VerticalLine(4,1,14),
					VerticalLine(5,1,14)
				]
			),
			"5": Char(
				hlines = [
					HorizontalLine(0,1,6),
					HorizontalLine(0,2,6),
					HorizontalLine(0,7,6),
					HorizontalLine(0,8,6),
					HorizontalLine(0,13,6),
					HorizontalLine(0,14,6)
				],
				vlines = [
					VerticalLine(0,1,8),
					VerticalLine(1,1,8),
					VerticalLine(4,8,7),
					VerticalLine(5,8,7)
				]
			),
			"6": Char(
				hlines = [
					HorizontalLine(0,1,6),
					HorizontalLine(0,2,6),
					HorizontalLine(0,7,6),
					HorizontalLine(0,8,6),
					HorizontalLine(0,13,6),
					HorizontalLine(0,14,6)
				],
				vlines = [
					VerticalLine(0,1,14),
					VerticalLine(1,1,14),
					VerticalLine(4,8,7),
					VerticalLine(5,8,7)
				]
			),
			"7": Char(
				hlines = [
					HorizontalLine(0,1,6),
					HorizontalLine(0,2,6)
				],
				vlines = [
					VerticalLine(4,1,14),
					VerticalLine(5,1,14)
				]
			),
			"8": Char(
				hlines = [
					HorizontalLine(0,1,6),
					HorizontalLine(0,2,6),
					HorizontalLine(0,7,6),
					HorizontalLine(0,8,6),
					HorizontalLine(0,13,6),
					HorizontalLine(0,14,6)
				],
				vlines = [
					VerticalLine(0,1,14),
					VerticalLine(1,1,14),
					VerticalLine(4,1,14),
					VerticalLine(5,1,14)
				]
			),
			"9": Char(
				hlines = [
					HorizontalLine(0,1,6),
					HorizontalLine(0,2,6),
					HorizontalLine(0,7,6),
					HorizontalLine(0,8,6),
					HorizontalLine(0,13,6),
					HorizontalLine(0,14,6)
				],
				vlines = [
					VerticalLine(0,1,7),
					VerticalLine(1,1,7),
					VerticalLine(4,1,14),
					VerticalLine(5,1,14)
				]
			),
			"°": Char(
				hlines = [
					HorizontalLine(4,1,3),
					HorizontalLine(4,3,3)
				],
				vlines = [
					VerticalLine(4,1,3),
					VerticalLine(6,1,3)
				]
			),
			"A": Char(
				hlines = [
					HorizontalLine(2,1,4),
					HorizontalLine(1,2,6),
					HorizontalLine(1,7,6),
					HorizontalLine(1,8,6),
				],
				vlines = [
					VerticalLine(1,2,13),
					VerticalLine(2,1,14),
					VerticalLine(5,1,14),
					VerticalLine(6,2,13)
				]
			),
			"C": Char(
				hlines = [
					HorizontalLine(2,1,4),
					HorizontalLine(1,2,6),
					HorizontalLine(1,13,6),
					HorizontalLine(2,14,4),
				],
				vlines = [
					VerticalLine(1,2,12),
					VerticalLine(2,1,14)
				]
			),
			"J": Char(
				hlines = [
					HorizontalLine(1,13,6),
					HorizontalLine(1,14,4)
				],
				vlines = [
					VerticalLine(5,1,14),
					VerticalLine(6,1,13)
				]
			),
			"S": Char(
				hlines = [
					HorizontalLine(2,1,4),
					HorizontalLine(1,2,6),
					HorizontalLine(1,7,5),
					HorizontalLine(2,8,5),
					HorizontalLine(1,13,6),
					HorizontalLine(2,14,4)
				],
				vlines = [
					VerticalLine(1,2,6),
					VerticalLine(2,1,8),
					VerticalLine(5,7,8),
					VerticalLine(6,8,6)
				]
			)
		}

	def get(self, char):
		# Copy Char for further modifications
		return self.chars[char].deepcopy()