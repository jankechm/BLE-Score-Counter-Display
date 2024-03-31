# Author: Marek Jankech

########################
# Bit operations
########################
ONE_NIBBLE = 4
ONE_BYTE = 8
HIGHER_NIBBLE_MASK = 0XF0
LOWER_NIBBLE_MASK = 0X0F

########################
# Matrixes
########################
ROWS_IN_MATRIX = 8
COLS_IN_MATRIX = 8
CASCADED_MATRIXES = 8
MATRIXES_IN_ROW = 4
MATRIXES_IN_COL = 2

########################
# Offsets
########################
ONE_DIGIT_X_OFFSET = 4
ONE_DIGIT_IS_1_X_OFFSET = 7
FIRST_DIGIT_X_OFFSET = 2
SECOND_DIGIT_X_OFFSET = 6
SECOND_DIGIT_MEDIUM_FONT_X_OFFSET = 8
SECOND_DIGIT_IS_1_X_OFFSET = 12
RIGHT_SIDE_X_OFFSET = 16
RIGHT_SIDE_MEDIUM_FONT_X_OFFSET = 18

########################
# MAX7291 registers
########################
NOOP = 0x00
DECODEMODE = 0x09
INTENSITY = 0x0A
SCANLIMIT = 0x0B
SHUTDOWN = 0x0C
DISPLAYTEST = 0x0F

########################
# MAX7291 register values
########################
SHUTDOWN_MODE_ON = 0X00
SHUTDOWN_MODE_OFF = 0X01
DISPLAY_TEST_ON = 0X01
DISPLAYTEST_TEST_OFF = 0X00
SCANLIMIT_8_DIGITS = 0X07
NO_BCD_DECODE = 0X00
INITIAL_BRIGHTNESS = 0X03
ROW0 = 0x01

########################
# SPI & UART
########################
DISPLAY_SPI_ID = 1
DISPLAY_SPI_BAUD = 5_000_000
DISPLAY_SPI_POLARITY = 1
DISPLAY_SPI_PHASE = 0

BLE_UART_ID = 0
BLE_UART_BAUD = 9600

########################
# RTC
########################
RTC_HOURS_IDX = 4
RTC_MINUTES_IDX = 5

########################
# Pins
########################
RTC_I2C_SDA_PIN = 26
RTC_I2C_SCL_PIN = 27

BLE_UART_TX = 16
BLE_UART_RX = 17

DISPLAY_SPI_CS_PIN = 13
DISPLAY_SPI_CLK_PIN = 14
DISPLAY_SPI_MOSI_PIN = 15

RECV_PIN = 28

########################
# Halves & quarters
########################
LEFT = 1
RIGHT = 2
LEFT_AND_RIGHT = 3

TOP_ROW = 1
BOTTOM_ROW = 2

TOP_LEFT = 1
TOP_RIGHT = 2
BOTTOM_LEFT = 3
BOTTOM_RIGHT = 4

########################
# BLE
########################
SET_SCORE_CMD_PREFIX = "SET_SCORE="
SET_TIME_CMD_PREFIX = "SET_TIME="
SET_SCORE_CMD_SCORE_DELIMITER = ":"

CR = 13
LF = 10

########################
# Date & time
########################
DEC_BASE = 10
MILLENIUM = 2000
