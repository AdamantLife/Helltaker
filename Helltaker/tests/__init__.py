## Test Utility
import unittest
## Test Target
from Helltaker import Coordinate, Map, Character, GameplaySequence, StandardRules, DestroyTerminalsRules
## Additional Tests
## It would be more appropriate to use a TestRunner, but
## the size of this module makes that seem like overkill
from Helltaker.tests.test_run import TestRun
from Helltaker.tests.test_gameplay import TestGameplay

## Builtin
from copy import deepcopy

TESTGRID = [
[" ", "T", "K"],
["B", " ", "S"],
["p", "C", "P"]
        ]

class MapInitTestCase(unittest.TestCase):
    """ Tests initialization of the Map class"""

    def test_gridsize_0(self) -> None:
        """ Grids must have a nonzero height and width """
        self.assertRaisesRegex(AttributeError,"Grid must have rows", Map , [])
        self.assertRaisesRegex(ValueError,"Grid rows must have columns", Map, [[]])
    
    def test_gridsize_mismatch(self) -> None:
        """ Grids must have all rows of the same length """
        self.assertRaisesRegex(ValueError, "Grid has rows with differing lengths", Map, [[" "],[" ","C"]])

    def test_character_count(self) -> None:
        self.assertRaisesRegex(ValueError, "Grid must have exactly 1 Character", Map, [[""]])
        self.assertRaisesRegex(ValueError, "Grid must have exactly 1 Character", Map, [["C","C"]])
        self.assertRaisesRegex(ValueError, "Grid must have exactly 1 Character", Map, [["C"],["C"]])

