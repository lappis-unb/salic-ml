import unittest

from salicml.data.query import metrics


class TestProponentProjects(unittest.TestCase):

    def test_proponent_with_analyzed_project(self):
        pronac = "1011645"  # CGCCPF -> 00367651000114
        project = metrics.get_project(pronac)

        # # Testing cached dictionary
        # analyzed_projects = self.proponent_projects.analyzed_projects
        # submitted_projects = self.proponent_projects.submitted_projects

        # pronac_keys = ["pronacs_list", "num_pronacs"]

        # for key in analyzed_projects.keys():
        #     map(lambda x: self.assertIn(x, analyzed_projects[key]), pronac_keys)

        # for key in analyzed_projects.keys():
        #     map(lambda x: self.assertIn(x, submitted_projects[key]), pronac_keys)

        # Testing get metric
        proponent_pronacs = project.finance.proponent_projects
        
        self.assertGreater(
            proponent_pronacs["analyzed_projects"]["number_of_projects"], 0
        )
        self.assertTrue(
            any(proponent_pronacs["analyzed_projects"]["pronacs_of_this_proponent"])
        )
        self.assertIn(
            pronac, proponent_pronacs["analyzed_projects"]["pronacs_of_this_proponent"]
        )

    # def test_proponent_with_submitted_project(self):
    #     pronac = "079172"  # CGCCPF -> '00274080001'

    #     # Testing cached dictionary
    #     analyzed_projects = self.proponent_projects.analyzed_projects
    #     submitted_projects = self.proponent_projects.submitted_projects

    #     pronac_keys = ["pronacs_list", "num_pronacs"]

    #     for key in analyzed_projects.keys():
    #         map(lambda x: self.assertIn(x, analyzed_projects[key]), pronac_keys)

    #     for key in analyzed_projects.keys():
    #         map(lambda x: self.assertIn(x, submitted_projects[key]), pronac_keys)

    #     # Testing get metric
    #     proponent_pronacs = self.proponent_projects.get_metrics(pronac)

    #     self.assertGreater(
    #         proponent_pronacs["submitted_projects"]["number_of_projects"], 0
    #     )
    #     self.assertTrue(
    #         any(proponent_pronacs["submitted_projects"]["pronacs_of_this_proponent"])
    #     )
    #     self.assertIn(
    #         pronac, proponent_pronacs["submitted_projects"]["pronacs_of_this_proponent"]
    #     )
