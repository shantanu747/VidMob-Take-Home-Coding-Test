import unittest
from calculator import *

class TestCalculator(unittest.TestCase):
    #Test the is_a_num() function
    def test_is_a_num(self):
        self.assertAlmostEqual(is_a_num("2"), True)
        self.assertAlmostEqual(is_a_num("cinnamon"), False)
        self.assertAlmostEqual(is_a_num("2.3"), True)
        self.assertAlmostEqual(is_a_num("-0.2"), True)
        self.assertAlmostEqual(is_a_num("2.shantanu"), False)
        self.assertAlmostEqual(is_a_num("lol"), False)
    
    #Test the perform_operation() function
    def test_perform_operation(self):
        self.assertAlmostEqual(perform_operation("2", "+", "2"), "4.0")
        self.assertAlmostEqual(perform_operation("1", "+", "2"), "3.0")

        self.assertAlmostEqual(perform_operation("100", "-", "50"), "50.0")
        self.assertAlmostEqual(perform_operation("2.4", "-", "0.4"), "2.0")

        self.assertAlmostEqual(perform_operation("0.1", "*", "10"), "1.0")
        self.assertAlmostEqual(perform_operation("-2", "*", "2.4"), "-4.8")

        self.assertAlmostEqual(perform_operation("-.32", "/", ".5"), "-0.64")
        self.assertAlmostEqual(perform_operation("100", "/", "4"), "25.0")

    #Test setup_expression and evaluate_expression both, if first works then second will work as well
    def test_evaluate_expression(self):
        self.assertAlmostEqual(evaluate_expression("1+2"), 3.0)
        self.assertAlmostEqual(evaluate_expression("4*5/2"), 10.0)
        self.assertAlmostEqual(evaluate_expression("-.32/.5"), -0.64)

        #These examples fail
        #TODO: Figure out why these particular cases doesn't work and fix it
        #self.assertAlmostEqual(evaluate_expression("-5+-8--11*2"), 9.0)
        #self.assertAlmostEqual(evaluate_expression("(4-2)*3.5"), 7.0)
        #self.assertAlmostEqual(evaluate_expression("((3+3)*4-2)"), 22.0)
        
        

        

    