class MapTestCase(unittest.TestCase):
    """ Tests general Map functionality """
    def setUp(self) -> None:
        self.map = Map(deepcopy(TESTGRID))
        self.character = Character((1,2), 100)
        return super().setUp()

    def test_size(self):
        """ Tests that the map returns the correct width and height """
        self.assertEqual(self.map.width, 3)
        self.assertEqual(self.map.height, 3)
    
    def test_isblocking(self):
        """ Tests that Map.isblocking functions correctly """


    def test_capcoord_nomodification(self):
        """ Tests that capcoord returns valid cooridinates """
        for coord in [(0,0),(1,1),(2,2),(0,2),(2,0)]:
            with self.subTest(coord = coord):
                self.assertEqual(coord, self.map.capcoord(coord))

    def test_capcoord_invalid(self):
        """ Tests that capcord returns None for invalid coordinates """
        for coord in [(-1,0), (0,-1), (3,0), (0,3), (3,3),(-1,-1)]:
            with self.subTest(coord=coord):
                self.assertEqual(None, self.map.capcoord(coord))

    def test_capcord_character(self):
        """ Ensures that capcoord interfaces with character.coord correctly """
        self.assertEqual(self.character.coord, self.map.capcoord(self.character.coord))

    def test_getadjacent(self):
        """ Tests that the map correctly returns squares adjacent to the character """
        for characoord, expected in [
            ( (1,2), ( (1,1), (2,2), None, (0,2) ) ),
            ( (1,1), ( (1,0), (2,1) , (1,2), (0,1) ) ),
            ( (0,0), ( None, (1,0) , (0,1), None ) ),
            ]:
            with self.subTest(characoord = characoord, expected = expected):
                self.map.moveentity("C", self.character.coord, characoord)
                self.character.coord = characoord
                self.assertEqual(self.map.getadjacent(self.character.coord), [Coordinate(*coord) if coord else coord for coord in expected])

    def test_cleangrid(self):
        """ Tests the functionality of Map.cleangrid """
        grid = [
            [ " ", "C "],
            [ "pB", ""]
            ]
        expected = [
            ["", "C"],
            ["Bp", ""]
        ]
        self.assertEqual(Map.cleangrid(grid), expected)

    def test_opposingcoord(self):
        """ Tests the functionality of Map.opposingcoord"""
        for coorda, coordb, coordc in [
            ( (2,0), (1,0), (0,0) ),
            ( (0,0), (0,1), (0,2) ),
            ( (1,1), (2,1), (3,1) ),
            ( (1,0), (0,0), (-1,0) )
            ]:
            with self.subTest(coorda = coorda, coordb = coordb, coordc = coordc):
                self.assertEqual(Map.opposingcoord(coorda, coordb), coordc)

    def test_opposingcoord_invalid_notadjacent(self):
        """ Tests that Map.opposingcoord throws errors on non-adjacent coords """
        for coorda, coordb in [
            ( (0,0), (1,1) ),
            ( (0,1), (0,4) ),
            ]:
            with self.subTest(coorda = coorda, coordb = coordb):
                self.assertRaises(ValueError, Map.opposingcoord, coorda, coordb)

    def test_direction_to_coord(self):
        """ Tests the direction_to_coord function """
        for relative, direction, result in [
            ( (0,0), "right", (1,0) ),
            ( (1,1), "down", (1,2) ),
            ( (0,0), "left", (-1,0) ),
            ( (0,0), "up", (0,-1) ),
            ]:
            with self.subTest(relative = relative, direction = direction, result = result):
                self.assertEqual(Map.direction_to_coord(direction, relative), Coordinate(*result))

    def test_coord_to_direction(self):
        """ Tests the coord_to_direction function """
        for relative, coord, result in [
            ( (0,0), (0,1), "down"),
            ( (5,4), (5,5), "down"),
            ( (0,0), (1,1), None),
            ( (0,0), (0,-1), "up"),
            ( (0,0), (0,2), None),
            ]:
            with self.subTest(relative=relative, coord = coord, result = result):
                self.assertEqual(Map.coord_to_direction(coord, relative), result)

    def test_eq(self):
        """ Tests the __eq__ comparitor of Map """
        ## test for map with entities in a different order
        misordered = Map([["P"],["C"]])
        misordered.moveentity("C", (0,1),(0,0)) ## This will result in (0,0) = "PC"
        for mapa, mapb, result in [
            (self.map, Map(TESTGRID), True),
            (self.map, Map([["C"],[""]]), False),
            (Map([["C"],[""]]), Map([["C"],[""]]), True),
            (Map([["CP"], [""]]), misordered, True) ## Tests that (0,0)'s "CP" == "PC"
            ]:
            with self.subTest(mapa = mapa, mapb = mapb, result = result):
                self.assertEqual(mapa == mapb, result)

    def test_iter(self):
        """ Tests the __iter__ function of Map """
        expected = [(0,0), (1,0), (2,0), (0,1), (1,1), (2,1), (0,2), (1,2), (2,2)]
        for coord, expect in zip(self.map, expected):
            with self.subTest(coord = coord, expect = expect):
                self.assertEqual(coord, Coordinate(*expect))

    def test_iskickable_invalid(self):
        """ Tests that invalid coords are not kickable """
        self.assertFalse(self.map.iskickable((-1,-1)))

    def test_nearest_entity(self):
        """ Tests the functionality of Map.nearest_entity """
        GRID = [
            [" "," ","T"," ", "T"],
            ["T"," "," "," ", " "],
            [" "," "," "," ", " "],
            [" "," "," "," ", " "],
            [" "," ","C"," ", " "],
            ]
        MAP = Map(GRID)
        for start, expected in [
            ((2,4), (2,0) ),
            ( (0,4), (0,1) ),
            ( (4,1), (4,0) ),
            ]:
            with self.subTest(start = start, expected = expected):
                self.assertEqual(MAP.nearest_entity(start, "T"), Coordinate(*expected))
    
    def test_distance_to_coord(self):
        """ Tests the functionality of Map.distance_to_coord """
        for start, target, expected in [
            ( (0,0), (0,0), 0 ),
            ( (0,0), (0,1), 1 ),
            ( (0,0), (1,0), 1 ),
            ( (1,1), (0,0), 2 ),
            ( (5,2), (1,6), 8 ),
            ( (-2,-1), (0,0), 3 ),
            ]:
            with self.subTest(start = start, target = target, expected = expected):
                self.assertEqual(Map.distance_to_coord(start, target), expected)

    def test_parsegridstring(self):
        """ Tests the parsegridstring """
        MAP1 = "C" ## One Cell
        MAP2 = "T, , ,C" ## One Row
        MAP3 = " ,T, \nB,B,B\nC, , " ## Square Grid
        MAP4 = "T,S,,\n,P,,S\n ,C,B," ## No Spaces including trailing commas
        MAP5 = "T\r\nC" ## Carriage/Newline Return
        MAP6 = "\n\n\n" ## Only New lines

        S1 = [
            ["C"]
        ]
        S2 = [
            ["T", " ", " ", "C"]
        ]
        S3 = [
            [" ","T"," "],
            ["B","B","B"],
            ["C"," ", " "]
        ]
        S4 = [
            ["T","S"," "," "],
            [" ","P"," ","S"],
            [" ","C","B"," "]
        ]
        S5 = [
            ["T"],
            ["C"]
        ]
        S6 = [
            [" "],
            [" "],
            [" "]
            ]

        for grid, expected in [
            (MAP1, S1),
            (MAP2, S2),
            (MAP3, S3),
            (MAP4, S4),
            (MAP5, S5),
            (MAP6, S6)
            ]:
            with self.subTest(grid = grid, expected = expected):
                self.assertEqual(Map.cleangrid(Map.parsegridstring(grid)), Map.cleangrid(expected))

    def test_generatelaser(self):
        """ Tests to ensure the generatelaser function returns correct lists """
        MAP1 = "2\nT\nS\nC" ## Laser goes through non-solid and stops at wall
        MAP2 = "1,,B,TC" ## Laser Stops at Block
        MAP3 = ",0,\n,,\n,C," ## No return because laser is firing up into wall
        MAP4 = "1,1,C," ## Lasers pass through other lasers
        L1 = (0,0)
        L2 = (0,0)
        L3 = (1,0)
        L4 = (0,0)
        S1 = [(0,1),(0,2),(0,3)]
        S2 = [(1,0),]
        S3 = []
        S4 = [(1,0), (2,0), (3,0)]
        for grid, laser, expected in [
            (MAP1, L1, S1),
            (MAP2, L2, S2),
            (MAP3, L3, S3),
            (MAP4, L4, S4),
            ]:
            with self.subTest(grid=grid, laser = laser, expected= expected):
                _map = Map(Map.parsegridstring(grid))
                self.assertEqual(_map.generatelaser(laser), [Coordinate(*c) for c in expected])

            

