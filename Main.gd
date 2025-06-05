extends Control

var board = ["", "", "", "", "", "", "", "", ""]
var player_turn = true
var game_over = false

func pythonpath():
	var output: Array = []
	var exit_code = OS.execute("where", ["python"], output, true)

	if exit_code == 0:
		for line in output:
			print(line.split("\r\n")[0])
			return line.split("\r\n")[0]
	else:
		print("Python not found in PATH!")
		
		
func _ready():
	start_game()


#func _ready2():
	#
       #var script_path = "res://xsolla-zk-lib/tictactoe-getBoard.py"  # path inside the project—needs conversion
	#var full_script_path = ProjectSettings.globalize_path(script_path)
#
	#var args = [full_script_path]
	#var output = []
	#var error = []
	#
	#var python_path = pythonpath()
#
	#var exit_code = OS.execute(python_path, args, output, true)
	#
	#var output_json = JSON.parse_string(output[0])
	#if output_json:
		#print("Board: ", output_json["board"])
		#var cn = 0
		#for x in range(3):
			#for y in range(3):
				#board[cn] = output_json["board"][y][x]
				#cn = cn + 1
	#else:
		#print("Parsing JSON error:", output[0])
#
	##print("Exit code:", exit_code)
	##print("stdout:", output_json)
	##print("stderr:", error)
	#update_ui()
	


func make_move(index):
	if game_over or board[index] != "":
		print("Game over or cell taken!")
		return

	if player_turn:
		# Convert flat index to row/col
		var row = int(index / 3)
		var col = index % 3

		# Locate Python
		var python = pythonpath()
		if not python:
			print("Python not found")
			return

		# Absolute path to send_move.py
		var script_path = ProjectSettings.globalize_path("res://xsolla-zk-lib/tictactoe-move.py")
		var args = [script_path, str(row), str(col)]
		var output := []
		var exit_code := OS.execute(python, args, output, true)

		if exit_code != 0:
			print("Python call failed:", output)
			return

		print("Sent move:", output[0])

		# Wait for transaction to settle (optional: delay or poll)
		await get_tree().create_timer(1.5).timeout

		# Reload board state
		update_ui()

func update_ui():
	
       var script_path = "res://xsolla-zk-lib/tictactoe-getBoard.py"  # path inside the project—needs conversion
	var full_script_path = ProjectSettings.globalize_path(script_path)

	var args = [full_script_path]
	var output = []
	
	var python_path = pythonpath()

	var exit_code = OS.execute(python_path, args, output, true)
	
	var output_json = JSON.parse_string(output[0])
	if output_json:
		print("Board: ", output_json["board"])
		var cn = 0
		for x in range(3):
			for y in range(3):
				board[cn] = output_json["board"][x][y]
				cn = cn + 1
	else:
		print("Parsing JSON error:", output[0])
	
	for i in range(9):
		var cell = get_node("GridContainer/Cell" + str(i))
		if cell != null:
			cell.text = board[i]
		else:
			print("Cell", i, " not found!")
	
	check_winner()

func check_winner():
	var wins = [
		[0,1,2], [3,4,5], [6,7,8],
		[0,3,6], [1,4,7], [2,5,8],
		[0,4,8], [2,4,6]
	]
	for combo in wins:
		var a = combo[0]
		var b = combo[1]
		var c = combo[2]
		if board[a] != "" and board[a] == board[b] and board[b] == board[c]:
			game_over = true
			show_result("%s wins!" % board[a])
			return

	if not board.has(""):
		game_over = true
		show_result("Draw")

func show_result(text):
	var popup = AcceptDialog.new()
	popup.dialog_text = text
	add_child(popup)
	popup.popup_centered()
	popup.confirmed.connect(self.start_game)

func start_game():
	# Get Python executable path
	var python_path = pythonpath()
	if not python_path:
		print("Python not found")
		return

	# Path to start_game.py (must be outside res:// for execution)
	var script_path = ProjectSettings.globalize_path("res://xsolla-zk-lib/tictactoe-startGame.py")

	# Call start_game.py
	var args = [script_path]
	var output := []
	var error := []

	var exit_code = OS.execute(python_path, args, output, true)
	if exit_code == 0:
		print("start_game.py executed successfully")
		for line in output:
			print(line)
	else:
		print("start_game.py failed")
		for line in error:
			print("Error:", line)

	# Continue with board fetch
	update_ui()
	game_over = false
