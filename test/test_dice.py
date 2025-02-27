import unittest
from typing import Type

from src.Dice import Die, Dice
from src.Dice import FourSidedDie, SixSidedDie, EightSidedDie, TenSidedDie, TwelveSidedDie, TwentySidedDie, OneHundredSidedDie


class DieTypeAndPropertyTestCases(unittest.TestCase):
    @staticmethod
    def TestDieProperties(test: unittest.TestCase, die: Die, die_type: Type, num_faces: int) -> None:
        valid_rolls = list(range(1, (num_faces+1)))

        test.assertIsInstance(die, die_type)

        test.assertEqual(die.rolled, 0)
        test.assertEqual(die.face_count, num_faces)
        test.assertEqual(die.name, f'd{num_faces}')
        test.assertEqual(die.__str__(), f'd{num_faces}')

        # test rolled property updates when rolled
        roll_result = die.roll()
        test.assertIsInstance(roll_result, int)
        test.assertIsNot(roll_result, 0)
        test.assertIn(die.rolled, valid_rolls, f"{
                      die.name} rolled outside of valid range")

        # test 1K roll iterations
        for i in range(1000):
            die.roll()
            test.assertIn(die.rolled, valid_rolls, f"{
                          die.name} rolled outside of valid range")

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

        self.twenty_sided_a = TwentySidedDie()
        self.twenty_sided_b = TwentySidedDie()

    # ##########################################################################
    # DIE LOGIC

    def test_comparing_dice(self):
        die1 = SixSidedDie()
        object.__setattr__(die1, "rolled", 2)
        die2 = SixSidedDie()
        object.__setattr__(die2, "rolled", 4)
        die3 = SixSidedDie()
        object.__setattr__(die3, "rolled", 4)

        self.assertEqual(die2, die3)
        self.assertNotEqual(die1, die2)
        self.assertGreater(die2, die1)
        self.assertGreaterEqual(die2, die1)
        self.assertGreaterEqual(die3, die2)
        self.assertLess(die1, die2)
        self.assertLessEqual(die3, die2)
        self.assertLessEqual(die1, die2)
        self.assertNotEqual(die1, die2)

    # ##########################################################################
    # SUMMING DIE

    def test_adding_die_rolls_together_from_same_dietype(self):
        """test adding same type dice objects returns total of both dice's rolls"""
        object.__setattr__(self.four_sided_a, "rolled", 4)
        object.__setattr__(self.four_sided_b, "rolled", 3)
        self.assertEqual(self.four_sided_a + self.four_sided_b, 7)

    def test_adding_die_and_int(self):
        """test adding dice object with a whole number returns the dice's roll plus the number"""
        object.__setattr__(self.four_sided_a, "rolled", 4)
        self.assertEqual(self.four_sided_a + 5, 9)

    def test_adding_int_and_die(self):
        """test adding a whole number with a die returns the sum of the number and dice's roll"""
        object.__setattr__(self.four_sided_a, "rolled", 4)
        self.assertEqual(5 + self.four_sided_a, 9)

    def test_summing_array_of_dice(self):
        """test ability to use sum() on an array of dice to get the roll total of all dice in array"""
        object.__setattr__(self.four_sided_a, "rolled", 4)
        object.__setattr__(self.four_sided_b, "rolled", 3)
        object.__setattr__(self.four_sided_c, "rolled", 2)
        dice_arr = [self.four_sided_a, self.four_sided_b, self.four_sided_c]
        self.assertEqual(sum(dice_arr), 9)

    def test_summing_array_of_dice_and_ints(self):
        object.__setattr__(self.four_sided_a, "rolled", 4)
        object.__setattr__(self.four_sided_b, "rolled", 3)
        object.__setattr__(self.four_sided_c, "rolled", 2)
        # [die, int, die, int, die]
        dice_arr = [self.four_sided_a, 5,
                    self.four_sided_b, 2, self.four_sided_c]
        self.assertEqual(sum(dice_arr), 16)

    # ##########################################################################
    # SUBTRACTING DIE

    def test_subtracting_die_rolls_from_same_dietype(self):
        """test subtracting same type dice objects returns difference of both dice's rolls"""
        object.__setattr__(self.four_sided_a, "rolled", 4)
        object.__setattr__(self.four_sided_b, "rolled", 1)
        self.assertEqual(self.four_sided_a - self.four_sided_b, 3)

    def test_subtracting_die_and_int(self):
        """test subtracting dice object with a whole number returns the dice's roll minus the number"""
        object.__setattr__(self.four_sided_a, "rolled", 4)
        self.assertEqual(self.four_sided_a - 2, 2)

    def test_subtracting_int_and_die(self):
        """test subtracting int with a die returns the number minus the dice's roll"""
        object.__setattr__(self.four_sided_a, "rolled", 3)
        self.assertEqual(4 - self.four_sided_a, 1)

    # ##########################################################################
    # MULTIPLYING DIE

    def test_multiplying_die_rolls_from_same_dietype(self):
        """test multiplying same type dice objects returns the product of both dice's rolls"""
        object.__setattr__(self.four_sided_a, "rolled", 3)
        object.__setattr__(self.four_sided_b, "rolled", 2)
        self.assertEqual(self.four_sided_a * self.four_sided_b, 6)

    def test_multiplying_die_and_int(self):
        """test multiplying dice object with a whole number returns the dice's roll times the number"""
        object.__setattr__(self.four_sided_a, "rolled", 3)
        self.assertEqual(self.four_sided_a * 4, 12)

    def test_multiplying_int_and_die(self):
        """test multiplying int with dice object returns the product of the int and the dice's roll"""
        object.__setattr__(self.four_sided_a, "rolled", 2)
        self.assertEqual(4 * self.four_sided_a, 8)

    # ##########################################################################
    # DIVIDING DIE
    #   default is floor divide (we need whole numbers)

    def test_dividing_die_rolls_from_same_dietype(self):
        """test dividing same type dice objects returns the division of dice's rolls"""
        object.__setattr__(self.twenty_sided_a, "rolled", 12)
        object.__setattr__(self.twenty_sided_b, "rolled", 4)
        self.assertEqual(self.twenty_sided_a / self.twenty_sided_b, 3)

        object.__setattr__(self.twenty_sided_a, "rolled", 17)
        object.__setattr__(self.twenty_sided_b, "rolled", 4)
        self.assertEqual(self.twenty_sided_a / self.twenty_sided_b, 4)

    def test_dividing_die_and_int(self):
        """test dividing dice object with a whole number returns the dice's roll divided by the number"""
        object.__setattr__(self.twenty_sided_a, "rolled", 15)
        self.assertEqual(self.twenty_sided_a / 2, 7)

    def test_dividing_int_and_die(self):
        """test dividing int with dice object returns the result of int divided by dice's roll"""
        object.__setattr__(self.twenty_sided_a, "rolled", 5)
        self.assertEqual(19 / self.twenty_sided_a, 3)

    @unittest.skip("no known need to implement ceiling logic yet...")
    def test_setting_ceiling_divide(self):
        raise NotImplementedError(
            "Create tests for test_setting_ceiling_divide")


