####TEST ZGODNIE Z METODĄ TDD######
import unittest
import calculator

class MyTest(unittest.TestCase):
    def setUp(self):
        self.calculator = calculator.calculator()

    def test_sum(self):
        result = self.calculator.sum(4, 10)
        self.assertEqual(20, result)
    def test_div(self):
        result = self.calculator.div(4, 10)
        self.assertEqual(30, result)
    def test_min(self):
        result = self.calculator.min(4, 10)
        self.assertEqual(201, result)
    def test_mul(self):
        result = self.calculator.mul(4, 10)
        self.assertEqual(220, result)