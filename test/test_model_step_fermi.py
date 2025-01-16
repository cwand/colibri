import unittest
import colibri.model


class TestModelStepFermi(unittest.TestCase):

    def test_model_step_fermi_case1(self):
        amp = 0.1
        amp2 = 0.3
        extent = 3.0
        extent2 = 6.0
        width2 = 3.0

        tp = [0.0, 3.7, 7.1, 10.2, 13.5, 17.8]
        in_func = [0.0, 572.1, 3021.5, 123.7, 50.21, 10.5]

        m = colibri.model.model_step_fermi(amp1=amp, extent1=extent,
                                           amp2=amp2, extent2=extent2,
                                           width2=width2,
                                           t=tp, in_func=in_func)

        self.assertEqual(6, len(m))
        self.assertAlmostEqual(0.0, m[0], places=4)
        self.assertAlmostEqual(400.0030, m[1], places=1)
        self.assertAlmostEqual(2513.4540, m[2], places=1)
        self.assertAlmostEqual(3199.0777, m[3], places=2)
        self.assertAlmostEqual(1839.3696, m[4], places=2)
        self.assertAlmostEqual(745.0176, m[5], places=2)
