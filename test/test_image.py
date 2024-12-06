import os.path
import unittest
import colibri
import SimpleITK as sitk


class TestLoadDynamicSeries(unittest.TestCase):

    def test_load_dynamic_series_8_3V(self):
        dcm_path = os.path.join('test', 'data', '8_3V')
        dyn = colibri.load_dynamic_series(dcm_path)
        img = dyn['img']
        acq = dyn['acq']
        self.assertEqual(len(img), 9)
        self.assertEqual(img[0].GetSize(), (128, 128, 64))
        self.assertEqual(img[0].GetSpacing(), (4.92, 4.92, 4.92))
        self.assertEqual(img[0].GetDimension(), 3)
        self.assertEqual(img[1].GetSize(), (128, 128, 64))
        self.assertEqual(img[1].GetSpacing(), (4.92, 4.92, 4.92))
        self.assertEqual(img[1].GetDimension(), 3)
        self.assertEqual(img[2].GetSize(), (128, 128, 64))
        self.assertEqual(img[2].GetSpacing(), (4.92, 4.92, 4.92))
        self.assertEqual(img[2].GetDimension(), 3)
        self.assertEqual(img[3].GetSize(), (128, 128, 64))
        self.assertEqual(img[3].GetSpacing(), (4.92, 4.92, 4.92))
        self.assertEqual(img[3].GetDimension(), 3)
        self.assertEqual(img[4].GetSize(), (128, 128, 64))
        self.assertEqual(img[4].GetSpacing(), (4.92, 4.92, 4.92))
        self.assertEqual(img[4].GetDimension(), 3)
        self.assertEqual(img[5].GetSize(), (128, 128, 64))
        self.assertEqual(img[5].GetSpacing(), (4.92, 4.92, 4.92))
        self.assertEqual(img[5].GetDimension(), 3)
        self.assertEqual(img[6].GetSize(), (128, 128, 64))
        self.assertEqual(img[6].GetSpacing(), (4.92, 4.92, 4.92))
        self.assertEqual(img[6].GetDimension(), 3)
        self.assertEqual(img[7].GetSize(), (128, 128, 64))
        self.assertEqual(img[7].GetSpacing(), (4.92, 4.92, 4.92))
        self.assertEqual(img[7].GetDimension(), 3)
        self.assertEqual(img[8].GetSize(), (128, 128, 64))
        self.assertEqual(img[8].GetSpacing(), (4.92, 4.92, 4.92))
        self.assertEqual(img[8].GetDimension(), 3)
        self.assertEqual(acq,
                         [0, 3.0, 6.3, 9.5, 12.8, 16.0, 19.3, 22.5, 25.8])


