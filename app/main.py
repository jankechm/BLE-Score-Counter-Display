# Author: Marek Jankech

from machine import Pin
from app.mx_data import MxScore
# TODO
# from app.mx_data import MxDate, MxTime
from app.hw import display
from app.view import BasicViewer

import uasyncio as asyncio
import app.constants as const

import micropython
import utime
import gc

class App:
	def __init__(self):
		"""
		Main application. 
		Evaluates user inputs from remote control and performs appropriate
		actions on matrix display.
		It uses asynchronous tasks execution (cooperative multitasking)
		to pretend parallelism.
		"""

		# Flags
		self.set_left_score = False
		self.set_right_score = False
		self.brightness_changed = False
		self.score_reset = False
		self.revert_score = False
		self.exit = False
		self.basic_mode = True
		self.display_on = True
		
		self.last_button = 0x00
		self.exit_cnt = 0

		self.display = display

		# Count ticks for measuring period between button pushes
		self.ticks = utime.ticks_ms()

		# Info renderable on the matrix
		self.mx_score = MxScore()
		# TODO
		# self.mx_date = MxDate()
		# self.mx_time = MxTime()

		self.basic_viewer = BasicViewer()
		self.basic_viewer.score = self.mx_score  # type: ignore

	def exec_not_too_fast(self, change):
		"""
		Execute the code conditionally.
		Avoid unwanted double increment/decrement of values
		- two changes of the same type in a very short time.
		"""
		
		MIN_TICKS_DIFF = 200

		t_curr = utime.ticks_ms()
		t_diff = utime.ticks_diff(t_curr, self.ticks)
		executed = False
		# t_diff can also be negative, after a period of time
		if t_diff > MIN_TICKS_DIFF or t_diff < 0:
			self.ticks = t_curr
			# Execute the change itself
			change()
			executed = True
		return executed
	
	def handle_btn_left(self):
		"""
		Left score
		"""

		if self.basic_mode:
			self.set_left_score = True
			self.basic_mode = False
			self.mx_score.render()
			print("Setting left score...")

	def toggle_on_off(self):
		"""
		Toggle display on/off.
		"""

		if self.display_on:
			print("Off")
			self.display.turn_off()
			self.display_on = False
		else:
			print("On")
			self.display.turn_on()
			self.display_on = True

	def reinit_display(self):
		"""
		Reinitialize display.
		"""

		print("Resetting display...")
		# TODO last brigtness level
		self.display.reinit_display(const.INITIAL_BRIGHTNESS)

	def exit_program(self):
		self.exit = True
		self.basic_mode = False

	async def led_blink(self):
		led_onboard = Pin(25, Pin.OUT)

		while True:
			led_onboard.toggle()
			await asyncio.sleep_ms(500)

	async def mem_monitor(self):
		while True:
			print("Free memory: {:.2f} KB".format(gc.mem_free() / 1024))
			await asyncio.sleep_ms(3000)

	async def basic_operation(self):
		while True:
			if self.basic_mode:
				await self.basic_viewer.view_info()
			# pass execution to other tasks
			await asyncio.sleep_ms(0)

	async def setting_operation(self):
		while True:
			if not self.basic_mode:
				self.basic_viewer.disable()

				if self.set_left_score or self.set_right_score:
					self.display.clear_half(
						const.LEFT if self.set_left_score else const.RIGHT)
					await asyncio.sleep_ms(300)
					# TODO disable UART IRQ
					self.mx_score.render()
					# TODO enable UART IRQ
					await asyncio.sleep_ms(650)

				self.basic_mode = True
				
			# pass execution to other tasks
			await asyncio.sleep_ms(0)

	async def main(self):
		asyncio.create_task(self.led_blink())
		asyncio.create_task(self.basic_operation())
		asyncio.create_task(self.setting_operation())
		# asyncio.create_task(self.mem_monitor())

		print('Running')

		# Run forever
		while not self.exit:
			await asyncio.sleep(2)

		print('Exit')


# Allocate buffer for exceptions during interrupt service routines
micropython.alloc_emergency_exception_buf(100)

try:
	print('Start')
	app = App()
	asyncio.run(app.main())
except KeyboardInterrupt:
	print('Interrupted')
finally:
	asyncio.new_event_loop()  # Clear retained state
