#!/usr/bin/env python
import time
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-c", help="Color in Hexadecimal")
parser.add_argument("-e", help="Enviroment")

params = parser.parse_args()


if params.e == "prod":
	import RPi.GPIO as GPIO
else:
	import FakeRPi.GPIO as GPIO

#colors = [0xFF0000, 0x00FF00, 0x0000FF, 0xFFFF00, 0x00FFFF, 0xFF00FF, 0xFFFFFF, 0x9400D3]
pins = {'pin_R':24, 'pin_G':26, 'pin_B':13}  # pins is a dict

GPIO.setmode(GPIO.BCM)       # Numbers GPIOs by physical location
for i in pins:
        GPIO.setup(pins[i], GPIO.OUT)   # Set pins' mode is output
        GPIO.output(pins[i], GPIO.HIGH) # Set pins to high(+3.3V) to off led

p_R = GPIO.PWM(pins['pin_R'], 2000)  # set Frequece to 2KHz
p_G = GPIO.PWM(pins['pin_G'], 2000)
p_B = GPIO.PWM(pins['pin_B'], 2000)

p_R.start(0)      # Initial duty Cycle = 0(leds off)
p_G.start(0)
p_B.start(0)

def map(x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def setColor(col):   # For example : col = 0x112233
# 	R_val = map(R_val, 0, 255, 0, 100)
# 	G_val = map(G_val, 0, 255, 0, 100)
# 	B_val = map(B_val, 0, 255, 0, 100)

	transform = hex_to_rgb(col)

	R_val = map(transform[0], 0, 255, 0, 100)
	G_val = map(transform[1], 0, 255, 0, 100)
	B_val = map(transform[2], 0, 255, 0, 100)	
	print("-----------")
	print(transform)
	print(R_val)
	print(G_val)
	print(B_val)
	print("-----------")

	p_R.ChangeDutyCycle(100-R_val)     # Change duty cycle
	p_G.ChangeDutyCycle(100-G_val)
	p_B.ChangeDutyCycle(100-B_val)

def hex_to_rgb(hex):
	hex = hex.lstrip('#')
	hlen = len(hex)
	return tuple(int(hex[i:i+hlen/3], 16) for i in range(0, hlen, hlen/3))
try:
	while True:
		setColor('#'+params.c)
		time.sleep(1000.0)
except KeyboardInterrupt:
        p_R.stop()
        p_G.stop()
        p_B.stop()
        for i in pins:
                GPIO.output(pins[i], GPIO.HIGH)    # Turn off all leds
        GPIO.cleanup()
