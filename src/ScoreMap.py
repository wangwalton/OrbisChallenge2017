from PythonClientAPI.Game import PointUtils
from PythonClientAPI.Game.Entities import Unit
from PythonClientAPI.Game.Entities import FriendlyUnit, EnemyUnit, Tile
from PythonClientAPI.Game.Enums import Direction, MoveType, MoveResult
import PythonClientAPI.Game.Enums
from PythonClientAPI.Game.PointUtils import *
from PythonClientAPI.Game.World import World
import operator

class ScoreMap:
    def __init__(self, world, friendly_units, enemy_units):
        self.world = world
        self.friendly_units = friendly_units
        self.enemy_units = enemy_units

        self.get_enemy_hash()
        self.get_friendly_hash()
        self.get_adjacentfriendly_hash()
        self.get_blocked_hash()
        self.find_pathfindingavoidset()

        self.find_nest_scores()
        self.find_enemy_nest_scores()
        self.evaluate_positional_scores()

    def find_nest_scores(self):
        self.nestScores = {} # Dictionary of Nest Scores
        self.doubleNestScores = {}
        self.tripleNestScores = {}
        self.newNestScores = {} # Dictionary of places which create a nest

        for pos in self.world.get_friendly_tiles():
            neighbours = self.world.get_tiles_around(pos.position)
            for n in neighbours:
                if neighbours[n].position not in self.nestScores:
                    self.nestScores[neighbours[n].position] = 1
                else:
                    self.nestScores[neighbours[n].position] += 1

        for pos in self.blocked_hash:
            neighbours = self.world.get_tiles_around(pos)
            for n in neighbours:
                if neighbours[n].position not in self.nestScores:
                    self.nestScores[neighbours[n].position] = 1
                else:
                    self.nestScores[neighbours[n].position] += 1

        for pos in self.world.get_friendly_tiles():
            if pos.position in self.nestScores:
                self.nestScores.pop(pos.position)

        for pos in self.blocked_hash:
            if pos in self.nestScores:
                self.nestScores.pop(pos)

        for pos in list(self.nestScores):
            if self.nestScores[pos] <= 2:
                self.nestScores.pop(pos)
                continue

        # for pos in self.nestScores:
        #     print(pos)

        for pos in self.world.get_neutral_tiles():
            neighbours = self.world.get_tiles_around(pos.position)
            for n in neighbours:
                if neighbours[n].position in self.nestScores:
                    if pos.position not in self.newNestScores:
                        self.newNestScores[pos.position] = 0;
                    self.newNestScores[pos.position] += self.nestScores[neighbours[n].position]

        for pos in self.world.get_enemy_tiles():
            neighbours = self.world.get_tiles_around(pos.position)
            for n in neighbours:
                if neighbours[n].position in self.nestScores:
                    if pos.position not in self.newNestScores:
                        self.newNestScores[pos.position] = 0;
                    self.newNestScores[pos.position] += self.nestScores[neighbours[n].position]

        # Double and Triple Nests
        for pos in self.newNestScores:
            if self.newNestScores[pos] == 6:
                self.doubleNestScores[pos] = self.newNestScores[pos]
                # print('Double ', self.newNestScores[pos])
            elif self.newNestScores[pos] > 8:
                self.tripleNestScores[pos] = self.newNestScores[pos]
                # print('Triple ', self.newNestScores[pos])

        # for pos in self.newNestScores:
        #     if self.newNestScores[pos] == 3:
        #         print(pos)

    def find_enemy_nest_scores(self):
        self.enemy_nest_hash = {}

        for pos in self.world.get_enemy_nest_positions():
            neighbours = self.world.get_tiles_around(pos)
            for n in neighbours:
                if neighbours[n].position not in self.enemy_nest_hash:
                    self.enemy_nest_hash[neighbours[n].position] = pos

    def get_enemy_hash(self):
        self.enemy_hash = {}

        for enemy in self.enemy_units:
            self.enemy_hash[enemy.position] = enemy

    def get_friendly_hash(self):
        self.friendly_hash = {}

        for friend in self.friendly_units:
            self.friendly_hash[friend.position] = friend

    def get_adjacentfriendly_hash(self):
        self.adjacentfriendlyhash = {}

        for friend in self.friendly_units:
            neighbours = self.world.get_tiles_around(friend.position)
            for n in neighbours:
                if neighbours[n].position not in self.adjacentfriendlyhash:
                    self.adjacentfriendlyhash[neighbours[n].position] = friend.position

    def get_blocked_hash(self):
        self.blocked_hash = {}

        empty_tiles = set()
        for tile in self.world.get_tiles():
            empty_tiles.add(tile.position)

        for i in range(0, self.world.get_width()):
            for j in range(0, self.world.get_height()):
                if (i, j) not in empty_tiles:
                    self.blocked_hash[(i, j)] = 0

    def find_pathfindingavoidset(self):
        self.pathfindingavoid = set(self.blocked_hash.keys())

        for pos in self.world.get_friendly_nest_positions():
            self.pathfindingavoid.add(pos)

        for pos in self.world.get_enemy_nest_positions():
            self.pathfindingavoid.add(pos)

    def evaluate_positional_scores(self):
        # Proximity to the 2-walls increases the score
        # Proximity to enemy nest
        self.position_values = {}
        self.new_value = {}
        tiles = self.world.get_tiles()
        for tile in tiles:
            self.position_values[tile.position] = 0
            self.new_value[tile.position] = 0

        # Add the triple nests
        for pos in self.newNestScores:
            self.position_values[pos] = 10

        for pos in self.doubleNestScores:
            self.position_values[pos] = 50

        for pos in self.tripleNestScores:
            self.position_values[pos] = 999
            print (pos)

        for pos in self.enemy_hash:
            self.position_values[pos] = 10

        for pos in self.enemy_nest_hash:
            self.position_values[pos] = 99

        # Loop through all the positions, get the taxicab distances

        for i in range(1,4):
            for pos in self.position_values:

                orig_temp = self.position_values[pos]
                self.new_value[pos] = 0.5 * self.position_values[pos];

                if (self.world.is_wall(mod_point(Direction.NORTH.move_point(pos), (19,19)))):
                    self.new_value[pos] += 0.125 * orig_temp
                else:
                    self.new_value[pos] += 0.125 * self.position_values[mod_point(Direction.NORTH.move_point(pos), (19,19))]

                if (self.world.is_wall(mod_point(Direction.SOUTH.move_point(pos), (19,19)))):
                    self.new_value[pos] += 0.125 * orig_temp
                else:
                    self.new_value[pos] += 0.125 * self.position_values[mod_point(Direction.SOUTH.move_point(pos), (19,19))]

                if (self.world.is_wall(mod_point(Direction.EAST.move_point(pos), (19,19)))):
                    self.new_value[pos] += 0.125 * orig_temp
                else:
                    self.new_value[pos] += 0.125 * self.position_values[mod_point(Direction.EAST.move_point(pos), (19,19))]

                if (self.world.is_wall(mod_point(Direction.WEST.move_point(pos), (19,19)))):
                    self.new_value[pos] += 0.125 * orig_temp
                else:
                    self.new_value[pos] += 0.125 * self.position_values[mod_point(Direction.WEST.move_point(pos), (19,19))]

            for pos in self.position_values:
                self.position_values[pos] = self.new_value[pos]

        # for j in range(0, 18):
        #     for i in range(0, 18):
        #         if((i,j) in self.position_values):
        #             print("%.2f" % self.position_values[(i,j)], "         ", end='')
        #         else:
        #             print('X             ', end='')
        #     print()


