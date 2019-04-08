from salicml.data.query import metrics
from salicml.data import data

COLUMNS = ["PRONAC", "Item", "vlAprovado", "vlComprovacao"]


@metrics.register('finance')
def operation_code_receipts(pronac, dt):
    pass


@data.lazy('planilha_comprovacao')
def approved_verified_items(df):
    receipts = (df[['idComprovantePagamento', 'PRONAC']]
                .groupby('idComprovantePagamento').count())
    repeated_receipts = receipts[receipts['PRONAC'] > 1].index.values
    lines = df.loc[df['idComprovantePagamento'].isin(repeated_receipts)]

    outliers_pronac = (linesu.groupby(['PRONAC'])
                       .nunique().index.values)
    return df[COLUMNS]
