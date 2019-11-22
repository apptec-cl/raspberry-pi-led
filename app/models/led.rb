class Led < ApplicationRecord

	belongs_to :color
	belongs_to :group

	attr_accessor :color_type
	attr_accessor :stdout

	before_validation :set_color
	before_create :set_color_led

	def set_color
		self.color_id = Color.find_by(hexadecimal: self.color_type).id
	end

	def set_color_led
		client = Hue::Client.new
		group = client.group(self.group_id)
		group.lights.each do |light|
			light.brightness = 255
			light.hue = self.color.hue
		end
# 		self.stdout = system("bash lib/led.sh start #{self.color.hexadecimal} &> /dev/null &")
	end
end
