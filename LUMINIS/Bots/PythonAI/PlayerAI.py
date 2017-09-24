from PythonClientAPI.Game import PointUtils
from PythonClientAPI.Game.Entities import FriendlyUnit, EnemyUnit, Tile
from PythonClientAPI.Game.Enums import Direction, MoveType, MoveResult
from PythonClientAPI.Game.World import World
import numpy as np

class PlayerAI:

    def __init__(self):
        """
        Any instantiation code goes here
        """
        pass


    # Get the state surrounding a unit
    # State is defined by a 5 x 5 x 3 Matrix
    # 5 x 5 [0] is the 5 x 5 grid surrounding the unit, marking the territory
        # -2 for enemy permanent territory
        # -1 for enemy temporary territory
        #  0 for neutral territory
        #  1 for friend temporary territory
        #  2 for friend permanent territory
        #  9 for Wall
    # 5 x 5 [1] marks the unit that lays on the grid
        # -1 for enemy unit
        #  0 for no unit
        #  1 for friendly unit
    # 5 x 5 [2] marks the existance of nests
        # -1 for enemy nest
        #  0 for no nest
        #  1 for friendly nest
    def get_state(self, world, unit, friendly_units, enemy_units):
        x, y = unit.position
        unit_state = np.zeros((5,5,3))

        # keys - cordinates
        # values - health
        friendly_health_dict = {}
        enemy_health_dict = {}

        for friendly in friendly_units:
            friendly_health_dict[friendly.position] = friendly.health
        for enemy in enemy_units:
            enemy_health_dict[enemy.position] = enemy.health

        # list of cordinates
        friendly_cord = list(friendly_health_dict.keys())
        enemy_cord = list(enemy_health_dict.keys())

        # define nest cordinates
        list_of_friendly_nests = world.get_friendly_nest_positions()
        list_of_enemy_nests = world.get_enemy_nest_positions()
        # generate 5 by 5 position cordinates
        for i in range(-2,3):
            for j in range(-2,3):

                # defines the board cordinates
                n_x = x + i
                n_y = y + j

                # crossing left-right boder
                if n_x < 0:
                    n_x = 19 + n_x
                elif n_x > 18:
                    n_x = n_x - 19

                # crossing top-bottom border
                if n_y < 0:
                    n_y = 19 + n_y
                elif n_y > 18:
                    n_y = n_y - 19

                unit_state[i+2][j+2][0] = self.assign_tile_value(world, tuple((n_x, n_y)))
                
                # checks for whether tile has friendly/enemy unit
                for f_cord in friendly_cord:
                    f_x, f_y = f_cord
                    if f_x == n_x and f_y == n_y:
                        # set as health value of that unit
                        unit_state[i+2][j+2][1] = friendly_health_dict[f_cord]

                for e_cord in enemy_cord:
                    e_x, e_y = e_cord
                    if e_x == n_x and e_y == n_y:
                        unit_state[i+2][j+2][1] = -1 * enemy_health_dict[e_cord]

                # checks for nest locations
                for fn_cord in list_of_friendly_nests:
                    fn_x, fn_y = fn_cord
                    if fn_x == n_x and fn_y == n_y:
                        unit_state[i+2][j+2][2] = 1

                for en_cord in list_of_enemy_nests:
                    en_x, en_y = en_cord
                    if en_x == n_x and en_y == n_y:
                        unit_state[i+2][j+2][2] = -1

        return unit_state

    def assign_tile_value(self, world, position):
        c_tile = world.get_tile_at(position)
        tile_value = 0

        if c_tile.is_enemy():
            if c_tile.is_permanently_owned():
                tile_value = -2
            else:
                tile_value = -1
        elif c_tile.is_friendly():
            if c_tile.is_permanently_owned():
                tile_value = 2
            else:
                tile_value = 1

        elif not c_tile.is_neutral():
            tile_value = -9
            print(position, end=" ")

        return tile_value

    def do_move(self, world, friendly_units, enemy_units):
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

        for unit in friendly_units:
            state = self.get_state(world, unit, friendly_units, enemy_units)
            print(unit.uuid)
            print("Base Board")
            print(state[:,:,0])
            print("Unit Board")
            print(state[:,:,1])
            print("Nest Board")
            print(state[:,:,2])
            path = world.get_shortest_path(unit.position,
                                           world.get_closest_capturable_tile_from(unit.position, None).position,
                                           None)
            if path: world.move(unit, path[0])
        print()