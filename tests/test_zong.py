import sys

sys.path.append('E:\game\Sword\src')
from zong import JianZong
from place import Place
import unittest

class TestChampoinZong(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def testIniatialState(self):
        arthur = JianZong(name = "Arthur")
        arthur.setGroup(1)
        place = Place()
        place.setName("sand")
        place.setChampion(arthur)
        self.assertEqual(arthur.position, place)
        self.assertEqual(arthur.health, 4)
        self.assertEqual(arthur.group, 1)
        self.assertEqual(len(arthur.skills), 3)
        self.assertEqual(arthur.states, [])
        print(arthur.skills)   



if __name__ == "__main__":
    unittest.main()
        