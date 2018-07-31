from unittest import TestCase

from finance.anomaly_detection import is_project_num_items_outlier,\
    is_project_total_raised_outlier

from salicml.utils.read_csv import read_csv

class TestIO(TestCase):
    def test_read_planila_orcamentaria(self):
        planilha_file_name = 'planilha_captacao.csv'
        planilha = read_csv(planilha_file_name)
        self.assertIsNotNone(planilha)


class TestAnomalyDetection(TestCase):
    def test_number_of_items_inlier(self):
        pronac = 172085
        outlier = is_project_num_items_outlier(pronac)
        self.assertEquals(outlier, False)


    def test_total_raised_intier(self):
        pronac = 111986
        outlier = is_project_total_raised_outlier(pronac)
        self.assertEquals(outlier, False)
