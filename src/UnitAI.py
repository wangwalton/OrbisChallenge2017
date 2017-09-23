from PythonClientAPI.Game import PointUtils
from PythonClientAPI.Game.Entities import Unit
from PythonClientAPI.Game.Entities import FriendlyUnit, EnemyUnit, Tile
from PythonClientAPI.Game.Enums import Direction, MoveType, MoveResult
import PythonClientAPI.Game.Enums
from PythonClientAPI.Game.World import World
import operator
import random

# Point System
p_kill = 50;
p_die = -50;
p_nest = 40;
p_new_tile = 5;
p_enemy_territory = 10;
p_combine = 0;

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

        points = {}

        nextTiles = self.world.get_tiles_around(self.unit.position);
        for dir in nextTiles:
            # Enemy Tile
            newTile = nextTiles[dir];
            index = Direction.DIRECTION_TO_INDEX[dir]
            points[index] = 0

            enemyList = [enemy for enemy in self.enemy_units if enemy.position is newTile.position]
            if enemyList:
                if(enemyList[0].health > self.unit.health):
                    points[index] += p_kill
                else:
                    points[index] += p_die
            if newTile.is_enemy():
                points[index] += p_enemy_territory

            if newTile.is_friendly():
                points[index] += p_combine

            if newTile.is_neutral():
                points[index] += p_new_tile

            print(points[index]);

        maxval = points[max(points, key=points.get)]
        maxdirList = [pt for pt in points if points[pt] == maxval]
        maxdirchosen = random.randint(0, len(maxdirList)-1)


        newPosition = Direction.INDEX_TO_DIRECTION[maxdirList[maxdirchosen]].move_point(self.unit.position)
        self.world.move(self.unit, newPosition)

        # path = self.world.get_shortest_path(self.unit.position,
        #                                     self.world.get_closest_capturable_tile_from(self.unit.position, None).position,
        #                                None)
        # if path: self.world.move(self.unit, path[0])