import sys

sys.path.append('E:\game\Sword\src')
from champion import Champion
from place import Place
from affect import Affect
from skill import Skill
from state import State
from state_util import *
from affect_util import *
import util
from solder import Solder
import unittest

class TestSkill(Skill):
    def __init__(self):
        super().__init__(name = "test skill")

    def cast(self):
        testAffect = Affect(owner = self, position = self.owner.position)
        # print(f"A skill with name {self.name} is casted.")

class TestChampoinInteraction(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def testChampionSkillInteraction(self):
        testChampion = Champion()
       
        testSkill = Skill()
        self.assertEqual(testChampion.position, None, "The initial position should be None.")
        self.assertEqual(testChampion.health, None, "The initial health should be None.")
        self.assertNotEqual(testChampion.group, None, "The initial group should be not be None.")
        self.assertEqual(testChampion.skills, [], "The initial skills should be [].")
        self.assertEqual(testChampion.states, [], "The initial states should be [].")
        testChampion.getSkill(testSkill)
        self.assertIn(testSkill, testChampion.skills, "Now the champoin should have the test skill")
        self.assertEqual(testSkill.owner,testChampion, "Now the champoin should be the owner of the test skill")

    def testChampionPlaceInteraction(self):
        testPlace = Place()
        testChampion = Champion()
        testSkill = TestSkill()
        testChampion.getSkill(testSkill)
        testPlace.setChampion(testChampion)
        self.assertEqual(testPlace, testChampion.position, "Now the champoin should have the position testPlace")
        self.assertIn(testChampion, testPlace.champions, "Now the champoin should have the test skill")
        testChampion.castSkill(testSkill)
        self.assertEqual(len(testPlace.affects), 1, "Now the champoin should have the test skill")

    def testSolderAttack(self):
        Place1 = Place()
        Place1.setName(1)
        Place2 = Place()
        Place2.setName(2)
        Solder1 = Solder()
        Solder2 = Solder()
        self.assertEqual(Solder1.health, 4, "A solder's health should be 4.")
        Place1.setChampion(Solder1)
        Place1.setChampion(Solder2)
        self.assertEqual(Solder1.position, Place1, "A solder is placed at place1.")
        Solder1.castSkill(Solder1.skills[0])
        self.assertEqual(1, len(Place1.affects), "An affect is placed at place1.")
        self.assertEqual(Solder1, Place1.affects[0].owner)
        Place1.settle()
        self.assertEqual(0, len(Place1.affects), "No affect is placed at place1.")
        self.assertEqual(1, len(Solder2.states), "One state is placed on solder1.")
        self.assertEqual(Solder2.states[0].owner, Solder2)
        Solder2.settleAllState()
        self.assertEqual(Solder2.health, 3, "A solder's health should be 3.")

    def testSolderMove(self):
        Place1 = Place()
        Place1.setName(1)
        Place2 = Place()
        Place2.setName(2)
        util.bondingPlaces((Place1, Place2))
        Solder1 = Solder()
        Solder2 = Solder()
        Place1.setChampion(Solder1)
        Place1.setChampion(Solder2)
        self.assertEqual(Solder1.position, Place1, "A solder is placed at place1.")
        Solder1.castSkill(Solder1.skills[2])
        self.assertEqual(Solder1.position, Place2, "A solder is placed at place2.")
        self.assertIn(Solder1, Place2.champions, "A solder is placed at place2.")
        self.assertNotIn(Solder1, Place1.champions, "A solder is not placed at place1.")




if __name__ == "__main__":
    unittest.main()