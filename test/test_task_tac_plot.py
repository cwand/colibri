import unittest
import colibri
from typing import Any, OrderedDict


class TestTACPlot(unittest.TestCase):

    def test_task_tac_plot_fail_missing_tag(self):

        task = OrderedDict[str, Any]()
        self.assertRaisesRegex(KeyError,
                               "Missing tags in TACPlot task: <tac_name> "
                               "<time_label> <labels>",
                               colibri.tasks.task_tac_plot, task, {})
