import unittest
import random

from src.Dice import *

class TestDieTypes(unittest.TestCase):

    def test_four_sided_die(self):
        die = FourSidedDie()
        die.roll()
        self.assertEqual(die.face_count, 4)
        self.assertEqual(die.name, 'd4')
        self.assertEqual(die.__str__(), 'd4')
        self.assertEqual(die.__repr__(), 'Die("d4")')
        
        valid_rolls = list(range(1,5))
        for i in range(1000):
            die.roll()
            self.assertIn(die.rolled, valid_rolls, f"Die rolled outside of valid range")


    def test_six_sided_die(self):
        die = SixSidedDie()
        die.roll()
        self.assertEqual(die.face_count, 6)
        self.assertEqual(die.name, 'd6')
        self.assertEqual(die.__str__(), 'd6')
        self.assertEqual(die.__repr__(), 'Die("d6")')
        
        valid_rolls = list(range(1,7))
        for i in range(1000):
            die.roll()
            self.assertIn(die.rolled, valid_rolls)


    def test_eight_sided_die(self):
        die = EightSidedDie()
        die.roll()
        self.assertEqual(die.face_count, 8)
        self.assertEqual(die.name, 'd8')
        self.assertEqual(die.__str__(), 'd8')
        self.assertEqual(die.__repr__(), 'Die("d8")')
        
        valid_rolls = list(range(1,9))
        for i in range(1000):
            die.roll()
            self.assertIn(die.rolled, valid_rolls)


    def test_ten_sided_die(self):
        die = TenSidedDie()
        die.roll()
        self.assertEqual(die.face_count, 10)
        self.assertEqual(die.name, 'd10')
        self.assertEqual(die.__str__(), 'd10')
        self.assertEqual(die.__repr__(), 'Die("d10")')
        
        valid_rolls = list(range(1,11))
        for i in range(1000):
            die.roll()
            self.assertIn(die.rolled, valid_rolls)
    

    def test_twelve_sided_die(self):
        die = TwelveSidedDie()
        die.roll()
        self.assertEqual(die.face_count, 12)
        self.assertEqual(die.name, 'd12')
        self.assertEqual(die.__str__(), 'd12')
        self.assertEqual(die.__repr__(), 'Die("d12")')
        
        valid_rolls = list(range(1,13))
        for i in range(1000):
            die.roll()
            self.assertIn(die.rolled, valid_rolls)


    def test_twenty_sided_die(self):
        die = TwentySidedDie()
        die.roll()
        self.assertEqual(die.face_count, 20)
        self.assertEqual(die.name, 'd20')
        self.assertEqual(die.__str__(), 'd20')
        self.assertEqual(die.__repr__(), 'Die("d20")')
        
        valid_rolls = list(range(1,21))
        for i in range(1000):
            die.roll()
            self.assertIn(die.rolled, valid_rolls)


    def test_onehundred_sided_die(self):
        die = OneHundredSidedDie()
        die.roll()
        self.assertEqual(die.face_count, 100)
        self.assertEqual(die.name, 'd100')
        self.assertEqual(die.__str__(), 'd100')
        self.assertEqual(die.__repr__(), 'Die("d100")')
        
        valid_rolls = list(range(1,101))
        for i in range(1000):
            die.roll()
            self.assertIn(die.rolled, valid_rolls)

    

        


if __name__ == '__main__':
    unittest.main()