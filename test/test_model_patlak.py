import unittest
import colibri


class TestModelPatlak(unittest.TestCase):

    def test_model_step_case0(self):
        k = 3
        v0 = 10

        tp = [0.0, 4.3, 7.5, 12.4, 16.2]
        in_func = [0.0, 10.3, 12.1, 8.1, 4.1]

        m = colibri.model_patlak(k1=k, v0=v0, t=tp, in_func=in_func)

        self.assertEqual(5, len(m))
        self.assertAlmostEqual(0.0, m[0], places=3)
        self.assertAlmostEqual(169.435, m[1], places=3)
        self.assertAlmostEqual(294.955, m[2], places=3)
        self.assertAlmostEqual(403.425, m[3], places=3)
        self.assertAlmostEqual(432.965, m[4], places=3)
