import sys

sys.path.append('E:\game\Sword\src')
from champion import Champion
import unittest

class TestChampoin(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Champion = Champion()

    def testIniatialState(self):
        self.assertEqual(self.Champion.position, None, "The initial position should be None.")
        self.assertEqual(self.Champion.health, None, "The initial health should be None.")
        self.assertEqual(self.Champion.group, None, "The initial group should be None.")
        self.assertEqual(self.Champion.skills, [], "The initial skills should be {}.")
        self.assertEqual(self.Champion.states, [], "The initial states should be {}.")


if __name__ == "__main__":
    unittest.main()
        
    