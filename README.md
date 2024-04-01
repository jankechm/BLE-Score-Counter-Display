# BLE score counter and clock on a matrix display.
- The display consists of eight 8*8 LED matrixes controlled by MAX7219.
- JDY-33 Bluetooth Low Energy 4.2 module is used for communication with a smartphone.
- The code runs on RP2040 MCU (Raspberry Pi Pico) with installed micropython interpreter.
- The internal RTC is synchronized with the time from a smartphone.

https://github.com/jankechm/BLE-Score-Counter-Display/assets/22982620/9a814e2d-1ac7-41b0-a2dc-2a36e0cf6935

This is the continuation of https://github.com/jankechm/score_counter but the IR transmitter/receiver was replaced by Bluetooth Low Energy and a smartphone app. Also, the external DS3231 RTC module was removed since the time is now synchronized with smartphone and then counted by the internal RTC.