class TestResampleSeriesToReference(unittest.TestCase):

    def test_resample_series_to_reference_8_3V(self):
        dcm_path = os.path.join('test', 'data', '8_3V')
        dyn = colibri.load_dynamic_series(dcm_path)

        ref_img = sitk.ReadImage(os.path.join(
            'test', 'data', '8_3V_seg', 'Segmentation_2.nrrd'))

        img = colibri.resample_series_to_reference(dyn['img'], ref_img)
        self.assertEqual(img[0].GetSize(), (512, 512, 132))
        self.assertAlmostEqual(img[0].GetSpacing()[0], 1.269531, places=5)
        self.assertAlmostEqual(img[0].GetSpacing()[1], 1.269531, places=5)
        self.assertAlmostEqual(img[0].GetSpacing()[2], 2.5, places=5)
        self.assertEqual(img[0].GetDimension(), 3)
        self.assertEqual(img[1].GetSize(), (512, 512, 132))
        self.assertAlmostEqual(img[1].GetSpacing()[0], 1.269531, places=5)
        self.assertAlmostEqual(img[1].GetSpacing()[1], 1.269531, places=5)
        self.assertAlmostEqual(img[1].GetSpacing()[2], 2.5, places=5)
        self.assertEqual(img[1].GetDimension(), 3)
        self.assertEqual(img[2].GetSize(), (512, 512, 132))
        self.assertAlmostEqual(img[2].GetSpacing()[0], 1.269531, places=5)
        self.assertAlmostEqual(img[2].GetSpacing()[1], 1.269531, places=5)
        self.assertAlmostEqual(img[2].GetSpacing()[2], 2.5, places=5)
        self.assertEqual(img[2].GetDimension(), 3)
        self.assertEqual(img[3].GetSize(), (512, 512, 132))
        self.assertAlmostEqual(img[3].GetSpacing()[0], 1.269531, places=5)
        self.assertAlmostEqual(img[3].GetSpacing()[1], 1.269531, places=5)
        self.assertAlmostEqual(img[3].GetSpacing()[2], 2.5, places=5)
        self.assertEqual(img[3].GetDimension(), 3)
        self.assertEqual(img[4].GetSize(), (512, 512, 132))
        self.assertAlmostEqual(img[4].GetSpacing()[0], 1.269531, places=5)
        self.assertAlmostEqual(img[4].GetSpacing()[1], 1.269531, places=5)
        self.assertAlmostEqual(img[4].GetSpacing()[2], 2.5, places=5)
        self.assertEqual(img[4].GetDimension(), 3)
        self.assertEqual(img[5].GetSize(), (512, 512, 132))
        self.assertAlmostEqual(img[5].GetSpacing()[0], 1.269531, places=5)
        self.assertAlmostEqual(img[5].GetSpacing()[1], 1.269531, places=5)
        self.assertAlmostEqual(img[5].GetSpacing()[2], 2.5, places=5)
        self.assertEqual(img[5].GetDimension(), 3)
        self.assertEqual(img[6].GetSize(), (512, 512, 132))
        self.assertAlmostEqual(img[6].GetSpacing()[0], 1.269531, places=5)
        self.assertAlmostEqual(img[6].GetSpacing()[1], 1.269531, places=5)
        self.assertAlmostEqual(img[6].GetSpacing()[2], 2.5, places=5)
        self.assertEqual(img[6].GetDimension(), 3)
        self.assertEqual(img[7].GetSize(), (512, 512, 132))
        self.assertAlmostEqual(img[7].GetSpacing()[0], 1.269531, places=5)
        self.assertAlmostEqual(img[7].GetSpacing()[1], 1.269531, places=5)
        self.assertAlmostEqual(img[7].GetSpacing()[2], 2.5, places=5)
        self.assertEqual(img[7].GetDimension(), 3)
        self.assertEqual(img[8].GetSize(), (512, 512, 132))
        self.assertAlmostEqual(img[8].GetSpacing()[0], 1.269531, places=5)
        self.assertAlmostEqual(img[8].GetSpacing()[1], 1.269531, places=5)
        self.assertAlmostEqual(img[8].GetSpacing()[2], 2.5, places=5)
        self.assertEqual(img[8].GetDimension(), 3)


class TestSeriesRoiMeans(unittest.TestCase):

    def test_series_roi_means_8_3V(self):
        dcm_path = os.path.join('test', 'data', '8_3V')
        roi_path = os.path.join(
            'test', 'data', '8_3V_seg', 'Segmentation.nrrd')
        dyn = colibri.load_dynamic_series(dcm_path)
        roi = sitk.ReadImage(roi_path)

        r = colibri.series_roi_means(dyn['img'], roi)

        self.assertEqual(r[1][0], 0)
        self.assertAlmostEqual(r[2][0], 31.3157, places=4)

        self.assertAlmostEqual(r[1][1], 0.767681, places=6)
        self.assertAlmostEqual(r[2][1], 3501.54, places=2)

        self.assertAlmostEqual(r[1][2], 1229.61, places=2)
        self.assertAlmostEqual(r[2][2], 33128.1, places=1)

        self.assertAlmostEqual(r[1][3], 12019.3, places=1)
        self.assertAlmostEqual(r[2][3], 38544.1, places=1)

        self.assertAlmostEqual(r[1][4], 12058.9, places=1)
        self.assertAlmostEqual(r[2][4], 9529.26, places=2)

        self.assertAlmostEqual(r[1][5], 1277.01, places=2)
        self.assertAlmostEqual(r[2][5], 642.525, places=3)

        self.assertAlmostEqual(r[1][6], 13.4822, places=4)
        self.assertAlmostEqual(r[2][6], 2.57748, places=5)

        self.assertAlmostEqual(r[1][7], 0.748028, places=6)
        self.assertAlmostEqual(r[2][7], 0.345963, places=6)

        self.assertEqual(r[1][8], 0)
        self.assertAlmostEqual(r[2][8], 0.0727437, places=7)


