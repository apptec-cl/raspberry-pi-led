class CreateColors < ActiveRecord::Migration[5.2]
  def change
    create_table :colors do |t|
      t.string :color
      t.string :hexadecimal
      t.string :rgb
	  t.integer :hue
	  t.integer :color_temperature
      t.timestamps
    end
  end
end
