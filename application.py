from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from marshmallow_jsonapi.flask import Schema
from marshmallow_jsonapi import fields
from flask_rest_jsonapi import Api, ResourceDetail, ResourceList
from core.led import Led
import RPi.GPIO as GPIO

# Create a new Flask application
app = Flask(__name__)

# Set up SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///led.db'
db = SQLAlchemy(app)

# Define a class for the Artist table
class Color(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	color = db.Column(db.String)

# Create the table
db.create_all()

# Create data abstraction layer
class ColorSchema(Schema):
	class Meta:
		type_ = 'color'
		self_view = 'led_one'
		self_view_kwargs = {'id': '<id>'}
		self_view_many = 'led_many'
	id = fields.Integer()
	color = fields.Str(required=True)    


colors = [0xFF0000, 0x00FF00, 0x0000FF, 0xFFFF00, 0x00FFFF, 0xFF00FF, 0xFFFFFF, 0x9400D3]
pins = {'pin_R':18, 'pin_G':24, 'pin_B':22}  # pins is a dict

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
        R_val = (col & 0x110000) >> 16
        G_val = (col & 0x001100) >> 8
        B_val = (col & 0x000011) >> 0

        R_val = map(R_val, 0, 255, 0, 100)
        G_val = map(G_val, 0, 255, 0, 100)
        B_val = map(B_val, 0, 255, 0, 100)

        p_R.ChangeDutyCycle(100-R_val)     # Change duty cycle
        p_G.ChangeDutyCycle(100-G_val)
        p_B.ChangeDutyCycle(100-B_val)


class LedMany(ResourceList):
	schema = ColorSchema
	data_layer = {'session': db.session, 'model': Color}
	def before_post(self, args, kwargs, data):
		try:
			setColor(col)
		except KeyboardInterrupt:
			p_R.stop()
			p_G.stop()
			p_B.stop()
			for i in pins:
				GPIO.output(pins[i], GPIO.HIGH)    # Turn off all leds
			GPIO.cleanup()

class LedOne(ResourceDetail):
	schema = ColorSchema
	data_layer = {'session': db.session,'model': Color}
	
api = Api(app)
api.route(LedMany, 'led_many', '/leds')
api.route(LedOne, 'led_one', '/leds/<int:id>')

# main loop to run app in debug mode
if __name__ == '__main__':
	app.run(debug=True)