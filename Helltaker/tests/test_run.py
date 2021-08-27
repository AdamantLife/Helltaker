## Test Utility
import unittest
## Test Target
from Helltaker import Map, Character

MAP_IV = [
        ["C",   "W",    "K",    "",     "B",    "W",    "W",    "W" ],
        ["",    "B",    "P",    "PB",   "",     "G",    "",     "W" ],
        ["B",   "",     "B",    "",     "B",    "B",    "T",    ""  ],
        ["",    "B",    "",     "B",    "",     "B",    "B",    "T"  ],
        ["W",   "",     "B",    "",     "B",    "",     "W",    "W" ],
        ]

class TestRun(unittest.TestCase):
    def test(self):
        """ Does a complete runthrough of Chapter IV, checking that the Game/Map state is exactly as it should be after each action. """
        _map = Map(MAP_IV)
        character = Character((0,0), 23, _map = _map)

        character.move("down")
        expected = Map([
        ["",   "W",    "K",    "",     "B",    "W",    "W",    "W" ],
        ["C",    "B",    "P",    "PB",   "",     "G",    "",     "W" ],
        ["B",   "",     "B",    "",     "B",    "B",    "T",    ""  ],
        ["",    "B",    "",     "B",    "",     "B",    "B",    "T"  ],
        ["W",   "",     "B",    "",     "B",    "",     "W",    "W" ],
        ])
        self.assertEqual(_map, expected)

        character.move("down")
        expected = Map([
        ["",   "W",    "K",    "",     "B",    "W",    "W",    "W" ],
        ["C",    "B",    "P",    "PB",   "",     "G",    "",     "W" ],
        ["",   "",     "B",    "",     "B",    "B",    "T",    ""  ],
        ["B",    "B",    "",     "B",    "",     "B",    "B",    "T"  ],
        ["W",   "",     "B",    "",     "B",    "",     "W",    "W" ],
        ])
        self.assertEqual(_map, expected)

        character.move("down")
        expected = Map([
        ["",   "W",    "K",    "",     "B",    "W",    "W",    "W" ],
        ["",    "B",    "P",    "PB",   "",     "G",    "",     "W" ],
        ["C",   "",     "B",    "",     "B",    "B",    "T",    ""  ],
        ["B",    "B",    "",     "B",    "",     "B",    "B",    "T"  ],
        ["W",   "",     "B",    "",     "B",    "",     "W",    "W" ],
        ])
        self.assertEqual(_map, expected)

        character.move("right")
        expected = Map([
        ["",   "W",    "K",    "",     "B",    "W",    "W",    "W" ],
        ["",    "B",    "P",    "PB",   "",     "G",    "",     "W" ],
        ["",   "C",     "B",    "",     "B",    "B",    "T",    ""  ],
        ["B",    "B",    "",     "B",    "",     "B",    "B",    "T"  ],
        ["W",   "",     "B",    "",     "B",    "",     "W",    "W" ],
        ])
        self.assertEqual(_map, expected)

        character.move("down")
        expected = Map([
        ["",   "W",    "K",    "",     "B",    "W",    "W",    "W" ],
        ["",   "B",    "P",    "PB",   "",     "G",    "",     "W" ],
        ["",   "C",     "B",    "",     "B",    "B",    "T",    ""  ],
        ["B",  "",    "",     "B",    "",     "B",    "B",    "T"  ],
        ["W",  "B",     "B",    "",     "B",    "",     "W",    "W" ],
        ])
        self.assertEqual(_map, expected)

        character.move("down")
        expected = Map([
        ["",   "W",    "K",    "",     "B",    "W",    "W",    "W" ],
        ["",    "B",    "P",    "PB",   "",     "G",    "",     "W" ],
        ["",   "",     "B",    "",     "B",    "B",    "T",    ""  ],
        ["B",   "C",    "",     "B",    "",     "B",    "B",    "T"  ],
        ["W",   "B",     "B",    "",     "B",    "",     "W",    "W" ],
        ])
        self.assertEqual(_map, expected)

        character.move("right")
        expected = Map([
        ["",   "W",    "K",    "",     "B",    "W",    "W",    "W" ],
        ["",    "B",    "P",    "PB",   "",     "G",    "",     "W" ],
        ["",   "",     "B",    "",     "B",    "B",    "T",    ""  ],
        ["B",   "",    "C",     "B",    "",     "B",    "B",    "T"  ],
        ["W",   "B",     "B",    "",     "B",    "",     "W",    "W" ],
        ])
        self.assertEqual(_map, expected)

        character.move("right")
        expected = Map([
        ["",   "W",    "K",    "",     "B",    "W",    "W",    "W" ],
        ["",    "B",    "P",    "PB",   "",     "G",    "",     "W" ],
        ["",   "",     "B",    "",     "B",    "B",    "T",    ""  ],
        ["B",   "",    "C",     "",    "B",     "B",    "B",    "T"  ],
        ["W",   "B",     "B",    "",     "B",    "",     "W",    "W" ],
        ])
        self.assertEqual(_map, expected)

        character.move("right")
        expected = Map([
        ["",   "W",    "K",    "",     "B",    "W",    "W",    "W" ],
        ["",    "B",    "P",    "PB",   "",     "G",    "",     "W" ],
        ["",   "",     "B",    "",     "B",    "B",    "T",    ""  ],
        ["B",   "",    "",     "C",    "B",     "B",    "B",    "T"  ],
        ["W",   "B",     "B",    "",     "B",    "",     "W",    "W" ],
        ])
        self.assertEqual(_map, expected)

        character.move("up")
        expected = Map([
        ["",   "W",    "K",    "",     "B",    "W",    "W",    "W" ],
        ["",    "B",    "P",    "PB",   "",     "G",    "",     "W" ],
        ["",   "",     "B",    "C",     "B",    "B",    "T",    ""  ],
        ["B",   "",    "",     "",    "B",     "B",    "B",    "T"  ],
        ["W",   "B",     "B",    "",     "B",    "",     "W",    "W" ],
        ])
        self.assertEqual(_map, expected)

        character.move("left")
        expected = Map([
        ["",   "W",    "K",    "",     "B",    "W",    "W",    "W" ],
        ["",    "B",    "P",    "PB",   "",     "G",    "",     "W" ],
        ["",   "B",     "",    "C",     "B",    "B",    "T",    ""  ],
        ["B",   "",    "",     "",    "B",     "B",    "B",    "T"  ],
        ["W",   "B",     "B",    "",     "B",    "",     "W",    "W" ],
        ])
        self.assertEqual(_map, expected)

        character.move("left")
        expected = Map([
        ["",   "W",    "K",    "",     "B",    "W",    "W",    "W" ],
        ["",    "B",    "P",    "PB",   "",     "G",    "",     "W" ],
        ["",   "B",     "C",    "",     "B",    "B",    "T",    ""  ],
        ["B",   "",    "",     "",    "B",     "B",    "B",    "T"  ],
        ["W",   "B",     "B",    "",     "B",    "",     "W",    "W" ],
        ])
        self.assertEqual(_map, expected)

        character.move("up")
        expected = Map([
        ["",   "W",    "K",    "",     "B",    "W",    "W",    "W" ],
        ["",    "B",    "CP",    "PB",   "",     "G",    "",     "W" ],
        ["",   "B",     "",    "",     "B",    "B",    "T",    ""  ],
        ["B",   "",    "",     "",    "B",     "B",    "B",    "T"  ],
        ["W",   "B",     "B",    "",     "B",    "",     "W",    "W" ],
        ])
        self.assertEqual(_map, expected)

        character.move("up")
        expected = Map([
        ["",   "W",    "C",    "",     "B",    "W",    "W",    "W" ],
        ["",    "B",    "P",    "PB",   "",     "G",    "",     "W" ],
        ["",   "B",     "",    "",     "B",    "B",    "T",    ""  ],
        ["B",   "",    "",     "",    "B",     "B",    "B",    "T"  ],
        ["W",   "B",     "B",    "",     "B",    "",     "W",    "W" ],
        ])
        self.assertEqual(_map, expected)

        character.move("right")
        expected = Map([
        ["",   "W",    "",    "C",     "B",    "W",    "W",    "W" ],
        ["",    "B",    "P",    "PB",   "",     "G",    "",     "W" ],
        ["",   "B",     "",    "",     "B",    "B",    "T",    ""  ],
        ["B",   "",    "",     "",    "B",     "B",    "B",    "T"  ],
        ["W",   "B",     "B",    "",     "B",    "",     "W",    "W" ],
        ])
        self.assertEqual(_map, expected)

        character.move("down")
        expected = Map([
        ["",   "W",    "",    "C",     "B",    "W",    "W",    "W" ],
        ["",    "B",    "P",    "P",   "",     "G",    "",     "W" ],
        ["",   "B",     "",    "B",     "B",    "B",    "T",    ""  ],
        ["B",   "",    "",     "",    "B",     "B",    "B",    "T"  ],
        ["W",   "B",     "B",    "",     "B",    "",     "W",    "W" ],
        ])
        self.assertEqual(_map, expected)

        character.move("down")
        expected = Map([
        ["",   "W",    "",    "",     "B",    "W",    "W",    "W" ],
        ["",    "B",    "P",    "CP",   "",     "G",    "",     "W" ],
        ["",   "B",     "",    "B",     "B",    "B",    "T",    ""  ],
        ["B",   "",    "",     "",    "B",     "B",    "B",    "T"  ],
        ["W",   "B",     "B",    "",     "B",    "",     "W",    "W" ],
        ])
        self.assertEqual(_map, expected)

        character.move("right")
        expected = Map([
        ["",   "W",    "",    "",     "B",    "W",    "W",    "W" ],
        ["",    "B",    "P",    "P",   "C",     "G",    "",     "W" ],
        ["",   "B",     "",    "B",     "B",    "B",    "T",    ""  ],
        ["B",   "",    "",     "",    "B",     "B",    "B",    "T"  ],
        ["W",   "B",     "B",    "",     "B",    "",     "W",    "W" ],
        ])
        self.assertEqual(_map, expected)

        character.move("right")
        expected = Map([
        ["",   "W",    "",    "",     "B",    "W",    "W",    "W" ],
        ["",    "B",    "P",    "P",   "",     "C",    "",     "W" ],
        ["",   "B",     "",    "B",     "B",    "B",    "T",    ""  ],
        ["B",   "",    "",     "",    "B",     "B",    "B",    "T"  ],
        ["W",   "B",     "B",    "",     "B",    "",     "W",    "W" ],
        ])
        self.assertEqual(_map, expected)

        character.move("right")
        expected = Map([
        ["",   "W",    "",    "",     "B",    "W",    "W",    "W" ],
        ["",    "B",    "P",    "P",   "",     "",    "C",     "W" ],
        ["",   "B",     "",    "B",     "B",    "B",    "T",    ""  ],
        ["B",   "",    "",     "",    "B",     "B",    "B",    "T"  ],
        ["W",   "B",     "B",    "",     "B",    "",     "W",    "W" ],
        ])
        self.assertEqual(_map, expected)

        character.move("down")
        expected = Map([
        ["",   "W",    "",    "",     "B",    "W",    "W",    "W" ],
        ["",    "B",    "P",    "P",   "",     "",    "",     "W" ],
        ["",   "B",     "",    "B",     "B",    "B",    "CT",    ""  ],
        ["B",   "",    "",     "",    "B",     "B",    "B",    "T"  ],
        ["W",   "B",     "B",    "",     "B",    "",     "W",    "W" ],
        ])
        self.assertEqual(_map, expected)