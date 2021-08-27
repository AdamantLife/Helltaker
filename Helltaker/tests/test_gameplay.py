## Test Utility
import unittest
## Test Target
from Helltaker import GameplaySequence

MAP = [
    ["C", "S", "p"],
    ["G", "K", ""],
    ["T", "W", "B"],
    ["", "W", "B"],
]

class TestGameplay(unittest.TestCase):
    def test(self):
        inputs = ["up", "right", "right", "right", "down", "down", "left", "down", "left", "down"]
        actions = [
        [], ## Up off map = No action
        ["right"], ## Kick Skeleton
        ["right","right"], ## Move into Skeletons Space
        ["right","right","RIGHT"], ## Move onto Spikes AND get hurt
        ["right","right","RIGHT", "down"], ## Move Down
        ["right","right","RIGHT", "down", "down"], ## Kick Block to no Effect
        ["right","right","RIGHT", "down", "down", "left"], ## Move Left onto Key
        ["right","right","RIGHT", "down", "down", "left"], ## Move into wall = No Action
        ["right","right","RIGHT", "down", "down", "left", "left"], ## Move Left through Gate
        ["right","right","RIGHT", "down", "down", "left", "left", "down"], ## Move onto Target space
        ] ## remaining willpower should be 0

        
        gameplay = GameplaySequence(MAP, 9)
        for inp, expected in zip(inputs[:-1], actions[:-1]):
            gameplay.move(inp)
            self.assertEqual(gameplay.actions, expected)

        ## Moving to a Target Square results in the Victory Exception
        self.assertRaises(GameplaySequence.Victory, gameplay.move, inputs[-1])
        self.assertEqual(gameplay.actions, actions[-1])

        self.assertEqual(gameplay.remaining_actions(), 0)
        ## With 0 Willpower remaining, trying to make a legal move should result in RuntimeError
        self.assertRaises(GameplaySequence.GameOver, gameplay.move, "down")
