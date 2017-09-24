from PythonClientAPI.Game import PointUtils
from PythonClientAPI.Game.Entities import FriendlyUnit, EnemyUnit, Tile
from PythonClientAPI.Game.Enums import Direction, MoveType, MoveResult
from PythonClientAPI.Game.World import World
import numpy as np
from UnitAI import UnitAI
from AttackerUnitAI import AttackerUnitAI
from ScoreMap import ScoreMap
import random

powerfulUnitThreshold = 4

class PlayerAI:
    def __init__(self):
        """
        List of AI Units in the game
        """
        self.friendlyAI = set()
        self.enemyAI = set()

        pass

    def do_move(self, world, friendly_units, enemy_units):
        """
        This method will get called every turn.
        
        :param world: World object reflecting current game state
        :param friendly_units: list of FriendlyUnit objects
        :param enemy_units: list of EnemyUnit objects
        """

        # Update the world
        self.ScoreMap = ScoreMap(world, friendly_units, enemy_units)


        # Update any new fireflies
        self.friendlyAI = set();
        for unit in friendly_units:
            if unit.health > powerfulUnitThreshold:
                newAI = AttackerUnitAI(unit, world, friendly_units, enemy_units, self.ScoreMap)
            else:
                newAI = UnitAI(unit, world, friendly_units, enemy_units, self.ScoreMap)
            self.friendlyAI.add(newAI);

        for unitAI in self.friendlyAI:
            unitAI.do_move()


