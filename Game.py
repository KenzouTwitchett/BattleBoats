import replit
from Player import Player
from Helper import get_boat_grid, get_hit_grid, convert_coordinate_to_grid_index, convert_grid_index_to_coordinate, merge_grids
import random
import os

class Game:
  def __init__(self):
    self.player = Player(True)
    self.computer = Player(False)
    self.running = True
    self.turns = 1
    self.last_turn_message = ""
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
        self.game_loop()
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
    i = 0
    # this is a while loop not a for loop for a good reason
    while i < max_boats:
      replit.clear()
      print(self.last_turn_message)
      print(get_boat_grid(self.player))
      print(f"\nInput coordinate for boat ({max_boats - i} boat{"s" if i != (max_boats-1) else ""} left):")
      coordinate_string = input("> ")
      coordinate = convert_coordinate_to_grid_index(coordinate_string)
      if not coordinate:
        # skip this increment since this is an invalid coordinate
        self.last_turn_message = f"Coordinate {coordinate_string.upper()} invalid!"
        continue
      
      # else check to see if the coordinate exists
      try:
        self.player.boat_grid[coordinate[0]][coordinate[1]]
      except IndexError:
        # it's out of bounds so skip
        self.last_turn_message = f"Coordinate {coordinate_string.upper()} invalid!"
        continue

      # else check to see if there's already a boat there
      if self.player.boat_grid[coordinate[0]][coordinate[1]] != " ":
        # boat exists :(
        self.last_turn_message = f"Boat already placed at {coordinate_string.upper()}!"
        continue

      # finally set it if all those checks pass
      self.player.boat_grid[coordinate[0]][coordinate[1]] = "B"
      self.last_turn_message = f"Boat placed at {coordinate_string.upper()}!"

      # if this was a for loop every time i had to skip id have to write i -= 1
      # but now we can just manually increment i
      i += 1

    i = 0
    # then get computer to place boats
    while i < max_boats:
      row = random.randint(0, len(self.computer.boat_grid)-1)
      col = random.randint(0, len(self.computer.boat_grid[row])-1)

      # coordinate will never be out of bounds
      # but still need to check for boatage here
      if self.computer.boat_grid[row][col] != " ":
        continue

      # place boat for computer
      self.computer.boat_grid[row][col] = "B"
      i += 1

    # replit.clear()
    # print("Player grid:")
    # print(get_boat_grid(self.player))
    # print("Computer grid:")
    # print(get_boat_grid(self.computer))

    self.last_turn_message = ""
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
    if self.computer.boat_grid[coordinate[0]][coordinate[1]] == "B":
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
        if self.computer.boat_grid[row][col] == "B":
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
    
    if self.player.boat_grid[row][col] == "B":
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
        if self.player.boat_grid[row][col] == "B":
          computer_won = False
          break
      if not computer_won: break
    
    if computer_won:
      self.computer_win()

    self.turns += 1

  def import_state(self):
    with open("./state", "r") as state_file:
      self.turns = int(state_file.readline())
      self.running = bool(state_file.readline())
      self.player.import_state(state_file)
      self.computer.import_state(state_file)

  def export_state(self):
    with open("./state", "w") as state_file:
      state_file.write(str(self.turns) + "\n")
      state_file.write(str(self.running) + "\n")
      state_file.write(self.player.export_state())
      state_file.write(self.computer.export_state())

  def player_win(self):
    replit.clear()
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
