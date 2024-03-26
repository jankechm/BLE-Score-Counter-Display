# Author: Marek Jankech

import app.constants as const
from app.display import Matrix
from machine import Pin, SPI

# Display SPI config 
mx_spi = SPI(const.DISPLAY_SPI_ID, baudrate=const.DISPLAY_SPI_BAUD,
	polarity=const.DISPLAY_SPI_POLARITY, phase=const.DISPLAY_SPI_PHASE,
	sck=Pin(const.DISPLAY_SPI_CLK_PIN),
	mosi=Pin(const.DISPLAY_SPI_MOSI_PIN))
cs_pin = Pin(const.DISPLAY_SPI_CS_PIN, Pin.OUT)

# LED matrix singleton
display = Matrix(mx_spi, cs_pin, const.INITIAL_BRIGHTNESS)