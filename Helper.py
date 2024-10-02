import typing
import io
if typing.TYPE_CHECKING:
  from Player import Player


def __get_grid(grid:list[list[str]]) -> str:
  alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
  ret = ""
  ret += "  " + alphabet[0:len(grid)] + "\n"
  #ret += " " + "-" * len(grid) + "\n"
  for row in range(len(grid)):
    ret += str(row + 1) + "|"
    for col in range(len(grid[row])):
      ret += grid[row][col]
    if row != len(grid):
      ret += "\n"
  return ret

def get_boat_grid(player:"Player"):
  return __get_grid(player.boat_grid)

def get_hit_grid(player:"Player"):
  return __get_grid(player.hit_grid)

def merge_grids(grid_1:str, grid_2:str, title_1:str, title_2:str, pad:str = "  |  ") -> str:
  split_1 = grid_1.split("\n")
  split_2 = grid_2.split("\n")
  ret = title_1.ljust(len(split_1[0])) + pad + title_2 + "\n"
  for index in range(len(split_1) - 1): # dunno why I have to subtract 1 but I do
    chunk_1 = split_1[index]
    chunk_2 = split_2[index]
    ret += chunk_1 + pad + chunk_2 + "\n"
  return ret

def convert_coordinate_to_grid_index(coordinate:str) -> tuple[int, int] | bool:
  if len(coordinate) != 2:
    return False
  
  try:
    col_letter = coordinate[0].upper()
    row = int(coordinate[1]) - 1 # subtract one since printed coordinates add one
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    col = alphabet.index(col_letter)
    return (row, col)
  except Exception:
    return False

def convert_grid_index_to_coordinate(coordinate:tuple[int, int]) -> str:
  alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
  return f"{alphabet[coordinate[1]]}{coordinate[0] + 1}"

def get_boat_info(index:int, boat_list:list) -> dict | None:
  found = 0
  for boat in boat_list:
    found += boat["count"]
    if found > index:
      return boat

def readline(file:io.TextIOWrapper) -> str:
  ret = file.readline()
  ret = ret.replace("\n", "") # remove \n at the end
  return ret

def convert_orientation_string(orientation:str) -> str | bool:
  horizontal_strings = [
    "left",
    "right",
    "horizontal",
    "left/right",
    "sideways",
    "flat"
  ]
  
  vertical_strings = [
    "up",
    "down",
    "top",
    "bottom",
    "vertical",
    "up/down",
    "upright",
    "standing" # ??? idk people are silly sometimes
  ]

  if orientation.lower() in horizontal_strings:
    return "horizontal"
  if orientation.lower() in vertical_strings:
    return "vertical"

  # invalid :(
  return False

def check_coordinate(coordinate:tuple[int, int], boat_grid:list[list[str]], is_boat_chunk = False) -> str | bool:
  coordinate_string = convert_grid_index_to_coordinate(coordinate)
  # else check to see if the coordinate exists
  try:
    boat_grid[coordinate[0]][coordinate[1]]
    if coordinate[0] == -1 or coordinate[1] == -1:
      raise(IndexError)
  except IndexError:
    # it's out of bounds so skip
    if is_boat_chunk:
      return f"Boat would be placed at {coordinate_string.upper()} which is out of bounds!"
    else:
      return f"Coordinate {coordinate_string.upper()} is out of bounds!"

  # else check to see if there's already a boat there
  if not boat_grid[coordinate[0]][coordinate[1]] == " ":
    # boat exists :(
    return f"Boat would overlap at {coordinate_string.upper()}!"

  return True

def check_coordinate_string(coordinate_string:str, boat_grid:list[list[str]]) -> str | bool:

  if coordinate_string.strip() == "":
    return "Please enter a coordinate!"
  
  coordinate = convert_coordinate_to_grid_index(coordinate_string)

  if not coordinate:
    # skip this increment since this is an invalid coordinate
    return f"Coordinate {coordinate_string.upper()} is invalid!"

  return check_coordinate(coordinate, boat_grid)

def check_orientation_string(orientation_string:str) -> str | bool:
  orientation = convert_orientation_string(orientation_string)
  if isinstance(orientation, bool):
    return f"Orientation {orientation_string.lower()} is invalid!"

  return True

def get_boat_chunk_letter(i:int, boat_size:int, direction:str) -> str:
  if boat_size == 1:
    return "#"
  if boat_size == 2:
    if direction == "horizontal":
      return "<>"[i]
    else:
      return "ΛV"[i]
  if boat_size == 3:
    if direction == "horizontal":
      return "<=>"[i]
    else:
      return "Λ║V"[i]

  return "B"

boat_chunk_letters = [
  "#",
  "<", ">", "Λ", "V",
  "=", "║"
]