class MapActionsTestCase(unittest.TestCase):
    """ Tests Map Actions (move, kick) """
    def setUp(self) -> None:
        self.map = Map(deepcopy(TESTGRID))
        self.character = Character((1,2), 100)
        return super().setUp()

    def test_moveentity_open(self):
        """ Tests that the map can move entities to open squares """
        start = (1,2)
        for target in [(0,0), (1,1)]:
            with self.subTest(target = target):
                self.map.moveentity("C", start, target)
                try:
                    self.assertTrue(self.map.coordcontains(target, "C"))
                    self.assertFalse(self.map.coordcontains(start, "C"))
                finally:
                    start = target

    def test_moveentity_nonblocking(self):
        """ Tests that the map can move entities to squares with Nonblocking Entities """
        start = (1,2)
        for target in [ (1, 0) , (2,0), (0,2), (2,2) ]:
            with self.subTest(target = target):
                self.map.moveentity("C", start, target)
                try:
                    self.assertTrue(self.map.coordcontains(target, "C"))
                    self.assertFalse(self.map.coordcontains(start, "C"))
                finally: 
                    start = target
    
    def test_moveentity_direction(self):
        """ Tests that movecharacter can accept a direction word as its target """
        self.assertEqual(self.map.moveentity("C", (1,2), "up"), (1,1))

    def test_movecharacter_invalid_occupied(self):
        """ Tests that character cannot be moved to occupied square (including it's current square) """
        start = (1,2)
        for target in [ (0, 1), (2, 1), (1,2)]:
            with self.subTest(target = target):
                self.assertIsNone(self.map.moveentity("C", start, target))

    def test_moveentity_invalid_outside(self):
        """ Tests that character cannot be moved outside the map """
        start = (1,2)
        for target in [ (-1,0), (0, -1), (3, 0), (0, 3), (1, -1), (3, 1)]:
            with self.subTest(target = target):
                self.assertIsNone(self.map.moveentity("C", start, target))

    def test_removeentity(self):
        """ Tests that the map can remove the entity from the given coordinate """
        for (coord, entity) in [
            ( (0,1), "B"),
            ( (2,1), "S"),
            ( (1,2), "C")
            ]:
            with self.subTest(coord = coord, entity = entity):
                self.map.removeentity(entity, coord)
                self.assertFalse(self.map.coordcontains(coord, entity))

    def test_removeentity_invalidcoord(self):
        """ Tests that removeentity fails on invalid coordinates """
        for coord in [ (-1,0), (-1,-1), (3, 0), (0, 3)]:
            with self.subTest(coord = coord):
                self.assertRaises(AttributeError, self.map.removeentity, "S", coord)
        
    def test_removeentity_mismatch(self):
        """ Tests that removeentity fails on invalid coordinates or coordinate-entity mismatch """
        for (coord, entity) in [
            ( (0,0), "C"),
            ( (1,1), "T"),
            ( (2,2), "p")
            ]:
            with self.subTest(coord = coord, entity = entity):
                self.assertRaises(ValueError, self.map.removeentity, entity, coord)
    
    def test_kick_empty(self):
        """ Tests that Kickable Entities can be kicked into empty squares """
        for entity, start, target in [
            ( "B", (0,1), (0,0) ),
            ( "S", (2,1), (1,1) )
            ]:
            with self.subTest(entity=entity, start = start, target = target):
                result = self.map.kick(entity, start, target)
                self.assertIsNotNone(result)
                self.assertEqual(result, target)
                self.assertTrue(self.map.coordcontains(target, entity))
                self.assertFalse(self.map.coordcontains(start,entity))

    def test_kick_nonblocking(self):
        """ Tests that Kickable Entities can be kicked into nonblocking entities' squares """
        for entity, start, target in [
            ( "B", (0,1), (0,2) ),
            ( "S", (2,1), (2,0) )
            ]:
            with self.subTest(entity=entity, start = start, target = target):
                result = self.map.kick(entity, start, target)
                self.assertIsNotNone(result)
                self.assertEqual(result, target)
                self.assertTrue(self.map.coordcontains(target, entity))
                self.assertFalse(self.map.coordcontains(start,entity))

    def test_kick_nomove(self):
        """ Tests that kicking a Kickable Entity into a square that it cannot move to results in no changes """
        ## Moving Skeleton next to Block so Block can be kicked into it
        self.map.moveentity("S", (2,1), (1,1))
        for entity, start, target in [
            ( "B", (0,1), (-1,1) ), ## Block Left into Wall
            ( "B", (0,1), (1,1) ) ## Block Right into Skeleton
            ]:
            with self.subTest(entity=entity, start = start, target = target):
                result = self.map.kick(entity, start, target)
                self.assertEqual(result, start)
                self.assertTrue(self.map.coordcontains(start, entity))
                try: self.assertFalse(self.map.coordcontains(target,entity))
                except ValueError: pass ## Target was off the map

    def test_kick_destroy(self):
        """ Tests that destroyables kicked into Blocking Entities, Walls, or the Edge of the Map are destroyed """
        result = self.map.kick("S", (2,1), (3,1)) ## Kick Skeleton Right into Wall
        self.assertIsNone(result)
        self.assertFalse(self.map.coordcontains((2,1),"S")) ## Skeleton has been destroyed

        self.map.createentity("S", (1,1)) ## Create new skeleton in center square
        result = self.map.kick("S", (1,1), (0,1)) ## Kick Skeleton Left into Block
        self.assertIsNone(result)
        self.assertFalse(self.map.coordcontains((1,1), "S")) ## Skeleton has been destroyed

    def test_kick_invalid_entitymismatch(self):
        """ Tests that providing the wrong Coordinate/Entity combination results in a ValueError """
        for entity, start, target in [
            ( "S", (1,1), (2,1) ),
            ( "B", (1,1), (2,1) ),
            ( "B", (2,1), (1,1) ),
            ]:
            with self.subTest(entity = entity, start = start, target = target):
                self.assertRaises(ValueError, self.map.kick, entity, start, target)

    def test_cyclespikes(self):
        """ Tests that cyclespikes cycles the spikes """
        self.map.cyclespikes()
        self.assertTrue(self.map.coordcontains((0,2),"P"))
        self.assertTrue(self.map.coordcontains((2,2),"p"))
    
    def test_spikeskeletons(self):
        """ Tests that spikeskeletons functions as expected """
        _map = Map([
            ["SP"],
            ["Sp"],
            ["SP"],
            ["C"]
        ])
        _map.spikeskeletons()
        self.assertFalse(_map.coordcontains((0,0), "S"))
        self.assertFalse(_map.coordcontains((0,2), "S"))
        self.assertTrue(_map.coordcontains((0,1), "S"))
        _map.cyclespikes()
        _map.spikeskeletons()
        self.assertFalse(_map.coordcontains((0,1), "S"))


class CharacterTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.map = Map(deepcopy(TESTGRID))
        self.character = Character((1,2), 100)
        return super().setUp()

    def test_move(self):
        """ Checks the results of character movement.
        
            Movement is mostly tested under MapActionsTestCase, but character.move has a few addendums.
        """
        for start, target, result in [
            ( (1,2), (1,1), (1,1) ), ## Move forward into open square
            ( (1,1), (0,1), (1,1) ), ## Move left into block- is technically a kick action
            ( (1,1), (2,1), (1,1) ), ## Move right into Skeleton- is technically a kick action which destroys the skeleton
            ]:
            with self.subTest(start = start, target = target, result = result):
                self.map = Map(deepcopy(TESTGRID))
                self.map.removeentity("C",(1,2))
                self.character = Character(start, 100)
                self.map.createentity("C", self.character.coord)
                self.assertEqual(self.character.move(target, _map = self.map), result)

    def test_move_kick(self):
        """ Checks the results of the character kicking an object during a move action. """
        ## Getting character into position
        self.character.move((1,1), _map = self.map)
        ## Moving left should kick block at (0,1)
        ## The result should be (1,1) instead of None and the entities should remain where they are
        self.assertEqual(self.character.move((0,1), _map = self.map), (1,1))
        self.assertEqual(self.map.getentities((0,1)), "B")
        self.assertEqual(self.map.getentities((1,1)), "C")
        ## Moving right should kick Skeleton at (2,1), destroying it
        ## The result should be (1,1) instead of None and Skeleton should be removed from (2,1) while Character remains where it is
        self.assertEqual(self.character.move((2,1), _map = self.map), (1,1))
        self.assertEqual(self.map.getentities((2,1)), "")
        self.assertEqual(self.map.getentities((1,1)), "C")

    def test_move_direction(self):
        """ Checks that character.move translates directions. """
        ## This should never fail because this is a valid move and therefore returns from _map.move with a coordinate
        ## (assuming that _map.move internally translates the direction correctly)
        self.character.move("up", _map = self.map)
        ## This may fail because _map.move returns None, and character.move will try to kick instead
        ## (failing to do so if target has not be translated by character.move)
        self.character.move("left", _map = self.map)

    def test_pickup_key(self):
        """ Tests that the character picks up keys he moves over. """
        MAP = [
            ["G"],
            ["G"],
            ["K"],
            ["C"]
            ]
        _map = Map(MAP)
        character = Character((0,3), 3, _map = _map)
        self.assertFalse(character.haskey)
        self.assertTrue(_map.coordcontains((0,2), "K"))
        character.move("up")
        self.assertTrue(character.haskey)
        self.assertFalse(_map.coordcontains((0,2), "K"))

    def test_cleargate(self):
        """ Tests taht the character clears gates he moves into if he has key"""
        MAP = [
            ["G"],
            ["G"],
            ["K"],
            ["C"]
            ]
        _map = Map(MAP)
        character = Character((0,3), 3, _map = _map)
        character.move("up")
        character.move("up")
        self.assertEqual(character.coord, (0,1))
        self.assertFalse(_map.coordcontains(character.coord, "G"))
        ## Testing that this no longer works if haskey is toggled off
        character.haskey = False
        character.move("up")
        ## Character has not moved
        self.assertEqual(character.coord, (0,1))
        self.assertTrue(_map.coordcontains((0,0), "G"))

    def test_destroyedstate_replacement(self):
        """ In EX Mode (Exam Mode) Terminals can be destroyed; instead of being removed from the map, they are replaced with a "Broken Terminal" entity """
        MAP = "E,C"
        _map = Map(MAP)
        character = Character((1,0), 100, _map = _map)
        ## Sanity Check
        self.assertTrue(_map.coordcontains((0,0), "E"))
        ## Character didn't move
        self.assertEqual(character.move("left"), Coordinate(1,0))
        ## Terminal is destroyed
        self.assertFalse(_map.coordcontains((0,0), "E"))
        self.assertTrue(_map.coordcontains((0,0), "e"))
        ## Character hasn't moved
        self.assertEqual(character.coord, Coordinate(1,0))

        

