import io
import json

from Helper import readline

class Player:
  def __init__(self, is_human:bool, grid_size=8):
    self.is_human = is_human
    self.boat_grid = [[" "]*grid_size for _ in range(grid_size)]
    self.hit_grid = [[" "]*grid_size for _ in range(grid_size)]

  def export_state(self) -> str:
    ret = ""
    ret += str(self.is_human) + "\n"
    ret += json.dumps(self.boat_grid) + "\n"
    ret += json.dumps(self.hit_grid) + "\n"
    return ret

  def import_state(self, file:io.TextIOWrapper):
    self.is_human = bool(readline(file))
    self.boat_grid = json.loads(readline(file))
    self.hit_grid = json.loads(readline(file))
