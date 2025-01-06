import unittest
from typing import Type

from src.Dice import Die
from src.Dice import FourSidedDie, SixSidedDie, EightSidedDie, TenSidedDie, TwelveSidedDie, TwentySidedDie, OneHundredSidedDie


class DieTypeAndPropertyTestCases(unittest.TestCase):
    @staticmethod
    def TestDieProperties(test: unittest.TestCase, die: Die, die_type: Type, num_faces: int) -> None:
        valid_rolls = list(range(1,(num_faces+1)))

        test.assertIsInstance(die, die_type)

        test.assertEqual(die.rolled, 0)
        test.assertEqual(die.face_count, num_faces)
        test.assertEqual(die.name, f'd{num_faces}')
        test.assertEqual(die.__str__(), f'd{num_faces}')
        
        #test rolled property updates when rolled
        roll_result = die.roll()
        test.assertIsInstance(roll_result, int)
        test.assertIsNot(roll_result, 0)
        test.assertIn(die.rolled, valid_rolls, f"{die.name} rolled outside of valid range")

        # test 1K roll iterations
        for i in range(1000):
            die.roll()
            test.assertIn(die.rolled, valid_rolls, f"{die.name} rolled outside of valid range")


    def test_four_sided_die_properties(self):
        """Test all properties of 4 sided dice (d4)"""
        test_die = FourSidedDie()
        DieTypeAndPropertyTestCases.TestDieProperties(test=self,
                                                      die=test_die,
                                                      die_type=type(test_die),
                                                      num_faces=4)

    def test_six_sided_die_properties(self):
        """Test all properties of 6 sided dice (d6)"""
        test_die = SixSidedDie()
        DieTypeAndPropertyTestCases.TestDieProperties(test=self,
                                                      die=test_die,
                                                      die_type=type(test_die),
                                                      num_faces=6)

    def test_eight_sided_die_properties(self):
        """Test all properties of 8 sided dice (d8)"""
        test_die = EightSidedDie()
        DieTypeAndPropertyTestCases.TestDieProperties(test=self,
                                                      die=test_die,
                                                      die_type=type(test_die),
                                                      num_faces=8)

    def test_ten_sided_die_properties(self):
        """Test all properties of 10 sided dice (d10)"""
        test_die = TenSidedDie()
        DieTypeAndPropertyTestCases.TestDieProperties(test=self,
                                                      die=test_die,
                                                      die_type=type(test_die),
                                                      num_faces=10)

    def test_twelve_sided_die_properties(self):
        """Test all properties of 12 sided dice (d12)"""
        test_die = TwelveSidedDie()
        DieTypeAndPropertyTestCases.TestDieProperties(test=self,
                                                      die=test_die,
                                                      die_type=type(test_die),
                                                      num_faces=12)

    def test_twenty_sided_die_properties(self):
        """Test all properties of 20 sided dice (d20)"""
        test_die = TwentySidedDie()
        DieTypeAndPropertyTestCases.TestDieProperties(test=self,
                                                      die=test_die,
                                                      die_type=type(test_die),
                                                      num_faces=20)

    def test_onehundred_sided_die_properties(self):
        """Test all properties of 100 sided dice (d100)"""
        test_die = OneHundredSidedDie()
        DieTypeAndPropertyTestCases.TestDieProperties(test=self,
                                                      die=test_die,
                                                      die_type=type(test_die),
                                                      num_faces=100)

class DieMethodTestCases(unittest.TestCase):
    def setUp(self):
        self.four_sided_a = FourSidedDie()
        self.four_sided_b = FourSidedDie()
        self.four_sided_c = FourSidedDie()


    def test_adding_die_rolls_together_from_same_dietype(self):
        """test adding same type dice objects returns total of both dice's rolls"""
        (_.roll() for _ in [self.four_sided_a, self.four_sided_b])
        roll_total = self.four_sided_a.rolled + self.four_sided_b.rolled
        self.assertEqual(self.four_sided_a + self.four_sided_b, roll_total)


    def test_adding_die_and_int(self):
        """test adding dice object with a whole number returns the dice's roll plus the number"""
        self.four_sided_a.roll()
        self.assertEqual(self.four_sided_a + 5, self.four_sided_a.rolled + 5)


    def test_summing_array_of_dice(self):
        """test ability to use sum() on an array of dice to get the roll total of all dice in array"""
        dice_arr = [self.four_sided_a, self.four_sided_b, self.four_sided_c]
        # roll dice just because
        [_.roll() for _ in dice_arr]
        manual_roll_total = dice_arr[0].rolled + dice_arr[1].rolled + dice_arr[2].rolled
        self.assertEqual(sum(dice_arr), manual_roll_total)


    def test_summing_array_of_dice_and_ints(self):
        # [die, int, die, int, die]
        dice_arr = [self.four_sided_a, 5, self.four_sided_b, 2, self.four_sided_c]
        # rolling dice returns ints, so we can use the below to get an int array to sum and check against
        summed_array = sum([_.roll() if issubclass(type(_), Die) else _ for _ in dice_arr])
        self.assertEqual(sum(dice_arr), summed_array)


    def test_subtracting_die_rolls_together_from_same_dietype(self):
        # do same tests for subtraction that you did for addition
        pass

    def test_multiplying_die_rolls_together_from_same_dietype(self):
        # do same tests for multiplication that you did for addition
        pass

    

    
class TestRollManager(unittest.TestCase):
    pass
        


if __name__ == '__main__':
    unittest.main()