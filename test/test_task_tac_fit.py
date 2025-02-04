import unittest
import colibri
import numpy as np
from colibri.tasks import tac_fit
from typing import Any, OrderedDict


class TestTACFit(unittest.TestCase):

    def test_task_tac_fit_fail_missing_tag(self):

        task = OrderedDict[str, Any]()
        self.assertRaisesRegex(KeyError,
                               "Missing tags in TACFit task: <tac_name> "
                               "<time_label> <inp_label> <tis_label> <method> "
                               "<model>",
                               colibri.tasks.task_tac_fit, task, {})


class TestLogProb(unittest.TestCase):

    def test_logprob_step_nobounds(self):

        param_values = [0.7, 10.0, 0.0]
        param_names = ['amp', 'extent', '__lnsigma']

        param_bounds = {
            'amp': (-np.inf, np.inf),
            'extent': (-np.inf, np.inf),
            '__lnsigma': (-np.inf, np.inf),
        }
        tp = [0.0, 4.3, 7.5, 12.4, 16.2]
        in_func = [0.0, 10.3, 12.1, 8.1, 4.1]
        # "true" = [0.0, 15.5015, 40.5895, 70.4035, 61.5472]
        m = [0.0, 15.0, 40.0, 70.0, 61.0]

        p = tac_fit._log_prob(param_values, param_names,
                              colibri.model.model_step, tp, in_func, m,
                              param_bounds)

        self.assertAlmostEqual(p, -5.125319, places=3)

    def test_logprob_step_inbounds(self):
        param_values = [0.7, 10.0, 0.0]
        param_names = ['amp', 'extent', '__lnsigma']
        param_bounds = {
            'amp': (0.1, 2.0),
            'extent': (1.0, 100.0),
            '__lnsigma': (-2.0, 10.0),
        }
        tp = [0.0, 4.3, 7.5, 12.4, 16.2]
        in_func = [0.0, 10.3, 12.1, 8.1, 4.1]
        # "true" = [0.0, 15.5015, 40.5895, 70.4035, 61.5472]
        m = [0.0, 15.0, 40.0, 70.0, 61.0]

        p = tac_fit._log_prob(param_values, param_names,
                              colibri.model.model_step, tp, in_func, m,
                              param_bounds)

        self.assertAlmostEqual(p, -5.125319, places=3)


    def test_logprob_step_outbounds_low(self):
        param_values = [0.7, 10.0, 0.0]
        param_names = ['amp', 'extent', '__lnsigma']
        param_bounds = {
            'amp': (0.8, 1.0),
            'extent': (1.0, 100.0),
            '__lnsigma': (-2.0, 10.0),
        }
        tp = [0.0, 4.3, 7.5, 12.4, 16.2]
        in_func = [0.0, 10.3, 12.1, 8.1, 4.1]
        # "true" = [0.0, 15.5015, 40.5895, 70.4035, 61.5472]
        m = [0.0, 15.0, 40.0, 70.0, 61.0]

        p = tac_fit._log_prob(param_values, param_names,
                              colibri.model.model_step, tp, in_func, m,
                              param_bounds)

        self.assertEqual(p, -np.inf)

    def test_logprob_step_outbounds_high(self):
        param_values = [0.7, 10.0, 0.0]
        param_names = ['amp', 'extent', '__lnsigma']
        param_bounds = {
            'amp': (0.1, 1.0),
            'extent': (1.0, 5.0),
            '__lnsigma': (-2.0, 10.0),
        }
        tp = [0.0, 4.3, 7.5, 12.4, 16.2]
        in_func = [0.0, 10.3, 12.1, 8.1, 4.1]
        # "true" = [0.0, 15.5015, 40.5895, 70.4035, 61.5472]
        m = [0.0, 15.0, 40.0, 70.0, 61.0]

        p = tac_fit._log_prob(param_values, param_names,
                              colibri.model.model_step, tp, in_func, m,
                              param_bounds)

        self.assertEqual(p, -np.inf)
