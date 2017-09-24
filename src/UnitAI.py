from PythonClientAPI.Game import PointUtils
from PythonClientAPI.Game.Entities import Unit
from PythonClientAPI.Game.Entities import FriendlyUnit, EnemyUnit, Tile
from PythonClientAPI.Game.Enums import Direction, MoveType, MoveResult
from PythonClientAPI.Game.PointUtils import *
from PythonClientAPI.Game.PlayerAPI import PlayerAPI
import PythonClientAPI.Game.Enums
from PythonClientAPI.Game.World import World
import operator
import random

# Point System
p_grow = 0;
p_kill = 200;
p_die = -50;
p_nest = 300;
p_destroynest = -200;
p_destroyenemynest = 1000;
p_new_tile = 50;
p_enemy_territory = 100;
p_combine = -20;
p_adjacentfriendly = -50;

class UnitAI:
    def __init__(self, Unit, world, friendly_units, enemy_units, scoreMap):
        self.unit = Unit
        self.world = world
        self.friendly_units = friendly_units
        self.enemy_units = enemy_units
        self.scoreMap = scoreMap
        self.mapsize = (world.get_width(), world.get_height())
        pass

    def do_move(self):

        points = {}

        nextTiles = self.world.get_tiles_around(self.unit.position);
        for dir in nextTiles:

            newTile = nextTiles[dir];
            index = Direction.DIRECTION_TO_INDEX[dir]
            points[index] = 0

            # Blocked Tile
            if (self.world.is_wall(newTile.position)):
                continue

            # Late Game - Choose to Grow instead of move
            if newTile.position is self.unit.position:
                points[index] += p_grow

            else:
                # Enemy or Friend Tile
                if newTile.position in self.scoreMap.enemy_hash:
                    enemy = self.scoreMap.enemy_hash[newTile.position]
                    if(enemy.health >= self.unit.health):
                        points[index] += p_kill
                    else:
                        points[index] += p_die

                if newTile.position in self.scoreMap.friendly_hash:
                    points[index] += p_combine

                if newTile.position in self.scoreMap.adjacentfriendlyhash:
                    points[index] += p_adjacentfriendly

                # Open Tiles
                if not newTile.is_permanently_owned():
                    if newTile.is_enemy():
                        points[index] += p_enemy_territory

                    if newTile.is_neutral():
                        points[index] += p_new_tile

                # Destruction of Positions that can have nests
                if newTile.position in self.scoreMap.nestScores:
                    points[index] += p_destroynest

                # Creation of Nests
                if newTile.position in self.scoreMap.newNestScores:
                    points[index] += p_nest

                # Destruction of Enemy Nests
                if newTile.position in self.scoreMap.enemy_nest_hash:
                    points[index] += p_destroyenemynest

                # General Direction
                points[index] += self.scoreMap.position_values[newTile.position] * 5


        maxval = points[max(points, key=points.get)]
        maxdirList = [pt for pt in points if points[pt] == maxval]
        maxdirchosen = random.randint(0, len(maxdirList)-1)


        newPosition = Direction.INDEX_TO_DIRECTION[maxdirList[maxdirchosen]].move_point(self.unit.position)
        self.world.move(self.unit, newPosition)

        # path = self.world.get_shortest_path(self.unit.position,
        #                                     self.world.get_closest_capturable_tile_from(self.unit.position, None).position,
        #                                None)
        # if path: self.world.move(self.unit, path[0])