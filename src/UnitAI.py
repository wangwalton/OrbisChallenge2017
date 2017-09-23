from PythonClientAPI.Game import PointUtils
from PythonClientAPI.Game.Entities import Unit
from PythonClientAPI.Game.Entities import FriendlyUnit, EnemyUnit, Tile
from PythonClientAPI.Game.Enums import Direction, MoveType, MoveResult
from PythonClientAPI.Game.World import World

# Point System
kill = 50;
nest = 40;
new_tile = 5;
combine = 30;

class UnitAI:
    def __init__(self, Unit, world, friendly_units, enemy_units):
        self.unit = Unit
        self.world = world
        self.friendly_units = friendly_units
        self.enemy_units = enemy_units

        pass

    def do_move(self):
        """
        This method will get called every turn.

        :param world: World object reflecting current game state
        :param friendly_units: list of FriendlyUnit objects
        :param enemy_units: list of EnemyUnit objects
        """
        # Fly away to freedom, daring fireflies
        # Build thou nests
        # Grow, become stronger
        # Take over the world

        points = 0;

        for dir in Direction.ORDERED_DIRECTIONS:
            unit.position



        path = self.world.get_shortest_path(self.unit.position,
                                            self.world.get_closest_capturable_tile_from(self.unit.position, None).position,
                                       None)
        if path: self.world.move(self.unit, path[0])