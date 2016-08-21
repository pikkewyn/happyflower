#!/usr/bin/python
 
import spidev
import time
import os
import RPi.GPIO as GPIO
import rrdtool

# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,0)
 
# Function to read SPI data from MCP3008 chip
# Channel must be an integer 0-7
def ReadChannel(channel):
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data
 
# Define sensor channels
moisture_channel = 0

GPIO.setmode(GPIO.BCM)

port_or_pin = 17
led_pin = 23

GPIO.setup(port_or_pin, GPIO.OUT) 
GPIO.setup(led_pin, GPIO.OUT, initial=GPIO.LOW)

GPIO.output(port_or_pin, 1) 
moisture_level = ReadChannel(moisture_channel)
GPIO.output(port_or_pin, 0) 

print moisture_level
with open("/home/janek/moisture/moisture.log", "a") as f:
    f.write("{} {}\n".format(time.strftime("%d-%m_%H:%M"), moisture_level))
    f.close()

#rrdtool.update('/home/janek/moisture/moisture.rrd', 'N:%d' % moisture_level)
#rrdtool.graph('/home/janek/public_html/moisture2.png', "-w 785", "-h 120", "--slope-mode", "--start", "-604800", "--end", "now", 
#    "--vertical-label", "temperature", "DEF:moisture=/home/janek/moisture/moisture.rrd:moisture:MAX") 

os.system('gnuplot /home/janek/moisture/moisture.gp')

if moisture_level < 700:
    GPIO.output(led_pin, GPIO.HIGH)
else:
    GPIO.output(led_pin, GPIO.LOW)

GPIO.cleanup()   
