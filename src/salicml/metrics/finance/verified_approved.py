from salicml.data.query import metrics
from salicml.data import data

COLUMNS = ["PRONAC", "Item", "vlAprovado", "vlComprovacao"]
VERIFIED_COLUMN = "vlComprovacao"
APPROVED_COLUMN = "vlAprovado"
MIN_EXPECTED_ITEMS = 0
MAX_EXPECTED_ITEMS = 0


@metrics.register('finance')
def verified_approved(pronac, data):
    """
    This metric compare budgetary items of SALIC projects in terms of
    verified versus approved value
    Items that have vlComprovacao > vlAprovacao * 1.5 are considered outliers
    output:
            is_outlier: True if any item is outlier
            number_of_outliers: Absolute number of items that are outliers
            outlier_items: Outlier items detail
    """
    items_df = data.approved_verified_items
    items_df = items_df.loc[items_df['PRONAC'] == int(pronac)]
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
    outlier_items = outlier_items_(features)
    features_size = features.shape[0]
    is_outlier = features_size > 0
    return {
        "is_outlier": is_outlier,
        "number_of_outliers": features_size,
        "minimum_expected": MIN_EXPECTED_ITEMS,
        "maximum_expected": MAX_EXPECTED_ITEMS,
        "outlier_items": outlier_items,
    }


@data.lazy('planilha_aprovacao_comprovacao')
def approved_verified_items(df):
    return df[COLUMNS]


def outlier_items_(features):
    outlier_items = []
    for row in features.itertuples():
        item_name = getattr(row, "Item")
        approved_value = getattr(row, "vlAprovado")
        verified_value = getattr(row, "vlComprovacao")

        item = {
            "item": item_name,
            "approved_value": approved_value,
            "verified_value": verified_value,
        }
        outlier_items.append(item)
    return outlier_items
