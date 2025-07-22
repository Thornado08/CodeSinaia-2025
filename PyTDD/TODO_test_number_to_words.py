import unittest
from TODO_number_to_words import number_to_words

class TestNums(unittest.TestCase):
    def sample_unit_test(self):
        return None
    def test_string(self):
        self.assertEqual(number_to_words("schaorma"), None)
    def test_double(self):
        self.assertEqual(number_to_words(3.14), None)
    def test_zero(self):
        self.assertEqual(number_to_words(0), "zero") 
    def test_single_digit(self):
        self.assertEqual(number_to_words(7), "seven")
    def test_teens(self):
        self.assertEqual(number_to_words(13), "thirteen")
    def test_tens(self):
        self.assertEqual(number_to_words(40), "forty")
        self.assertEqual(number_to_words(89), "eighty-nine")
    def test_hundreds(self):
        self.assertEqual(number_to_words(100), "one hundred")
        self.assertEqual(number_to_words(219), "two hundred nineteen")
    def test_thousands(self):
        self.assertEqual(number_to_words(1000), "one thousand")
        self.assertEqual(number_to_words(3456), "three thousand four hundred fifty-six")
    def test_max(self):
        self.assertEqual(number_to_words(3999), "three thousand nine hundred ninety-nine")
    def test_negative(self):
        self.assertEqual(number_to_words(-5), "Number out of range (0 to 3999)")
    def test_too_large(self):
        self.assertEqual(number_to_words(4000), "Number out of range (0 to 3999)")
