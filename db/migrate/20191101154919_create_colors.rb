class CreateColors < ActiveRecord::Migration[5.2]
  def change
    create_table :colors do |t|
      t.string :color
      t.string :hexadecimal
      t.string :rgb

      t.timestamps
    end
  end
end
