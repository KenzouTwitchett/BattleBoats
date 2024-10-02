import replit
from Player import Player
from Helper import check_coordinate, check_coordinate_string, check_orientation_string, convert_orientation_string, get_boat_grid, get_hit_grid, convert_coordinate_to_grid_index, convert_grid_index_to_coordinate, merge_grids, readline, get_boat_info, get_boat_chunk_letter, boat_chunk_letters
import random
import os
import json

class Game:
  def __init__(self):
    self.player = Player(True)
    self.computer = Player(False)
    self.running = True
    self.turns = 1
    self.last_turn_message = ""
    self.setup_finished = False
    self.setup_stage = 0
    self.boat_types = [
      {
        "size": 1,
        "count": 2,
        "name": "Destroyer"
      },
      {
        "size": 2,
        "count": 2,
        "name": "Submarine"
      },
      {
        "size": 3,
        "count": 1,
        "name": "Carrier"
      }
    ]
    self.print_menu()

  def print_menu(self):
    replit.clear()
    print("Choose an option:")
    print("  1. New Game")
    if os.path.isfile("./state"):
      print("  2. Resume Game")
    print("  3. Instructions")
    print("  4. Quit")
    chosen_option = input("> ")
    if chosen_option == "1":
      self.game_setup()
    elif chosen_option == "2":
      if os.path.isfile("./state"):
        self.import_state()
        if self.setup_finished:
          self.game_loop()
        else:
          self.game_setup()
      else:
        self.print_menu()
    elif chosen_option == "3":
      self.print_instructions()
    elif chosen_option == "4":
      self.export_state()
      self.quit()
    else:
      self.print_menu()

  def print_instructions(self):
    with open("./instructions.txt") as instructions:
      print(instructions.read())

  def game_setup(self):
    # prompt user to place boats
    max_boats = 5
    # this is a while loop not a for loop for a good reason
    while self.setup_stage < max_boats:
      replit.clear()
      self.export_state()
      boat_info = get_boat_info(self.setup_stage, self.boat_types)
      print(self.last_turn_message)
      print(get_boat_grid(self.player))
      printable_boat = "".join([get_boat_chunk_letter(x, boat_info["size"], "horizontal") for x in range(boat_info["size"])])
      print(f"\nInput{"" if boat_info["size"] == 1 else " left" } coordinate for {printable_boat}:{get_boat_info(self.setup_stage, self.boat_types)["name"]} ({max_boats - self.setup_stage} boat{"s" if self.setup_stage != (max_boats-1) else ""} left):")
      coordinate_string = input("> ")

      # check the coordinate without knowing the type of boat yet
      res = check_coordinate_string(coordinate_string, self.player.boat_grid)

      if not isinstance(res, bool):
        # you FAIL
        self.last_turn_message = res
        continue

      # ok that was successful
      coordinate = convert_coordinate_to_grid_index(coordinate_string) # this wont fail

      orientation = "vertical"
      if boat_info["size"] != 1:
        print("Input orientation for boat:")
        orientation_string = input("> ")
  
        res = check_orientation_string(orientation_string)
  
        if not isinstance(res, bool):
          # you FAIL AGAIN
          self.last_turn_message = res
          continue
  
        # ok that was successful
        orientation = convert_orientation_string(orientation_string)

      # figure out where the boat is going to be placed
      boat_chunk_coordinates = []
      for boat_chunk_index in range(boat_info["size"]):
        if orientation == "vertical":
          boat_chunk_coordinates.append((coordinate[0] + boat_chunk_index, coordinate[1]))
        else:
          boat_chunk_coordinates.append((coordinate[0], coordinate[1] + boat_chunk_index))

      # and check to see if there's any issues with them
      failed = False
      for chunk_coordinate in boat_chunk_coordinates:
        res = check_coordinate(chunk_coordinate, self.player.boat_grid, True)
        if not isinstance(res, bool):
          # you FAIL AGAIN AGAIN
          self.last_turn_message = res
          failed = True
          break
      if failed: continue

      # FINALLY after all those checks IT CAN BE PLACED
      for chunk_index, chunk_coordinate in enumerate(boat_chunk_coordinates):
        letter = get_boat_chunk_letter(chunk_index, boat_info["size"], orientation)
        self.player.boat_grid[chunk_coordinate[0]][chunk_coordinate[1]] = letter
      self.last_turn_message = f"{boat_info["name"]} placed at {coordinate_string.upper()}!"

  
      # if this was a for loop every time i had to skip id have to write i -= 1
      # but now we can just manually increment i
      self.setup_stage += 1

    i = 0
    # then get computer to place boats
    while i < max_boats:
      boat_info = get_boat_info(i, self.boat_types)
      row = random.randint(0, len(self.computer.boat_grid)-2)
      col = random.randint(0, len(self.computer.boat_grid[row])-2)
      coordinate = (row, col)

      orientation = random.choice(["vertical", "horizontal"])

      # figure out where the boat is going to be placed
      boat_chunk_coordinates = []
      for boat_chunk_index in range(boat_info["size"]):
        if orientation == "vertical":
          boat_chunk_coordinates.append((coordinate[0] + boat_chunk_index, coordinate[1]))
        else:
          boat_chunk_coordinates.append((coordinate[0], coordinate[1] + boat_chunk_index))

      # and check to see if there's any issues with them
      failed = False
      for chunk_coordinate in boat_chunk_coordinates:
        res = check_coordinate(chunk_coordinate, self.computer.boat_grid, True)
        if not isinstance(res, bool):
          # fail :(
          #self.last_turn_message = res
          print("fail computer boat place (overlap)")
          failed = True
          break
      if failed: continue

      # aaand place
      for chunk_index, chunk_coordinate in enumerate(boat_chunk_coordinates):
        letter = get_boat_chunk_letter(chunk_index, boat_info["size"], orientation)
        print(f"[computer] place at {coordinate}: {letter}")
        self.computer.boat_grid[chunk_coordinate[0]][chunk_coordinate[1]] = letter
      #self.last_turn_message = f"{boat_info["name"]} placed at {coordinate_string.upper()}!"

      i += 1
    
    # replit.clear()
    # print("Player grid:")
    # print(get_boat_grid(self.player))
    # print("Computer grid:")
    # print(get_boat_grid(self.computer))

    self.last_turn_message = ""
    self.setup_finished = True
    self.game_loop()

  def game_loop(self):
    while self.running:
      self.tick_game()

  def tick_game(self):
    self.export_state()
    replit.clear()
    print(f"Turn {self.turns}:")
    print(self.last_turn_message)
    print(
      merge_grids(
        get_boat_grid(self.player),
        get_hit_grid(self.player),
        "Boats:",
        "Hit:"
      )
    )

    print("Choose a square to target on the computer's board:")
    coordinate_string = input("> ")
    coordinate = convert_coordinate_to_grid_index(coordinate_string)
    if not coordinate:
      # invalid coordinate so skip and go back to the start of the loop
      return
    
    try:
      self.computer.boat_grid[coordinate[0]][coordinate[1]]
    except IndexError:
      # invalid coordinate (out of bounds)
      self.last_turn_message = f"Coordinate {coordinate_string.upper()} invalid!"
      return
    
    if self.player.hit_grid[coordinate[0]][coordinate[1]] != " ":
      # already targeted before
      self.last_turn_message = f"Coordinate {coordinate_string.upper()} already targeted before!"
      return
      
    # else time to check hits
    if self.computer.boat_grid[coordinate[0]][coordinate[1]] in boat_chunk_letters:
      # HIT!
      self.last_turn_message = f"You hit the computer's boat at {coordinate_string.upper()}!"
      self.player.hit_grid[coordinate[0]][coordinate[1]] = "X"
      self.computer.boat_grid[coordinate[0]][coordinate[1]] = "X"
    else:
      # aww miss
      self.last_turn_message = f"You missed the computer's boats at {coordinate_string.upper()}!"
      self.player.hit_grid[coordinate[0]][coordinate[1]] = "-"
      self.computer.boat_grid[coordinate[0]][coordinate[1]] = "o"

    # check if you won
    # just loop over computer's board and see if any boats remain
    player_won = True
    for row in range(len(self.computer.boat_grid)):
      for col in range(len(self.computer.boat_grid[row])):
        if self.computer.boat_grid[row][col] in boat_chunk_letters:
          player_won = False
          break
      if not player_won: break
    
    if player_won:
      self.player_win()

    # and computer's turn
    computer_already_targeted = True
    row = 0
    col = 0
    while computer_already_targeted:
      row = random.randint(0, len(self.computer.boat_grid)-1)
      col = random.randint(0, len(self.computer.boat_grid[row])-1)
      # check if computer's already targeted here
      if self.computer.hit_grid[row][col] == " ":
        computer_already_targeted = False
    
    if self.player.boat_grid[row][col] in boat_chunk_letters:
      # computer hit!
      self.last_turn_message += f"\nComputer hit your boat at {convert_grid_index_to_coordinate((row, col))}"
      self.computer.hit_grid[row][col] = "X"
      self.player.boat_grid[row][col] = "X"
    else:
      # computer missed :(
      self.last_turn_message += f"\nComputer missed your boats at {convert_grid_index_to_coordinate((row, col))}"
      self.computer.hit_grid[row][col] = "-"
      self.player.boat_grid[row][col] = "o"

    # check if computer won
    # same process as above
    computer_won = True
    for row in range(len(self.player.boat_grid)):
      for col in range(len(self.player.boat_grid[row])):
        if self.player.boat_grid[row][col] in boat_chunk_letters:
          computer_won = False
          break
      if not computer_won: break
    
    if computer_won:
      self.computer_win()

    self.turns += 1

  def import_state(self):
    with open("./state", "r") as state_file:
      self.turns = int(readline(state_file))
      self.running = bool(readline(state_file))
      self.setup_stage = int(readline(state_file))
      self.setup_finished = bool(readline(state_file))
      self.last_turn_message = readline(state_file).replace("|","\n")
      self.boat_types = json.loads(readline(state_file))
      self.player.import_state(state_file)
      self.computer.import_state(state_file)

  def export_state(self):
    with open("./state", "w") as state_file:
      state_file.write(str(self.turns) + "\n")
      state_file.write(str(self.running) + "\n")
      state_file.write(str(self.setup_stage) + "\n")
      state_file.write(str(self.setup_finished) + "\n")
      state_file.write(self.last_turn_message.replace("\n","|") + "\n")
      state_file.write(json.dumps(self.boat_types) + "\n")
      state_file.write(self.player.export_state())
      state_file.write(self.computer.export_state())

  def player_win(self):
    replit.clear()
    self.export_state()
    print("You win!")
    print(f"Turns: {self.turns}")
    print("Final board:")
    print(
      merge_grids(
        get_boat_grid(self.player),
        get_hit_grid(self.player),
        "Boats:",
        "Hit:"
      )
    )

    self.quit()

  def computer_win(self):
    replit.clear()
    self.export_state()
    print("You lose!")
    print(f"Turns: {self.turns}")
    print("Final board:")
    print(
      merge_grids(
        get_boat_grid(self.player),
        get_hit_grid(self.player),
        "Boats:",
        "Hit:"
      )
    )

    self.quit()

  def quit(self):
    exit(0)
