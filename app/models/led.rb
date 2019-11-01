class Led < ApplicationRecord
	belongs_to :color

	attr_accessor :color_type

	after_validation :set_color

	after_create :set_color_led

	def set_color
		self.color_id = Color.find_by(hexadecimal: self.color_type).id
	end

	def set_color
		Open3.popen3("python lib/ledrgb.py") do |stdout, stderr|
			puts stdout
		end
	end
end
