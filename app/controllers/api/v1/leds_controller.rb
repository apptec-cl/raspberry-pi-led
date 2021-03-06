class Api::V1::LedsController < ApplicationController
	def create
		led = Led.new led_params
		render json: (led.save ? {response: false, msg: led.stdout} : {response: false, msg: led.errors}), status: (led.save ? :ok : :internal_server_error)
	end
	private
		def led_params
			params.require(:led).permit(:color_type, :ip, :group_id)
		end
end
