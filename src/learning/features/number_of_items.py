import pandas as pd


class FeatureNumberOfItems:
    def __init__(self):
        pass

    def get_projects_number_of_items(self, items):
        """Receives budgetary items of SALIC projects in a matrix form as input
        The matrix must be a python list of python lists, where each inner list
        represents a row in the matrix. For each distinct pronac on the input,
        there will be exactly one row in the output matrix, containing the
        feature.

        Input format:
        The order of the elements of the inner list must be:
        pronac (str), id_segmento (str), id_planilha_aprovacao (int)

        Input example:

        [['012345', 123, 'A1'],
         ['012345', 124, 'A1'],
         ['012345', 125, 'A1'],
         ['012348', 126, 'A2'],
         ['012348', 127, 'A2'],
         ['012350', 128, 'A3'], ]


        Output example:

        [['012345', '2A', 3],
         ['012348', '3A', 2],
         ['012350', '4D', 1],
         ]
        """

        PRONAC = "PRONAC"
        SEGMENT = "id_segmento"
        ID = "id_planilha_aprovacao"
        NUMBER_OF_ITEMS = "number_of_items"
        COLUMNS = [PRONAC, ID, SEGMENT]

        items_df = pd.DataFrame(items, columns=COLUMNS)

        pronacs_group = items_df.groupby(by=[PRONAC, SEGMENT]).count()
        pronacs_group.rename(columns={ID: NUMBER_OF_ITEMS}, inplace=True)
        pronacs_group.reset_index(inplace=True)

        features = pronacs_group.values.tolist()
        return features

    def get_pronac_number_of_items(self, items):
        """Receives budgetary items of a SALIC project in a matrix form as input
        The matrix must be a python list of python lists, where each inner list
        represents a row in the matrix. An exception will be raise if there's
        more than one distinct pronac in the input. The behavior is undefined
        if the same pronac has more than one segment.

        Input format:
        The order of the elements of the inner list must be:
        pronac (str), id_segmento (str), id_planilha_aprovacao (int)

        Input example:

        [['012345', '2A', 123],
         ['012345', '2A', 124],
         ['012345', '2A', 125],
        ]

        Output example:

        ['012345', '2A', 3]
        """

        res = self.get_projects_number_of_items(items)
        if len(res) == 1:
            return res[0]
        else:
            raise ValueError("More than one distinct pronac were given.")
