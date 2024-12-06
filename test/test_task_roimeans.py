import unittest
import colibri
import os
import xmltodict


class TestTaskROIMeans(unittest.TestCase):

    def test_task_simple(self):
        f = open(
            os.path.join('test', 'xml_input', 'test_roi_means_simple.xml'))
        tree = xmltodict.parse(f.read(), xml_attribs=True)
        task = tree['colibri']['task']
        colibri.task_roi_means(task)
        dyn = colibri.load_tac(os.path.join('test', 'out.txt'))
        tacq = dyn['tacq']
        self.assertEqual(tacq,
                         [0, 3.0, 6.3, 9.5, 12.8, 16.0, 19.3, 22.5, 25.8])

        r1 = dyn['1']
        r2 = dyn['2']

        self.assertEqual(r1[0], 0)
        self.assertAlmostEqual(r2[0], 31.3157, places=4)

        self.assertAlmostEqual(r1[1], 0.767681, places=6)
        self.assertAlmostEqual(r2[1], 3501.54, places=2)

        self.assertAlmostEqual(r1[2], 1229.61, places=2)
        self.assertAlmostEqual(r2[2], 33128.1, places=1)

        self.assertAlmostEqual(r1[3], 12019.3, places=1)
        self.assertAlmostEqual(r2[3], 38544.1, places=1)

        self.assertAlmostEqual(r1[4], 12058.9, places=1)
        self.assertAlmostEqual(r2[4], 9529.26, places=2)

        self.assertAlmostEqual(r1[5], 1277.01, places=2)
        self.assertAlmostEqual(r2[5], 642.525, places=3)

        self.assertAlmostEqual(r1[6], 13.4822, places=4)
        self.assertAlmostEqual(r2[6], 2.57748, places=5)

        self.assertAlmostEqual(r1[7], 0.748028, places=6)
        self.assertAlmostEqual(r2[7], 0.345963, places=6)

        self.assertEqual(r1[8], 0)
        self.assertAlmostEqual(r2[8], 0.0727437, places=7)

    def test_task_labels(self):
        f = open(os.path.join(
            'test', 'xml_input', 'test_roi_means_labels.xml'))
        tree = xmltodict.parse(f.read(), xml_attribs=True)
        task = tree['colibri']['task']
        colibri.task_roi_means(task)
        dyn = colibri.load_tac(os.path.join('test', 'out.txt'))
        tacq = dyn['tacq']
        self.assertEqual(tacq,
                         [0, 3.0, 6.3, 9.5, 12.8, 16.0, 19.3, 22.5, 25.8])

        r1 = dyn['a']
        r2 = dyn['b']

        self.assertEqual(r1[0], 0)
        self.assertAlmostEqual(r2[0], 31.3157, places=4)

        self.assertAlmostEqual(r1[1], 0.767681, places=6)
        self.assertAlmostEqual(r2[1], 3501.54, places=2)

        self.assertAlmostEqual(r1[2], 1229.61, places=2)
        self.assertAlmostEqual(r2[2], 33128.1, places=1)

        self.assertAlmostEqual(r1[3], 12019.3, places=1)
        self.assertAlmostEqual(r2[3], 38544.1, places=1)

        self.assertAlmostEqual(r1[4], 12058.9, places=1)
        self.assertAlmostEqual(r2[4], 9529.26, places=2)

        self.assertAlmostEqual(r1[5], 1277.01, places=2)
        self.assertAlmostEqual(r2[5], 642.525, places=3)

        self.assertAlmostEqual(r1[6], 13.4822, places=4)
        self.assertAlmostEqual(r2[6], 2.57748, places=5)

        self.assertAlmostEqual(r1[7], 0.748028, places=6)
        self.assertAlmostEqual(r2[7], 0.345963, places=6)

        self.assertEqual(r1[8], 0)
        self.assertAlmostEqual(r2[8], 0.0727437, places=7)

    def test_task_resample_img(self):
        f = open(os.path.join(
            'test', 'xml_input', 'test_roi_means_resample_img.xml'))
        tree = xmltodict.parse(f.read(), xml_attribs=True)
        task = tree['colibri']['task']
        colibri.task_roi_means(task)
        dyn = colibri.load_tac(os.path.join('test', 'out.txt'))
        tacq = dyn['tacq']
        self.assertEqual(tacq,
                         [0, 3.0, 6.3, 9.5, 12.8, 16.0, 19.3, 22.5, 25.8])

        r1 = dyn['1']
        r2 = dyn['2']

        self.assertAlmostEqual(r1[3], 11405.7, places=1)
        self.assertAlmostEqual(r2[3], 15053.1, places=1)

    def test_task_resample_roi(self):
        f = open(os.path.join(
            'test', 'xml_input', 'test_roi_means_resample_roi.xml'))
        tree = xmltodict.parse(f.read(), xml_attribs=True)
        task = tree['colibri']['task']
        colibri.task_roi_means(task)
        dyn = colibri.load_tac(os.path.join('test', 'out.txt'))
        tacq = dyn['tacq']
        self.assertEqual(tacq,
                         [0, 3.0, 6.3, 9.5, 12.8, 16.0, 19.3, 22.5, 25.8])

        r1 = dyn['1']
        r2 = dyn['2']

        self.assertAlmostEqual(r1[3], 13473.5, places=1)
        self.assertAlmostEqual(r2[3], 17120.9, places=1)

    def tearDown(self):
        if os.path.exists(os.path.join('test', 'out.txt')):
            os.remove(os.path.join('test', 'out.txt'))
