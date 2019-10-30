from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from marshmallow_jsonapi.flask import Schema
from marshmallow_jsonapi import fields
from flask_rest_jsonapi import Api, ResourceDetail, ResourceList
from core.led import Led
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

class LedMany(ResourceList):
	schema = ColorSchema
	data_layer = {'session': db.session, 'model': Color}
	def before_post(self, args, kwargs, data):
		led = Led(data['color'])
		led.change_color()

class LedOne(ResourceDetail):
	schema = ColorSchema
	data_layer = {'session': db.session,'model': Color}
	
api = Api(app)
api.route(LedMany, 'led_many', '/leds')
api.route(LedOne, 'led_one', '/leds/<int:id>')

# main loop to run app in debug mode
if __name__ == '__main__':
	app.run(debug=True)