class TestLazySeriesRoiMeans(unittest.TestCase):

    def test_lazy_series_roi_means_8_3V_no_resample(self):
        dcm_path = os.path.join('test', 'data', '8_3V')
        roi_path = os.path.join(
            'test', 'data', '8_3V_seg', 'Segmentation.nrrd')
        dyn = colibri.lazy_series_roi_means(dcm_path, roi_path)

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

    def test_lazy_series_roi_means_8_3V_resample_roi(self):
        dcm_path = os.path.join('test', 'data', '8_3V')
        roi_path = os.path.join(
            'test', 'data', '8_3V_seg', 'Segmentation_2.nrrd')
        dyn = colibri.lazy_series_roi_means(dcm_path, roi_path, resample='roi')

        r1 = dyn['1']
        r2 = dyn['2']

        self.assertAlmostEqual(r1[3], 13473.5, places=1)
        self.assertAlmostEqual(r2[3], 17120.9, places=1)

    def test_lazy_series_roi_means_8_3V_resample_img(self):
        dcm_path = os.path.join('test', 'data', '8_3V')
        roi_path = os.path.join(
            'test', 'data', '8_3V_seg', 'Segmentation_2.nrrd')
        dyn = colibri.lazy_series_roi_means(dcm_path, roi_path, resample='img')

        r1 = dyn['1']
        r2 = dyn['2']

        self.assertAlmostEqual(r1[3], 11405.7, places=1)
        self.assertAlmostEqual(r2[3], 15053.1, places=1)

    def test_custom_labels(self):
        dcm_path = os.path.join('test', 'data', '8_3V')
        roi_path = os.path.join(
            'test', 'data', '8_3V_seg', 'Segmentation.nrrd')
        dyn = colibri.lazy_series_roi_means(dcm_path, roi_path,
                                            labels={'0': 'a',
                                                    '2': '14'})
        self.assertTrue('a' in dyn.keys())
        self.assertTrue('1' in dyn.keys())
        self.assertTrue('14' in dyn.keys())
        self.assertTrue('tacq' in dyn.keys())
        self.assertFalse('0' in dyn.keys())
        self.assertFalse('2' in dyn.keys())

    def test_frame_dur(self):
        dcm_path = os.path.join('test', 'data', '8_3V')
        roi_path = os.path.join(
            'test', 'data', '8_3V_seg', 'Segmentation.nrrd')
        dyn = colibri.lazy_series_roi_means(dcm_path, roi_path,
                                            frame_dur=True)
        frame_durs = dyn['frame_dur']
        self.assertEqual(3.04, frame_durs[0])
        self.assertEqual(3.26, frame_durs[1])
        self.assertEqual(3.26, frame_durs[2])
        self.assertEqual(3.26, frame_durs[3])
        self.assertEqual(3.25, frame_durs[4])
        self.assertEqual(3.26, frame_durs[5])
        self.assertEqual(3.25, frame_durs[6])
        self.assertEqual(3.26, frame_durs[7])
        self.assertEqual(3.26, frame_durs[8])

    def test_ignore_label(self):
        dcm_path = os.path.join('test', 'data', '8_3V')
        roi_path = os.path.join(
            'test', 'data', '8_3V_seg', 'Segmentation.nrrd')
        dyn = colibri.lazy_series_roi_means(dcm_path, roi_path,
                                            ignore=['0', '2'])
        self.assertTrue('1' in dyn.keys())
        self.assertFalse('0' in dyn.keys())
        self.assertFalse('2' in dyn.keys())
