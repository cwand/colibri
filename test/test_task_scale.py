import unittest

import xmltodict
import colibri
import os
from typing import Any


class TestTaskScale(unittest.TestCase):

    def test_task_scale_label(self):
        f = open(
            os.path.join('test', 'xml_input', 'test_scale.xml'))
        tree = xmltodict.parse(f.read(), xml_attribs=True)
        task = tree['colibri']['task']
        no: dict[str, Any] = {
            'ttest': {
                'Right': [0.0, 1.0, 1.5, -2.0],
                'Left': [1.0, 2.0, 3.0]
            }
        }
        colibri.tasks.task_apply_correction(task, no)

        self.assertEqual(len(no['ttest']['Right2']), 4)
        self.assertEqual(no['ttest']['Right2'][0], 0.0)
        self.assertEqual(no['ttest']['Right2'][1], 2.0)
        self.assertEqual(no['ttest']['Right2'][2], 3.0)
        self.assertEqual(no['ttest']['Right2'][3], -4.0)
