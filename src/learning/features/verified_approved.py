import pandas as pd

from flask import current_app as app


COLUMNS = ["PRONAC", "Item", "vlAprovado", "vlComprovacao"]
VERIFIED_COLUMN = "vlComprovacao"
APPROVED_COLUMN = "vlAprovado"


def log(message):
    with app.app_context():
        app.logger.info(message)


class VerifiedApprovedFeature:
    def __init__(self):
        pass

    def get_features(self, items_dataset):
        """Receives budgetary items of SALIC projects in a matrix form as input
        The matrix must be a python list of python lists, where each inner list
        represents a row in the matrix. For each distinct pronac on the input,
        there will be exactly one row in the output matrix, containing the
        feature. Return items that vlComprovacao > vlAprovacao * 1.5

        Input format:
        The order of the elements of the inner list must be:
        pronac (str), item (str), vlAprovado (money), vlComprovacao (money)

        Input example:

        [['012345', 'Lousa', 123, 55],
         ['012345', 'Lousa', 124, 55],
         ['012345', 'Aviao', 125, 500],
         ['012348', 'Mansão', 126, 55],
         ['012348', 'Lousa', 127, 55],
         ['012350', 'Lambo', 128, 1000], ]


        Output example:

        [['012345', 'Aviao', 125, 500],
         ['012350', 'Lambo', 128, 1000], ]
        """

        if isinstance(items_dataset, list):
            items_df = pd.DataFrame(items_dataset)
            items_df.columns = items_df.iloc[0].values
            items_df = items_df[1:]
            items_df = items_df[COLUMNS]
        else:
            items_df = items_dataset.copy()

        items_df[[APPROVED_COLUMN, VERIFIED_COLUMN]] = items_df[
            [APPROVED_COLUMN, VERIFIED_COLUMN]
        ].astype(float)
        items_df["Item"] = items_df["Item"].str.replace("\r", "")
        items_df["Item"] = items_df["Item"].str.replace("\n", "")
        items_df["Item"] = items_df["Item"].str.replace('"', "")
        items_df["Item"] = items_df["Item"].str.replace("'", "")
        items_df["Item"] = items_df["Item"].str.replace("\\", "")

        THRESHOLD = 1.5
        bigger_than_approved = items_df[VERIFIED_COLUMN] > (
            items_df[APPROVED_COLUMN] * THRESHOLD
        )
        features = items_df[bigger_than_approved]
        return features
