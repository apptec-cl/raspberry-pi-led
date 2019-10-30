
# import FakeRPi.GPIO as GPIO
import RPi.GPIO as GPIO

pins = {'pin_R': 24, 'pin_G': 26, 'pin_B': 13}

GPIO.setmode(GPIO.BCM)       # Numbers GPIOs by physical location

for i in pins:
        GPIO.setup(pins[i], GPIO.OUT)   # Set pins' mode is output
        GPIO.output(pins[i], GPIO.HIGH) # Set pins to high(+3.3V) to off led

p_R = GPIO.PWM(pins['pin_R'], 2000)     # Initial duty Cycle = 0(leds off)
p_G = GPIO.PWM(pins['pin_G'], 2000)
p_B = GPIO.PWM(pins['pin_B'], 2000)

p_R.start(0)      # Initial duty Cycle = 0(leds off)
p_G.start(0)
p_B.start(0)


class Led:

	def __init__(self, color):
		self.color = self.transform_to_hex(color)
		self.colors = [0xFF0000, 0x00FF00, 0x0000FF, 0xFFFF00, 0x00FFFF, 0xFF00FF, 0xFFFFFF, 0x9400D3]
        
	def map(self,x, in_min, in_max, out_min, out_max):
	        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

	def change_color(self):   # For example : col = 0x112233

		R_val = (self.color & 0x110000) >> 16
		G_val = (self.color & 0x001100) >> 8
		B_val = (self.color & 0x000011) >> 0
		
		R_val = self.map(R_val, 0, 255, 0, 100)
		G_val = self.map(G_val, 0, 255, 0, 100)
		B_val = self.map(B_val, 0, 255, 0, 100)
		
		p_R.ChangeDutyCycle(100-R_val)     # Change duty cycle
		p_G.ChangeDutyCycle(100-G_val)
		p_B.ChangeDutyCycle(100-B_val)
		
		print("Led Changed")

	def transform_to_hex(self, string_hex):
		hex_str = string_hex
		hex_int = int(hex_str, 16)
		new_int = hex_int + 0x200
		return new_int

	def turn_off(self):
		p_R.stop()
		p_G.stop()
		p_B.stop()
		for i in pins:
			GPIO.output(pins[i], GPIO.HIGH)    # Turn off all leds
		GPIO.cleanup()
		
