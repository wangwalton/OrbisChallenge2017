from PythonClientAPI.Game import PointUtils
from PythonClientAPI.Game.Entities import FriendlyUnit, EnemyUnit, Tile
from PythonClientAPI.Game.Enums import Direction, MoveType, MoveResult
from PythonClientAPI.Game.World import World
from PythonClientAPI.Game.PointUtils import *

class SmartDirection:
    def __init__(self):

        pass

    def get_tiles_around(self, point):
        tile_neighbours = {}
        if not self._position_to_tile_cache:
            self._create_position_to_tile_cache()
        neighbours = self.get_neighbours(point)
        for direction in neighbours:
            if mod_point(neighbours[direction]) in self._position_to_tile_cache:
                tile_neighbours[direction] = self._position_to_tile_cache[mod_point(neighbours[direction])]
        return tile_neighbours