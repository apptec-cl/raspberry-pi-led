
#import FakeRPi.GPIO as GPIO
import RPi.GPIO as GPIO

class Led:

	def __init__(self, color):
		self.color = self.transform_to_hex(color)
		self.colors = [0xFF0000, 0x00FF00, 0x0000FF, 0xFFFF00, 0x00FFFF, 0xFF00FF, 0xFFFFFF, 0x9400D3]
		self.pins = {'pin_R': 24, 'pin_G': 26, 'pin_B': 13}
        
	def map(self,x, in_min, in_max, out_min, out_max):
	        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

	def change_color(self):   # For example : col = 0x112233

		GPIO.setmode(GPIO.BCM)       # Numbers GPIOs by physical location

		for i in self.pins:
		        GPIO.setup(self.pins[i], GPIO.OUT)   # Set pins' mode is output
		        GPIO.output(self.pins[i], GPIO.HIGH) # Set pins to high(+3.3V) to off led

		p_R = GPIO.PWM(self.pins['pin_R'], 2000)     # Initial duty Cycle = 0(leds off)
		p_G = GPIO.PWM(self.pins['pin_G'], 2000)
		p_B = GPIO.PWM(self.pins['pin_B'], 2000)
		
		p_R.start(0)      # Initial duty Cycle = 0(leds off)
		p_G.start(0)
		p_B.start(0)

		R_val = (self.color & 0x110000) >> 16
		G_val = (self.color & 0x001100) >> 8
		B_val = (self.color & 0x000011) >> 0
		
		R_val = self.map(R_val, 0, 255, 0, 100)
		G_val = self.map(G_val, 0, 255, 0, 100)
		B_val = self.map(B_val, 0, 255, 0, 100)
		print(100-R_val)
		print(100-G_val)
		print(100-B_val)
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
		self.p_R.stop()
		self.p_G.stop()
		self.p_B.stop()
		for i in self.pins:
			GPIO.output(self.pins[i], GPIO.HIGH)    # Turn off all leds
		GPIO.cleanup()
		
