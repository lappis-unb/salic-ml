import unittest

from core.utils.read_csv import read_csv_with_different_type
from core.finance.metrics.proponent_projects import ProponentProjects

class TestProponentProjects(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestProponentProjects, cls).setUpClass()

        csv_name = 'planilha_comprovacao.csv'
        usecols = ['PRONAC', 'proponenteCgcCpf']
        cls.dt_verified_funds = read_csv_with_different_type(csv_name, {'PRONAC': str, \
                                                                        'proponenteCgcCpf': str}, usecols=usecols)

        csv_name = 'planilha_projetos.csv'
        usecols = ['PRONAC', 'CgcCpf']
        cls.dt_projects = read_csv_with_different_type(csv_name, {'PRONAC': str, 'CgcCpf': str}, usecols=usecols)

        cls.proponent_projects = ProponentProjects(cls.dt_verified_funds, cls.dt_projects)


    def test_IO(self):
        csv_name = 'planilha_comprovacao.csv'
        usecols = ['PRONAC', 'proponenteCgcCpf']
        csv = read_csv_with_different_type(csv_name, {'PRONAC': str, 'proponenteCgcCpf': str}, usecols=usecols)
        self.assertIsNotNone(csv)

        csv_name = 'planilha_projetos.csv'
        usecols = ['PRONAC', 'CgcCpf']
        csv = read_csv_with_different_type(csv_name, {'PRONAC': str, 'CgcCpf': str}, usecols=usecols)
        self.assertIsNotNone(csv)


    def test_proponent_with_analyzed_project(self):
        pronac = '1011645'  # CGCCPF -> 00367651000114

        # Testing cached dictionary
        analyzed_projects = self.proponent_projects.analyzed_projects
        submitted_projects = self.proponent_projects.submitted_projects

        pronac_keys = ['pronacs_list', 'num_pronacs']

        for key in analyzed_projects.keys():
            map(lambda x: self.assertIn(x, analyzed_projects[key]), pronac_keys)

        for key in analyzed_projects.keys():
            map(lambda x: self.assertIn(x, submitted_projects[key]), pronac_keys)

        # Testing get metric
        proponent_pronacs = self.proponent_projects.get_metrics(pronac)

        self.assertGreater(proponent_pronacs['analyzed_projects']['number_of_projects'], 0)
        self.assertTrue(any(proponent_pronacs['analyzed_projects']['pronacs_of_this_proponent']))
        self.assertIn(pronac, proponent_pronacs['analyzed_projects']['pronacs_of_this_proponent'])


    def test_proponent_with_submitted_project(self):
        pronac = '079172'  # CGCCPF -> '00274080001'

        # Testing cached dictionary
        analyzed_projects = self.proponent_projects.analyzed_projects
        submitted_projects = self.proponent_projects.submitted_projects

        pronac_keys = ['pronacs_list', 'num_pronacs']

        for key in analyzed_projects.keys():
            map(lambda x: self.assertIn(x, analyzed_projects[key]), pronac_keys)

        for key in analyzed_projects.keys():
            map(lambda x: self.assertIn(x, submitted_projects[key]), pronac_keys)

        # Testing get metric
        proponent_pronacs = self.proponent_projects.get_metrics(pronac)

        self.assertGreater(proponent_pronacs['submitted_projects']['number_of_projects'], 0)
        self.assertTrue(any(proponent_pronacs['submitted_projects']['pronacs_of_this_proponent']))
        self.assertIn(pronac, proponent_pronacs['submitted_projects']['pronacs_of_this_proponent'])