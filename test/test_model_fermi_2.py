import unittest
import colibri.model


class TestModelFermi2(unittest.TestCase):

    def test_model_fermi_2_case1(self):
        amp = 0.1
        amp2 = 0.3
        extent = 3.0
        extent2 = 6.0
        width1 = 1.0
        width2 = 3.0

        tp = [0.0, 3.7, 7.1, 10.2, 13.5, 17.8]
        in_func = [0.0, 572.1, 3021.5, 123.7, 50.21, 10.5]

        m = colibri.model.model_fermi_2(amp1=amp, extent1=extent,
                                        amp2=amp2, extent2=extent2,
                                        width1=width1, width2=width2,
                                        t=tp, in_func=in_func)

        self.assertEqual(6, len(m))
        self.assertAlmostEqual(0.0, m[0], places=4)
        self.assertAlmostEqual(389.333, m[1], places=3)
        self.assertAlmostEqual(2472.040, m[2], places=1)
        self.assertAlmostEqual(3249.592, m[3], places=2)
        self.assertAlmostEqual(1899.835, m[4], places=3)
        self.assertAlmostEqual(748.214, m[5], places=3)
