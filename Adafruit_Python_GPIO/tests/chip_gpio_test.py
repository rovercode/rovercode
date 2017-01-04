#!/usr/bin/python

import Adafruit_GPIO as GPIO
import time, os

print "GETTING GPIO OBJECT"
gpio = GPIO.get_platform_gpio()


print "SETUP CSID1"
gpio.setup("CSID1", GPIO.OUT)

#print os.path.exists('/sys/class/gpio/gpio133')

print "SETUP XIO-P1"
gpio.setup("XIO-P1", GPIO.IN)
#GPIO.setup("U14_13", GPIO.IN)

print "READING XIO-P1"
gpio.output("CSID1", GPIO.HIGH)
print "HIGH", gpio.input("XIO-P1")

gpio.output("CSID1", GPIO.LOW)
time.sleep(1)
print "LOW", gpio.input("XIO-P1")

gpio.output("CSID1", GPIO.HIGH)
print "HIGH", gpio.input("XIO-P1")
time.sleep(1)

gpio.output("CSID1", GPIO.LOW)
print "LOW", gpio.input("XIO-P1")

print "CLEANUP"
gpio.cleanup()