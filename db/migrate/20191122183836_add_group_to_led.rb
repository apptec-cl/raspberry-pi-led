class AddGroupToLed < ActiveRecord::Migration[5.2]
  def change
    add_reference :leds, :group, foreign_key: true
  end
end
