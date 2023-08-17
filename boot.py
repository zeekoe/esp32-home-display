# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#from machine import Pin, SoftI2C, ADC
import machine

#pin16 = machine.Pin(2, machine.Pin.OUT)
#pin16.value(0)
from config import user,password
from espidf import VSPI_HOST,HSPI_HOST
from ili9XXX import ili9341
from xpt2046generic import Xpt2046_hw
disp = ili9341(miso=12, mosi=13, clk=14, cs=15, dc=2, rst=-1, power=-1, backlight=21, backlight_on=1, power_on=0, rot=0x80,spihost=VSPI_HOST, mhz=50, factor=16, hybrid=True, width=240, height=320, invert=False, double_buffer=True, half_duplex=False, initialize=True)
#touch = xpt2046(cs=33, spihost=HSPI_HOST, mosi=32, miso=39, clk=25, cal_y0 = 423, cal_y1=3948)


#define XPT2046_SPI_SCLK 25
#define XPT2046_SPI_MOSI 32
#define XPT2046_SPI_MISO 39
#define XPT2046_SPI_FREQ 2000000
#define XPT2046_PIN_INT 36
#define XPT2046_PIN_CS 33
# Calibration 240x320
#define XPT2046_MIN_X 349
#define XPT2046_MAX_X 3859
#define XPT2046_MIN_Y 247
#define XPT2046_MAX_Y 3871


# spi=machine.SoftSPI(
#     baudrate=1_000_000, # the chip does not handle more than 2MHz (!)
#     polarity=0,
#     phase=0,
#     sck=machine.Pin(25, machine.Pin.OUT),
#     mosi=machine.Pin(32, machine.Pin.OUT),
#     miso=machine.Pin(39, machine.Pin.IN),
# )

# tsc=Xpt2046_hw(spi=spi,cs=33,rot=1,ranges=((349,3859),(247,3871)))

import network
print("Connecting to WiFi...")
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(user, password)
while not wifi.isconnected():
    pass
print("Connected.")

import uftpd

