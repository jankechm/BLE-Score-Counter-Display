# Author: Marek Jankech

from machine import Pin
from app.mx_data import MxScore
from app.data import Config
# TODO
# from app.mx_data import MxDate, MxTime
from app.hw import display, ble_uart, rtc
from app.view import BasicViewer

import uasyncio as asyncio
import ujson as json
import app.constants as const

import micropython
import gc
import os

class App:
	def __init__(self):
		"""
		Main application. 
		Evaluates user inputs from BLE remote control and performs appropriate
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

		self.basic_viewer = BasicViewer()
		self.basic_viewer.score = self.mx_score  # type: ignore

		self.ble_reader = asyncio.StreamReader(ble_uart)
		self.ble_writer = asyncio.StreamWriter(ble_uart, {})

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
		score_and_timestamp = cmd[len(const.SET_SCORE_CMD_PREFIX):]\
			.split(const.TIMESTAMP_DELIMITER)
		if len(score_and_timestamp) == 2:
			score = score_and_timestamp[0]\
				.split(const.SET_SCORE_CMD_SCORE_DELIMITER)
			if len(score) == 2:
				isOk = False
				try:
					left_score = int(score[0])
					right_score = int(score[1])
					timestamp = int(score_and_timestamp[1])
					isOk = True
				except ValueError:
					print("Unable to parse score and timestamp!")
				if isOk:
					self.basic_mode = False
					self.basic_viewer.disable()
					self.mx_score.timestamp = timestamp
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

	def handle_set_bright_cmd(self, cmd: str):
		print("Handle SET_BRIGHTNESS command")
		brightness = cmd[len(const.SET_BRIGHTNESS_CMD_PREFIX):]
		isOk = False
		try:
			level = int(brightness)
			isOk = True
		except ValueError:
			print("Unable to parse brightness level!")
		if isOk:
			if level < const.MIN_BRIGHTNESS:
				level = const.MIN_BRIGHTNESS
			elif level > const.MAX_BRIGHTNESS:
				level = const.MAX_BRIGHTNESS
			self.display.set_brightness(level)
			self.basic_viewer.config.bright_lvl = level

	def handle_set_show_score_cmd(self, cmd: str):
		print("Handle SET_SHOW_SCORE command")
		show_score_str = cmd[len(const.SET_SHOW_SCORE_CMD_PREFIX):]
		show_score = self.parse_bool_str_cmd_val(show_score_str)
		if show_score is None:
			print("Invalid show score value!")
		else:
			# Halt rendering only if show_score value is different
			# than the value in current config.
			if self.basic_viewer.config.use_score != show_score:
				self.basic_mode = False
				self.basic_viewer.disable()
				self.basic_viewer.config.use_score = show_score
				self.basic_mode = True

	def handle_set_show_date_cmd(self, cmd: str):
		print("Handle SET_SHOW_DATE command")
		show_date_str = cmd[len(const.SET_SHOW_DATE_CMD_PREFIX):]
		show_date = self.parse_bool_str_cmd_val(show_date_str)
		if show_date is None:
			print("Invalid show date value!")
		else:
			# Halt rendering only if show_date value is different
			# than the value in current config.
			if self.basic_viewer.config.use_date != show_date:
				self.basic_mode = False
				self.basic_viewer.disable()
				self.basic_viewer.config.use_date = show_date
				self.basic_mode = True

	def handle_set_show_time_cmd(self, cmd: str):
		print("Handle SET_SHOW_TIME command")
		show_time_str = cmd[len(const.SET_SHOW_TIME_CMD_PREFIX):]
		show_time = self.parse_bool_str_cmd_val(show_time_str)
		if show_time is None:
			print("Invalid show time value!")
		else:
			# Halt rendering only if show_time value is different
			# than the value in current config.
			if self.basic_viewer.config.use_time != show_time:
				self.basic_mode = False
				self.basic_viewer.disable()
				self.basic_viewer.config.use_time = show_time
				self.basic_mode = True
	
	def handle_set_scroll_cmd(self, cmd: str):
		print("Handle SET_SCROLL command")
		scroll_str = cmd[len(const.SET_SCROLL_CMD_PREFIX):]
		scroll = self.parse_bool_str_cmd_val(scroll_str)
		if scroll is None:
			print("Invalid scroll value!")
		else:
			# Halt rendering only if scroll value is different
			# than the value in current config.
			if self.basic_viewer.config.scroll != scroll:
				self.basic_mode = False
				self.basic_viewer.disable()
				self.basic_viewer.config.scroll = scroll
				self.basic_mode = True

	async def handle_get_score_cmd(self, cmd: str):
		print("Handle GET_SCORE command")
		score = self.mx_score.score
		cmd_to_send = "{}{}:{}T{}\r\n".format(
			const.SCORE_CMD_PREFIX, score.left, score.right, 
			self.mx_score.timestamp)
		print("Sending {}".format(cmd_to_send))
		await self.ble_writer.awrite(cmd_to_send.encode('ascii'))

	async def handle_get_cfg_cmd(self, cmd: str):
		print("Handle GET_CONFIG command")
		cfg_str = json.dumps(self.basic_viewer.config.__dict__)
		cmd_to_send = "{}{}\r\n".format(
			const.CONFIG_CMD_PREFIX, cfg_str)
		print("Sending {}".format(cmd_to_send))
		await self.ble_writer.awrite(cmd_to_send.encode('ascii'))

	def handle_persist_cfg_cmd(self, cmd: str):
		print("Handle PERSIST_CONFIG command")
		cfg_str = cmd[len(const.PERSIST_CONFIG_CMD_PREFIX):]
		isOk = False
		try:
			# Just test that the json config could be converted to Config obj
			cfg_dict = json.loads(cfg_str)
			Config(**cfg_dict)
			isOk = True
		except ValueError | TypeError:
			print("Unable to parse Config!")
		if isOk:
			if not self.dir_exists(const.DATA_DIR):
				os.mkdir(const.DATA_DIR)
			with open(const.DATA_DIR + "/" + const.CONFIG_FILE, "w") as f:
				f.write(cfg_str + "\n")

	def handle_all_leds_on_cmd(self, cmd: str):
		print("Handle SET_ALL_LEDS_ON command")
		all_leds_on_str = cmd[len(const.SET_ALL_LEDS_ON_CMD_PREFIX):]
		all_leds_on = self.parse_bool_str_cmd_val(all_leds_on_str)
		if all_leds_on is None:
			print("Invalid value for SET_ALL_LEDS_ON!")
		else:
			if all_leds_on:
				print("Set all LEDs on!")
				self.basic_mode = False
				self.basic_viewer.disable()
				self.display.fill(1)
				self.display.redraw_twice()
			else:
				print("Disable all LEDs on!")
				self.basic_mode = True

	def parse_bool_str_cmd_val(self, str_val: str):
		if str_val == "1":
			bool_val = True
		elif str_val == "0":
			bool_val = False
		else:
			bool_val = None
		return bool_val
	
	def dir_exists(self, dir_path):
		try:
			os.listdir(dir_path)
			return True
		except OSError:
			return False

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

	async def recv_cmd(self):
		while True:
			cmd = await self.ble_reader.readline()
			if (cmd is not None and len(cmd) > 2
					and cmd[-2] == const.CR and cmd[-1] == const.LF):
				decoded = cmd[0:-2].decode('ascii')
				print("Received command: {}".format(decoded))

				if decoded.startswith(const.SET_SCORE_CMD_PREFIX):
					await self.handle_set_score_cmd(decoded)
				elif decoded.startswith(const.GET_SCORE_CMD):
					await self.handle_get_score_cmd(decoded)
				elif decoded.startswith(const.SET_TIME_CMD_PREFIX):
					self.handle_set_time_cmd(decoded)
				elif decoded.startswith(const.SET_BRIGHTNESS_CMD_PREFIX):
					self.handle_set_bright_cmd(decoded)
				elif decoded.startswith(const.SET_SHOW_SCORE_CMD_PREFIX):
					self.handle_set_show_score_cmd(decoded)
				elif decoded.startswith(const.SET_SHOW_DATE_CMD_PREFIX):
					self.handle_set_show_date_cmd(decoded)
				elif decoded.startswith(const.SET_SHOW_TIME_CMD_PREFIX):
					self.handle_set_show_time_cmd(decoded)
				elif decoded.startswith(const.SET_SCROLL_CMD_PREFIX):
					self.handle_set_scroll_cmd(decoded)
				elif decoded.startswith(const.GET_CONFIG_CMD):
					await self.handle_get_cfg_cmd(decoded)
				elif decoded.startswith(const.PERSIST_CONFIG_CMD_PREFIX):
					self.handle_persist_cfg_cmd(decoded)
				elif decoded.startswith(const.SET_ALL_LEDS_ON_CMD_PREFIX):
					self.handle_all_leds_on_cmd(decoded)

	async def main(self):
		asyncio.create_task(self.led_blink())
		asyncio.create_task(self.basic_operation())
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