class GameplaySequenceTestCase(unittest.TestCase):
    ## TODO: GameplaySequence Tests
    def test_doubledamage_on_last_action(self):
        """ Tests that getting hit by spikes when at 0 stamina doesn't cause any errors """
        MAP = [
            ["p"],
            ["C"]
        ]
        gameplay = GameplaySequence(MAP, willpower = 1)
        gameplay.up()
        ## Actions is ["UP",] which equals 2 actions
        self.assertEqual(gameplay.action_length(), 2)
        ## Willpower - action_length = -1
        self.assertEqual(gameplay.remaining_actions(),-1)
        ## gameplay raises RuntimeError on next action as expected
        self.assertRaises(RuntimeError, gameplay.down)

    def test_unwinnable(self):
        """ Basic tests for GameplaySequence.unwinnable """
        MAP = [
            ["C", " ", " ", "T"],
            ["B", " ", " ", "T"],
        ]
        gameplay = GameplaySequence(MAP, willpower = 4)
        self.assertFalse(gameplay.unwinnable())
        gameplay.down()
        self.assertFalse(gameplay.unwinnable())
        gameplay.down()
        self.assertTrue(gameplay.unwinnable())

    def test_laserdeath(self):
        """ Tests that lasers kill Characters """
        MAP = "C\n\n0" ## Laser firing directly upwards to character
        gameplay = GameplaySequence(MAP, 100)
        self.assertRaisesRegex(gameplay.GameOver, "Lasered!", gameplay.down)
        MAP = "1,,B,C,B" ## Laser firing into interposing block
        gameplay = GameplaySequence(MAP, 100)
        try:
            gameplay.right()
        except GameplaySequence.GameOver:
            self.fail(f"Laser penetrated Block to kill Character\n{gameplay.map}")
        try:
            gameplay.left()
        except GameplaySequence.GameOver:
            self.fail(f"Laser penetrated Block after it was kicked\n{gameplay.map}")
        MAP = ",,2,\n,B,,\nC,,," ## Simple puzzle where block is pushed to interrupt laser stream
        gameplay = GameplaySequence(MAP, 100)
        gameplay.right()
        ## Running into the laser beam without pushing block and dying
        self.assertRaisesRegex(GameplaySequence.GameOver, "Lasered!", gameplay.right)
        gameplay = GameplaySequence(MAP, 100)
        try:
            gameplay.up()
            gameplay.right()
            gameplay.down()
            gameplay.right()
            gameplay.right()
            gameplay.right()
        except GameplaySequence.GameOver:
            self.fail(f"Got Lasered while trying to solve puzzle\n{gameplay.map}")

