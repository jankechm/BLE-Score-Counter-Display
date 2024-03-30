# Author: Marek Jankech

from machine import Pin
from app.mx_data import MxScore
# TODO
# from app.mx_data import MxDate, MxTime
from app.hw import display, ble_uart, rtc
from app.view import BasicViewer

import uasyncio as asyncio
import app.constants as const

import micropython
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

		# Info renderable on the matrix
		self.mx_score = MxScore()
		# TODO
		# self.mx_date = MxDate()
		# self.mx_time = MxTime()

		self.basic_viewer = BasicViewer()
		self.basic_viewer.score = self.mx_score  # type: ignore

		self.ble_reader = asyncio.StreamReader(ble_uart)

	# def handle_ble_data_received(self):
	# 	pass
	
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

	async def handle_set_score_cmd(self, cmd: str):
		print("Handle SET_SCORE command")
		score = cmd[len(const.SET_SCORE_CMD_PREFIX):]
		score = score.split(const.SET_SCORE_CMD_SCORE_DELIMITER)
		if len(score) == 2:
			isOk = False
			try:
				left_score = int(score[0])
				right_score = int(score[1])
				isOk = True
			except ValueError:
				print("Unable to parse score!")
			if isOk:
				self.basic_mode = False
				self.basic_viewer.disable()
				await self.mx_score.render_change(left_score, right_score)
				self.basic_mode = True

	def handle_set_time_cmd(self, cmd: str):
		print("Handle SET_TIME command")
		datetime_str = cmd[len(const.SET_TIME_CMD_PREFIX):]
		datetime_split = datetime_str.split()
		print(datetime_split)
		if len(datetime_split) == 3:
			try:
				weekday = int(datetime_split[0])
				
				day_month_year = datetime_split[1].split(".")
				if len(day_month_year) == 3:
					day = int(day_month_year[0])
					month = int(day_month_year[1])
					year = int(day_month_year[2])
				
				hour_minute_second = datetime_split[2].split(":")
				if len(hour_minute_second) == 3:
					hour = int(hour_minute_second[0])
					minute = int(hour_minute_second[1])
					second = int(hour_minute_second[2])

				# Set date and time of the Real Time Clock
				rtc.datetime(
					(year, month, day, weekday, hour, minute, second, 0))
			except ValueError | NameError:
				print("Unable to parse datetime!")

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

	async def recv_cmd(self):
		while True:
			cmd = await self.ble_reader.readline()
			if (cmd is not None and len(cmd) > 2
					and cmd[-2] == const.CR and cmd[-1] == const.LF):
				decoded = cmd[0:-2].decode('ascii')
				print("Received command: {}".format(decoded))

				if decoded.startswith(const.SET_SCORE_CMD_PREFIX):
					await self.handle_set_score_cmd(decoded)
				elif decoded.startswith(const.SET_TIME_CMD_PREFIX):
					self.handle_set_time_cmd(decoded)

	async def main(self):
		asyncio.create_task(self.led_blink())
		asyncio.create_task(self.basic_operation())
		asyncio.create_task(self.setting_operation())
		asyncio.create_task(self.recv_cmd())
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
