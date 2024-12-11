import unittest
import xmltodict
import colibri
import os
from typing import Any


class TestTaskSaveLoadTable(unittest.TestCase):

    def test_task_save_table(self):
        f = open(
            os.path.join('test', 'xml_input', 'test_save_table.xml'))
        tree = xmltodict.parse(f.read(), xml_attribs=True)
        task = tree['colibri']['task']
        no: dict[str, Any] = {
            'table': {
                'tacq': [0.0, 1.0, 2.0],
                'A':    [1.0, 3.0, 3.5],
                '2':    [-1.3, 0.1, -2.0]
            }
        }

        colibri.tasks.task_save_table(task, no)
        dyn = colibri.load_table(os.path.join('test', 'out.txt'))

        tacq = dyn['tacq']
        r1 = dyn['A']
        r2 = dyn['2']

        self.assertAlmostEqual(tacq[0], 0.0, places=7)
        self.assertAlmostEqual(r1[0], 1.0, places=7)
        self.assertAlmostEqual(r2[0], -1.3, places=7)

        self.assertAlmostEqual(tacq[1], 1.0, places=7)
        self.assertAlmostEqual(r1[1], 3.0, places=7)
        self.assertAlmostEqual(r2[1], 0.1, places=7)

        self.assertAlmostEqual(tacq[2], 2.0, places=7)
        self.assertAlmostEqual(r1[2], 3.5, places=7)
        self.assertAlmostEqual(r2[2], -2.0, places=7)

    def test_task_load_table(self):
        f = open(
            os.path.join('test', 'xml_input', 'test_load_table.xml'))
        tree = xmltodict.parse(f.read(), xml_attribs=True)
        task = tree['colibri']['task']
        no: dict[str, Any] = {}

        colibri.tasks.task_load_table(task, no)
        dyn = no['table']

        tacq = dyn['tacq']
        r1 = dyn['A']
        r2 = dyn['2']

        self.assertAlmostEqual(tacq[0], 0.0, places=7)
        self.assertAlmostEqual(r1[0], 1.0, places=7)
        self.assertAlmostEqual(r2[0], -1.3, places=7)

        self.assertAlmostEqual(tacq[1], 1.0, places=7)
        self.assertAlmostEqual(r1[1], 3.0, places=7)
        self.assertAlmostEqual(r2[1], 0.1, places=7)

        self.assertAlmostEqual(tacq[2], 2.0, places=7)
        self.assertAlmostEqual(r1[2], 3.5, places=7)
        self.assertAlmostEqual(r2[2], -2.0, places=7)

    def tearDown(self):
        if os.path.exists(os.path.join('test', 'out.txt')):
            os.remove(os.path.join('test', 'out.txt'))
