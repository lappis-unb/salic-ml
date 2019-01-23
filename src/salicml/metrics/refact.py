from salicml.data import data

def get_segment_id(pronac):
    """
    Returns the cultural segment of the
    project with the given pronac.
    """
    df = data.planilha_orcamentaria
    return (
        df[df['PRONAC'] == int(pronac)]
        .iloc[0]['idSegmento']
    )


def segment_projects(segment_id):
    """
    Returns all projects from a segment.
    """
    df = data.items
    return (
        df[df['idSegmento'] == str(segment_id)]
        .drop_duplicates(["PRONAC"])
        .values
    )


def get_project_items(pronac):
    """
    Returns all items from a project.
    """
    df = data.items
    return (
        df[df['PRONAC'] == pronac]
        .drop(columns=['PRONAC', 'idSegmento'])
        .values[:, 0]
    )


def segment_common_items(segment_id):
    """
    Returns all the common items in a segment.
    """
    df = data.common_items
    return (
        df
        .loc[str(segment_id)]
        .reset_index(drop=1)
        .drop(columns=["itemOccurrences"])
    )

## Retorna a porcentagem de itens de um projeto
## que são comuns em seu segmento
def common_items_percentage(pronac):
    """
    Returns the percentage of items in a project that are
    common in the cultural segment. 
    """
    segment_id = get_segment_id(pronac) 
    seg_common_items = segment_common_items(segment_id)
    
    if len(seg_common_items) == 0:
        return 0

    project_items = get_project_items(pronac)
    project_items_amount = len(project_items)
    
    if project_items_amount == 0:
        return 1

    common_found_items = sum(seg_common_items.isin(project_items)['idPlanilhaItens'])

    return common_found_items / project_items_amount


## ??
@data.lazy('planilha_orcamentaria')
def distintic_items(df):
    return df[
        ['idPlanilhaItens', 'Item']
    ].set_index('idPlanilhaItens').drop_duplicates()


@data.lazy('planilha_orcamentaria')
def items(df):
    """
    Retorna todos os itens usados nos segmentos
    sem repetição
    """
    return (
        df[['PRONAC', 'idSegmento', 'idPlanilhaItens']]
        .drop_duplicates()
    )


@data.lazy('items')
def common_items(df):
    """
    Retorna os itens que são comuns nos segmentos
    formato idSegmento idPlanilhaItens
    """
    percentage = 0.1
    
    items_filter = lambda x : x[None : max(2, int(len(x) * percentage))]
   
    return (
        df
        .groupby(['idSegmento', 'idPlanilhaItens'])
        .count()
        .rename(columns={'PRONAC': 'itemOccurrences'})
        .sort_values('itemOccurrences', ascending=False)
        .reset_index(['idSegmento', 'idPlanilhaItens'])
        .groupby('idSegmento')
        .apply(items_filter)
        .reset_index(['idSegmento'], drop=True)
        .set_index(['idSegmento'])
    )

    
@data.lazy('items', 'common_items')
def common_items_metrics(items, common_items):
    segments = common_items.index.unique()
    metrics = {}

    for seg in segments:
        common_items = segment_common_items(seg)
        projects = segment_projects(seg)

        metric_values = []

        for proj in projects:
            pronac = proj[0]
            percentage = common_items_percentage(pronac)
            metric_values.append(percentage)

        metrics[seg] = {
            'mean': np.mean(metric_values),
            'std': np.std(metric_values)
        }

    return pd.DataFrame.from_dict(metrics, orient='index')
