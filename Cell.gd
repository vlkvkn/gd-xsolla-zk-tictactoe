extends Button

func _ready():
	self.pressed.connect(self._on_pressed)

func _on_pressed():
	var main = get_node("/root/Main")
	var index = int(name.replace("Cell", ""))
	main.make_move(index)
