import os
import unittest
from datetime import datetime
import colibri
from typing import Union


class TestGetAcqDateTime(unittest.TestCase):

    def test_acq_datetime_8_3V_1(self):
        dcm_path = os.path.join(
            'test', 'data', '8_3V',
            'Patient_test_Study_10_Scan_10_Bed_1_Dyn_1.dcm')
        dt = colibri.get_acq_datetime(dcm_path)
        self.assertEqual(dt, datetime(2023, 12, 1, 13, 30, 28, 0))

    def test_acq_datetime_8_3V_5(self):
        dcm_path = os.path.join(
            'test', 'data', '8_3V',
            'Patient_test_Study_10_Scan_10_Bed_1_Dyn_5.dcm')
        dt = colibri.get_acq_datetime(dcm_path)
        self.assertEqual(dt, datetime(2023, 12, 1, 13, 30, 40, 800000))


class TestShiftTime(unittest.TestCase):

    def test_shift_time_one_step(self):
        res = colibri.shift_time([1.0, 2.0], [1.0, 2.0], 1.0)
        self.assertEqual(2, len(res))
        self.assertAlmostEqual(1.0, res[0], places=6)
        self.assertAlmostEqual(1.0, res[1], places=6)

    def test_shift_time_one_and_a_half_steps(self):
        res = colibri.shift_time([2.0, 4.0, 3.0], [1.0, 2.0, 3.0], 1.5)
        self.assertEqual(3, len(res))
        self.assertAlmostEqual(2.0, res[0], places=6)
        self.assertAlmostEqual(2.0, res[1], places=6)
        self.assertAlmostEqual(3.0, res[2], places=6)


class TestSaveLoadTAC(unittest.TestCase):

    def test_save_load_tac(self):
        tac: dict[Union[str, int], list[float]] = \
            {1: [1.0, 2.0, 3.0],
             '2': [0.5, 0.1, 3.0],
             'tacq': [0.0, 1.2, 5.4]
             }
        colibri.save_tac(tac, os.path.join('test', 'tac.txt'))
        tac2 = colibri.load_tac(os.path.join('test', 'tac.txt'))
        self.assertEqual(tac2['tacq'], [0.0, 1.2, 5.4])
        self.assertEqual(tac2['1'], [1.0, 2.0, 3.0])
        self.assertEqual(tac2['2'], [0.5, 0.1, 3.0])

    def tearDown(self):
        if os.path.exists(os.path.join('test', 'tac.txt')):
            os.remove(os.path.join('test', 'tac.txt'))
