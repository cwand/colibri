import unittest
import colibri
from typing import Any, OrderedDict


class TestTACFit(unittest.TestCase):

    def test_task_tac_fit_fail_missing_tag(self):

        task = OrderedDict[str, Any]()
        self.assertRaisesRegex(KeyError,
                               "Missing tags in TACFit task: <tac_name> "
                               "<time_label> <inp_label> <tis_label> <method> "
                               "<model>",
                               colibri.tasks.task_tac_fit, task, {})
