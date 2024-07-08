import typing
if typing.TYPE_CHECKING:
    from Player import Player


def __get_grid(grid:list[list[str]]) -> str:
  alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
  ret = ""
  ret += " " + alphabet[0:len(grid)] + "\n"
  for row in range(len(grid)):
    ret += str(row + 1)
    for col in range(len(grid[row])):
      ret += grid[row][col]
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
  return f"{coordinate[0] + 1}{alphabet[coordinate[1]]}"

# this is my code
def list_to_string(list:list) -> str:
  return "!".join(["-".join(row) for row in list])

def string_to_list(string):
    return [row.split("-") for row in string.split("!")]
