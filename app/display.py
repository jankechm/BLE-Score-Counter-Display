# Author: Marek Jankech

from machine import Pin, SPI
from utime import sleep_ms

import app.constants as const

import framebuf

class Matrix:
	WIDTH = const.MATRIXES_IN_ROW * const.COLS_IN_MATRIX
	HEIGHT = const.MATRIXES_IN_COL * const.ROWS_IN_MATRIX
	HALF_WIDTH = WIDTH // 2
	HALF_HEIGHT = const.ROWS_IN_MATRIX
	BOTTOM_HALF_OFFSET = const.MATRIXES_IN_ROW * const.ROWS_IN_MATRIX

	def __init__(self, spi: SPI, cs_pin: Pin, bright_lvl):
		"""
		Provides operations for showing patterns on the matrix display.
		"""
		self.spi = spi
		self.cs_pin = cs_pin

		self.buffer = bytearray(
			const.ROWS_IN_MATRIX * const.MATRIXES_IN_ROW * const.MATRIXES_IN_COL)

		self.fb = framebuf.FrameBuffer(self.buffer, 
			const.COLS_IN_MATRIX * const.MATRIXES_IN_ROW,
			const.ROWS_IN_MATRIX * const.MATRIXES_IN_COL, framebuf.MONO_HLSB)

		# Framebuffer methods
		self.fill = self.fb.fill
		self.fill_rect = self.fb.fill_rect
		self.hline = self.fb.hline
		self.vline = self.fb.vline
		self.pixel = self.fb.pixel
		self.text = self.fb.text

		self.init_display(bright_lvl)

	def init_display(self, bright_lvl: int):
		self._write(const.SHUTDOWN, const.SHUTDOWN_MODE_ON)

		self._write(const.DISPLAYTEST, const.DISPLAYTEST_TEST_OFF)

		self._write(const.SCANLIMIT, const.SCANLIMIT_8_DIGITS)
		self._write(const.DECODEMODE, const.NO_BCD_DECODE)
		self._write(const.INTENSITY, bright_lvl)

		self._write(const.SHUTDOWN, const.SHUTDOWN_MODE_OFF)

	def reinit_display(self, bright_lvl: int):
		self._write(const.SHUTDOWN, const.SHUTDOWN_MODE_ON)

		self._write(const.SCANLIMIT, const.SCANLIMIT_8_DIGITS)
		self._write(const.DECODEMODE, const.NO_BCD_DECODE)
		self._write(const.INTENSITY, bright_lvl)

		self._write(const.SHUTDOWN, const.SHUTDOWN_MODE_OFF)

		# Signalize display re-init by horzizontal line in the middle.
		self.fb.fill(0)
		self.fb.fill_rect(0, Matrix.HALF_HEIGHT - 1, Matrix.WIDTH, 2, 1)
		self.redraw_twice()
		sleep_ms(300)

	def turn_off(self):
		self._write(const.SHUTDOWN, const.SHUTDOWN_MODE_ON)

	def turn_on(self):
		self._write(const.SHUTDOWN, const.SHUTDOWN_MODE_OFF)

	def display_test(self, is_on: bool):
		self._write(const.DISPLAYTEST, 
			  const.DISPLAY_TEST_ON if is_on else const.DISPLAYTEST_TEST_OFF)

	def set_brightness(self, val):
		self._write(const.INTENSITY, val)

	def redraw_twice(self):
		"""Some LEDs need to tell it twice to understand..."""

		self.redraw()
		self.redraw()

	def redraw(self):
		"""Translate contents of the buffer to the LED matrix."""

		for row_idx in range(const.ROWS_IN_MATRIX):
			self.cs_pin.value(0)

			# First half of the buffer
			for matrix_idx in range(const.MATRIXES_IN_ROW):
				self.spi.write(bytearray([const.ROW0 + row_idx, 
					self.buffer[(row_idx * const.MATRIXES_IN_ROW) + matrix_idx]]))

			# Second half of the buffer
			for matrix_idx in range(const.MATRIXES_IN_ROW):
				self.spi.write(bytearray([const.ROW0 + row_idx, 
					self.buffer[(row_idx * const.MATRIXES_IN_ROW) + matrix_idx
					+ Matrix.BOTTOM_HALF_OFFSET]]))

			self.cs_pin.value(1)

	def clear_half(self, side):
		if side == const.LEFT:
			self.fb.fill_rect(0, 0, Matrix.HALF_WIDTH - 1, Matrix.HEIGHT, 0)
		elif side == const.RIGHT:
			self.fb.fill_rect(Matrix.HALF_WIDTH + 1, 0, Matrix.HALF_WIDTH - 1,
				Matrix.HEIGHT, 0)
		else:
			# both
			self.fb.fill_rect(0, 0, Matrix.HALF_WIDTH - 1, Matrix.HEIGHT, 0)
			self.fb.fill_rect(Matrix.HALF_WIDTH + 1, 0, Matrix.HALF_WIDTH - 1,
				Matrix.HEIGHT, 0)

		self.redraw_twice()

	def clear_quarter(self, quarter):
		if quarter == const.TOP_LEFT:
			self.fb.fill_rect(0, 0, Matrix.HALF_WIDTH, Matrix.HALF_HEIGHT, 0)
		elif quarter == const.TOP_RIGHT:
			self.fb.fill_rect(Matrix.HALF_WIDTH, 0, Matrix.HALF_WIDTH,
				Matrix.HALF_HEIGHT, 0)
		elif quarter == const.BOTTOM_LEFT:
			self.fb.fill_rect(0, Matrix.HALF_HEIGHT, Matrix.HALF_WIDTH,
				Matrix.HALF_HEIGHT, 0)
		else:
			self.fb.fill_rect(Matrix.HALF_WIDTH, Matrix.HALF_HEIGHT,
				Matrix.HALF_WIDTH, Matrix.HALF_HEIGHT, 0)

		self.redraw_twice()

	def clear_matrix_row(self, row):
		if row == const.TOP_ROW:
			self.fb.fill_rect(0, 0, Matrix.WIDTH, Matrix.HALF_HEIGHT, 0)
		else:
			self.fb.fill_rect(0, Matrix.HALF_HEIGHT, Matrix.WIDTH,
				Matrix.HALF_HEIGHT, 0)

		self.redraw_twice()

	def _write(self, register_add, data):
		self.cs_pin.value(0)
		
		for _ in range(const.CASCADED_MATRIXES):
			self.spi.write(bytearray([register_add, data]))
		
		self.cs_pin.value(1)

