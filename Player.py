import io
from Helper import list_to_string, string_to_list

class Player:
  def __init__(self, is_human:bool, grid_size=8):
    self.is_human = is_human
    self.boat_grid = [[" "]*grid_size for _ in range(grid_size)]
    self.hit_grid = [[" "]*grid_size for _ in range(grid_size)]

  def export_state(self) -> str:
    ret = ""
    ret += str(self.is_human) + "\n"
    ret += list_to_string(self.boat_grid) + "\n"
    ret += list_to_string(self.hit_grid) + "\n"
    return ret

  def import_state(self, file:io.TextIOWrapper):
    self.is_human = bool(file.readline())
    self.boat_grid = string_to_list(file.readline())
    self.hit_grid = string_to_list(file.readline())
