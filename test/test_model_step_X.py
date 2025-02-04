import unittest
import colibri


class TestModelStep(unittest.TestCase):

    def test_model_step_case0(self):
        amp = 0.7
        extent = 10.0

        tp = [0.0, 4.3, 7.5, 12.4, 16.2]
        in_func = [0.0, 10.3, 12.1, 8.1, 4.1]

        m = colibri.model.model_step(amp=amp, extent=extent,
                                     t=tp, in_func=in_func)

        self.assertEqual(5, len(m))
        self.assertAlmostEqual(0.0, m[0], places=3)
        self.assertAlmostEqual(15.5015, m[1], places=3)
        self.assertAlmostEqual(40.5895, m[2], places=3)
        self.assertAlmostEqual(70.4035, m[3], places=3)
        self.assertAlmostEqual(61.5472, m[4], places=3)

    def test_model_step_case0_kws_dict(self):
        kw = {'amp': 0.7, 'extent': 10.0, 'lnsigma': 0.1}

        tp = [0.0, 4.3, 7.5, 12.4, 16.2]
        in_func = [0.0, 10.3, 12.1, 8.1, 4.1]

        m = colibri.model.model_step(t=tp, in_func=in_func, **kw)

        self.assertEqual(5, len(m))
        self.assertAlmostEqual(0.0, m[0], places=3)
        self.assertAlmostEqual(15.5015, m[1], places=3)
        self.assertAlmostEqual(40.5895, m[2], places=3)
        self.assertAlmostEqual(70.4035, m[3], places=3)
        self.assertAlmostEqual(61.5472, m[4], places=3)

    def test_model_step_case1(self):
        amp = 0.1
        extent = 3.0

        tp = [0.0, 3.7, 7.1, 10.2, 13.5, 17.8]
        in_func = [0.0, 572.1, 3021.5, 123.7, 50.21, 10.5]

        m = colibri.model.model_step(amp=amp, extent=extent,
                                     t=tp, in_func=in_func)

        self.assertEqual(6, len(m))
        self.assertAlmostEqual(0.0, m[0], places=4)
        self.assertAlmostEqual(102.0502, m[1], places=3)
        self.assertAlmostEqual(582.2645, m[2], places=1)
        self.assertAlmostEqual(457.7583, m[3], places=3)
        self.assertAlmostEqual(25.0844, m[4], places=3)
        self.assertAlmostEqual(7.3057, m[5], places=3)


class TestModelStep2(unittest.TestCase):

    def test_model_step_2_case1(self):
        amp = 0.1
        amp2 = 0.3
        extent = 3.0
        extent2 = 6.0

        tp = [0.0, 3.7, 7.1, 10.2, 13.5, 17.8]
        in_func = [0.0, 572.1, 3021.5, 123.7, 50.21, 10.5]

        m = colibri.model.model_step_2(amp1=amp, extent1=extent,
                                       amp2=amp2, extent2=extent2,
                                       t=tp, in_func=in_func)

        self.assertEqual(6, len(m))
        self.assertAlmostEqual(0.0, m[0], places=4)
        self.assertAlmostEqual(419.5657, m[1], places=1)
        self.assertAlmostEqual(2704.4526, m[2], places=1)
        self.assertAlmostEqual(3640.1826, m[3], places=3)
        self.assertAlmostEqual(1233.5420, m[4], places=2)
        self.assertAlmostEqual(81.7247, m[5], places=2)