class EXTestCase(unittest.TestCase):
    def test_victory(self):
        """ Tests that the victory condition triggers """
        grid = "C,B"
        gameplay = GameplaySequence(grid, 100, rulesets=[StandardRules, DestroyTerminalsRules])
        self.assertRaises(GameplaySequence.Victory, gameplay.right)

    def test_multipleterminals(self):
        """ Tests that the game only ends when after all Terminals are destroyed """
        grid = "E,E\nC,"
        gameplay = GameplaySequence(grid, 100, rulesets=[StandardRules, DestroyTerminalsRules])
        try:
            gameplay.up()
        except GameplaySequence.Victory:
            self.fail("Victory after destroying only one Terminal")
        gameplay.right()
        self.assertRaises(GameplaySequence.Victory, gameplay.up)

    def test_standardstillapplies(self):
        """ Sanity Check which tests that standard rules still apply """
        grid = "C,"
        gameplay = GameplaySequence(grid,0, rulesets= [StandardRules, DestroyTerminalsRules])
        self.assertRaises(GameplaySequence.GameOver, gameplay.right)

    def test_unwinnable(self):
        """ Tests DestroyTerminalsRules.unwinnable """
        grid = "C,"
        gameplay = GameplaySequence(grid,100, rulesets= [StandardRules, DestroyTerminalsRules])
        ## No Terminals to find
        self.assertRaises(ValueError, gameplay.unwinnable)

        ## Can't reach terminal
        grid = "C,,E"
        gameplay = GameplaySequence(grid,0, rulesets= [StandardRules, DestroyTerminalsRules])
        self.assertTrue(gameplay.unwinnable())

        
if __name__ == "__main__":
    unittest.main()