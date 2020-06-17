# -*- coding: utf-8 -*
from . import PedigreeMatrix
import unittest


class InputTest(unittest.TestCase):
    def test_ecospold_input(self):
        input_text = "(1, 2, 3)"
        pm = PedigreeMatrix(1,)
        self.assertEqual(pm.parse_args((input_text,)), [1, 2, 3])

    def test_float_inputs(self):
        input_text = (1, 2, 3)
        pm = PedigreeMatrix(1,)
        self.assertEqual(pm.parse_args((input_text,)), [1, 2, 3])

    def test_str_inputs(self):
        input_text = ("1", "2", "3")
        pm = PedigreeMatrix(1,)
        self.assertEqual(pm.parse_args((input_text,)), [1, 2, 3])

    def test_padding(self):
        input_text = [1, 2, 3]
        pm = PedigreeMatrix(input_text)
        self.assertEqual(pm.pad_args(input_text),
            [1, 2, 3, 1, 1, 1])

    def test_complete_parsing_ecospold_input(self):
        input_text = "(1, 2, 3)"
        pm = PedigreeMatrix(input_text)
        self.assertEqual(pm.inputs, [1, 2, 3, 1, 1, 1])

    def test_complete_parsing_float_inputs(self):
        input_text = (1, 2, 3)
        pm = PedigreeMatrix(input_text)
        self.assertEqual(pm.inputs, [1, 2, 3, 1, 1, 1])

    def test_complete_parsing_str_inputs(self):
        input_text = ("1", "2", "3")
        pm = PedigreeMatrix(input_text)
        self.assertEqual(pm.inputs, [1, 2, 3, 1, 1, 1])

    def test_denester(self):
        input_dict = {1: {2: {3: 4}}}
        pm = PedigreeMatrix(1,)
        self.assertEqual(pm.denester((1, 2, 3), input_dict), 4)
        input_dict = {1: 2}
        pm = PedigreeMatrix(1,)
        self.assertEqual(pm.denester((1, ), input_dict), 2)
