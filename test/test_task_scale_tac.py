import unittest
import xmltodict
import colibri
import os
from typing import Any


class TestTaskScaleTAC(unittest.TestCase):

    def test_task_scale_label(self):
        f = open(
            os.path.join('test', 'xml_input', 'test_tac_scale.xml'))
        tree = xmltodict.parse(f.read(), xml_attribs=True)
        task = tree['colibri']['task']
        no: dict[str, Any] = {}
        colibri.tasks.task_apply_correction(task, no)
        dyn = colibri.load_table(os.path.join('test', 'out.txt'))

        tacq = dyn['tacq']
        r1 = dyn['0']
        r2 = dyn['Right2']

        self.assertAlmostEqual(tacq[0], 0.0, places=7)
        self.assertAlmostEqual(r1[0], 1.669720725246406478e-09, places=7)
        self.assertAlmostEqual(r2[0], 0.0, places=7)

        self.assertAlmostEqual(tacq[1], 4.2, places=7)
        self.assertAlmostEqual(r1[1], 9.983449980727247697e-06, places=7)
        self.assertAlmostEqual(r2[1], 4.794023269153122e-06, places=7)

        self.assertAlmostEqual(tacq[2], 8.7, places=7)
        self.assertAlmostEqual(r1[2], 1.655645138234570568e-03, places=7)
        self.assertAlmostEqual(r2[2], 0.001414627308168, places=7)

        self.assertAlmostEqual(tacq[3], 13.1, places=7)
        self.assertAlmostEqual(r1[3], 5.599932675303434526e-02, places=7)
        self.assertAlmostEqual(r2[3], 0.127460377986212, places=7)

        self.assertAlmostEqual(tacq[4], 17.6, places=7)
        self.assertAlmostEqual(r1[4], 1.928118222420220462, places=7)
        self.assertAlmostEqual(r2[4], 3.473432179421435, places=7)

    def tearDown(self):
        if os.path.exists(os.path.join('test', 'out.txt')):
            os.remove(os.path.join('test', 'out.txt'))
