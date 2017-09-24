from PythonClientAPI.Game import PointUtils
from PythonClientAPI.Game.Entities import Unit
from PythonClientAPI.Game.Entities import FriendlyUnit, EnemyUnit, Tile
from PythonClientAPI.Game.Enums import Direction, MoveType, MoveResult
from PythonClientAPI.Game.PlayerAPI import PlayerAPI
import PythonClientAPI.Game.Enums
from PythonClientAPI.Game.World import World
import operator
import random
from UnitAI import UnitAI

# Point System
p_kill = 200;
p_far_nest = 300;
p_destroyenemynest = 1000;

class AttackerUnitAI(UnitAI):
    def __init__(self, Unit, world, friendly_units, enemy_units, scoreMap):
        UnitAI.__init__(self, Unit, world, friendly_units, enemy_units, scoreMap)
        pass

    def do_move(self):

        distToPosition = {}

        # Evaluate locations with enemy nests
        closest_enemy_nest_position = self.world.get_closest_enemy_nest_from(self.unit.position, None)
        distToPosition[closest_enemy_nest_position] = self.world.get_shortest_path_distance(self.unit.position, closest_enemy_nest_position)

        if(closest_enemy_nest_position in self.scoreMap.pathfindingavoid):
            self.scoreMap.pathfindingavoid.remove(closest_enemy_nest_position)

        # for p in self.scoreMap.pathfindingavoid:
        #     print (p)
        # print(closest_enemy_nest_position)

        path = self.world.get_shortest_path(self.unit.position, closest_enemy_nest_position, self.scoreMap.pathfindingavoid)
        self.world.move(self.unit, path[0])
