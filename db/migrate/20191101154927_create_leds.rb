class CreateLeds < ActiveRecord::Migration[5.2]
  def change
    create_table :leds do |t|
      t.string :ip
      t.references :color, foreign_key: true

      t.timestamps
    end
  end
end