class DiceTests(unittest.TestCase):
    def setUp(self):
        self.dice = Dice(die_type=SixSidedDie, count=3)

    def test_dice_init(self):
        self.assertIsInstance(self.dice, Dice)

    def test_getting_len_of_dice(self):
        self.assertEqual(len(self.dice), 3)

    def test_dice_print(self):
        self.assertEqual(self.dice.__str__(), "3d6, [0, 0, 0]")

    def test_dice_print_after_roll(self):
        # set dice roll state of current_roll manually for assertion
        object.__setattr__(self.dice.roll_history[0][0], "rolled", 4)
        object.__setattr__(self.dice.roll_history[0][1], "rolled", 2)
        object.__setattr__(self.dice.roll_history[0][2], "rolled", 5)
        self.assertEqual(self.dice.__str__(), "3d6, [4, 2, 5]")

    def test_dice_count(self):
        self.assertEqual(len(self.dice.dice), 3)
        with self.assertRaises(IndexError):
            self.dice.dice[3]

    def test_dice_initial_state(self):
        self.assertIsInstance(self.dice.dice[0], SixSidedDie)
        self.assertIsInstance(self.dice.dice[1], SixSidedDie)
        self.assertIsInstance(self.dice.dice[2], SixSidedDie)
        self.assertEqual(self.dice.dice[0].rolled, 0)
        self.assertEqual(self.dice.dice[1].rolled, 0)
        self.assertEqual(self.dice.dice[2].rolled, 0)

    def test_rolling_dice(self):
        rolled = self.dice.roll()

        # validate roll return
        self.assertEqual(len(rolled), 3)
        self.assertIsInstance(rolled[0], Die)
        self.assertIsInstance(rolled[1], Die)
        self.assertIsInstance(rolled[2], Die)
        self.assertGreater(rolled[0].rolled, 0)
        self.assertGreater(rolled[1].rolled, 0)
        self.assertGreater(rolled[2].rolled, 0)

        # validate dice update within dice object
        self.assertGreater(self.dice.dice[0].rolled, 0)
        self.assertGreater(self.dice.dice[1].rolled, 0)
        self.assertGreater(self.dice.dice[2].rolled, 0)

    def test_rolling_updates_history(self):
        # reset self.dice
        self.setUp()
        start_len = 1

        self.assertEqual([d.rolled for d in self.dice.current_roll], [0, 0, 0])
        self.assertEqual(len(self.dice.roll_history), start_len)
        self.assertEqual(self.dice.current_roll, self.dice.dice)
        with self.assertRaises(IndexError):
            self.dice.previous_roll

        start_len += 1
        self.dice.roll()
        self.assertEqual(len(self.dice.roll_history), start_len)
        self.assertNotEqual(
            [d.rolled for d in self.dice.current_roll], [0, 0, 0])
        self.assertEqual(
            [d.rolled for d in self.dice.previous_roll], [0, 0, 0])
        self.assertIsNotNone(self.dice.previous_roll)
        self.assertNotEqual(self.dice.current_roll, self.dice.previous_roll)
        self.assertEqual(self.dice.current_roll, self.dice.dice)

        # do it a couple more times to validate roll history updates
        for i in range(5):
            start_len += 1
            self.dice.roll()
            self.assertEqual(len(self.dice.roll_history), start_len)
            self.assertNotEqual(
                [d.rolled for d in self.dice.current_roll], [0, 0, 0])
            self.assertNotEqual(
                [d.rolled for d in self.dice.previous_roll], [0, 0, 0])
            self.assertEqual(self.dice.current_roll, self.dice.dice)

    def test_returning_totals(self):
        # reset self.dice
        self.setUp()

        self.assertEqual(len(self.dice.roll_history), 1)
        self.assertEqual(self.dice.current_total, 0)
        with self.assertRaises(IndexError):
            self.dice.previous_total

        self.dice.roll()
        self.assertEqual(len(self.dice.roll_history), 2)
        self.assertNotEqual(self.dice.current_total, 0)
        self.assertIsNotNone(self.dice.previous_total)
        self.assertEqual(self.dice.previous_total, 0)

        self.dice.roll()
        self.assertEqual(len(self.dice.roll_history), 3)
        self.assertNotEqual(self.dice.current_total, 0)
        self.assertNotEqual(self.dice.previous_total, 0)

    @unittest.skip
    def test_adding_die_of_same_type_to_dice(self):
        self.dice.add(SixSidedDie())


class TestRollManager(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()
