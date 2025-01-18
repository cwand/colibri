import unittest

import xmltodict
import colibri
import os


class TestTaskCorrection(unittest.TestCase):

    def test_task_fails_missing_tags(self):
        f = open(
            os.path.join('test', 'xml_input', 'test_scale.xml'))
        tree = xmltodict.parse(f.read(), xml_attribs=True)
        task = tree['colibri']['task']

        del task['type']

        self.assertRaisesRegex(KeyError,
                               "Missing tags in Correction task: <type>",
                               colibri.tasks.task_apply_correction, task, {})
