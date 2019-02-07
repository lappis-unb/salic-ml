import unittest

from salicml.data.query import metrics


class TestProponentProjects(unittest.TestCase):

    def test_proponent_with_analyzed_project(self):
        pronac = "1011645"  # CGCCPF -> 00367651000114
        project = metrics.get_project(pronac)

        # Testing metric
        proponent_pronacs = project.finance.proponent_projects

        assert proponent_pronacs['analyzed_projects']['number_of_projects'] > 0

        assert any(
            proponent_pronacs['analyzed_projects']['pronacs_of_this_proponent']
        )

        assert pronac in (
            proponent_pronacs['analyzed_projects']['pronacs_of_this_proponent']
        )

    def test_proponent_with_submitted_project(self):
        pronac = "079172"  # CGCCPF -> '00274080001'
        project = metrics.get_project(pronac)

        # Testing metric
        proponentpronacs = project.finance.proponent_projects

        assert proponentpronacs['submitted_projects']['number_of_projects'] > 0

        assert any(
            proponentpronacs['submitted_projects']['pronacs_of_this_proponent']
        )

        assert pronac in (
            proponentpronacs['submitted_projects']['pronacs_of_this_proponent']
        )
