import os
import numpy as np

from core.data_handler.data_source import DataSource

class CommonItemsRatio():
    def __init__(self, items, dt_comprovacao):
        """
            This function receives a pandas.DataFrame with all items of all
            Salic projects and generates the mean and variance of the
            percentage of the items of a project that are in the list of the
            most common items for that segment. It also caches the list of the
            most common items of each segment.
            Input:
                items: pandas.Dataframe containing the all items of all
                       Salic projects. It must contain at least the columns
                       'idSegmento', 'PRONAC', and 'idPlanilhaAprovacao'.
            Output:
                This function has no output, instead, it caches the metrics
                found in its instance.
        """
        print('*** CommonItemsRatio ***')
        # Generate distinct items table
        distinct_items = items[['idPlanilhaItens', 'Item']]
        distinct_items = distinct_items.set_index('idPlanilhaItens')
        self.distinct_items = distinct_items.drop_duplicates()

        # Filtering items table
        items = items[['PRONAC', 'idSegmento', 'idPlanilhaItens', 'idPronac',
                       'UfItem', 'idProduto', 'cdCidade', 'cdEtapa']]

        ### TODO: OPTIMIZE PERFORMANCE.
        ### For now, using pronac as integer
        items[['PRONAC']] = items[['PRONAC']].astype(int)
        ####################################

        self.items = items.drop_duplicates()

        # Generating cache
        self.cache = {}
        self.cache['top_items'] = self._top_items(self.items)
        self.cache['metrics'] = self._top_items_metrics(self.items)

        self.dt_comprovacao = self._process_receipt_data(dt_comprovacao)

    def get_metrics(self, pronac, k=1.5):
        """
            This function receives a project identifier and a constant 'k' and
            verify if this project has an anomalous percentage of its items
            that belongs to the most common items of its segment, considering a
            gaussian distribution of this percentage for all projects of a same
            segment. The project is said outlier if its:
                (# of common items ratio) = (# of common items) / (# of items)
            is lower than (mean - k * std) for its segment. It also return the
            project '# of common items ratio' and its segment 'mean' and
            'standard deviation' for this metric. Besides that, this function
            returns a list of the uncommon items found in the project and a
            list of common items not found in the project.
            Input:
                pronac: the project identifier.
                k: constant that defines the threshold to verify if a project
                is an outlier.
            Output:
                A dictionary containing the keys: is_outlier, value, mean, std,
                uncommon_items, and common_items_not_in_project.
        """

        if not isinstance(pronac, str):
            raise ValueError('PRONAC type must be str')

        ### TODO: OPTIMIZE PERFORMANCE.
        ### For now, using pronac as integer
        pronac = int(pronac)
        ####################################

        pronac_items = self._get_pronac_data(pronac)

        items = self.items

        project = pronac_items.iloc[0]
        segment = project['idSegmento']
        seg_top_items = self._top_items_segment(segment)
        com_items_ratio = self._perc_items_in_top(items, pronac, seg_top_items)

        metrics = self.cache['metrics'][segment]
        threshold = metrics['mean'] - k * metrics['std']

        project_items = pronac_items
        project_items = project_items.drop(columns=['PRONAC', 'idSegmento'])
        project_items = project_items.set_index('idPlanilhaItens').index
        seg_top_items = seg_top_items.set_index('idPlanilhaItens').index

        uncommon_items = list(project_items.difference(seg_top_items))
        uncommon_items = self.distinct_items.loc[uncommon_items]
        uncommon_items = uncommon_items.to_dict()['Item']

        pronac_filter = items['PRONAC'] == pronac
        uncommon_items_filter = items['idPlanilhaItens'].isin(uncommon_items)
        items_filter = pronac_filter & uncommon_items_filter

        filtered_items = items[items_filter].drop_duplicates(subset='idPlanilhaItens')
        for index, item in filtered_items.iterrows():
            item_id = item['idPlanilhaItens']
            item_name = uncommon_items[item_id]
            item_salic_url = self._item_salic_url(item)
            has_receipt = self._item_has_receipt(item)
            uncommon_items[item_id] = {'name': item_name, 'salic_url': item_salic_url, 'has_receipt': has_receipt}

        com_items_not_in_proj = list(seg_top_items.difference(project_items))
        com_items_not_in_proj = self.distinct_items.loc[com_items_not_in_proj]
        com_items_not_in_proj = com_items_not_in_proj.to_dict()['Item']

        results = {}
        results['is_outlier'] = (com_items_ratio < threshold)
        results['value'] = com_items_ratio
        results['mean'] = metrics['mean']
        results['std'] = metrics['std']
        results['uncommon_items'] = uncommon_items
        results['common_items_not_in_project'] = com_items_not_in_proj

        return results

    def _item_salic_url(self, item_info):
        url_keys = [
            ('pronac', 'idPronac'),
            ('uf', 'uf'),
            ('product', 'produto'),
            ('county', 'idmunicipio'),
            ('item_id', 'idPlanilhaItem'),
            ('stage', 'etapa')
        ]

        url_values = {
            'pronac': item_info['idPronac'],
            'uf': item_info['UfItem'],
            'product': item_info['idProduto'],
            'county': item_info['cdCidade'],
            'item_id': item_info['idPlanilhaItens'],
            'stage': item_info['cdEtapa']
        }

        item_data = []
        for key, value in url_keys:
            item_data.append((value, url_values[key]))

        URL_PREFIX = '/prestacao-contas/analisar/comprovante'
        url = URL_PREFIX
        for key, value in item_data:
            url += '/' + str(key) + '/' + str(value)

        return url

    def _top_items(self, items, percentage=0.1):
        # Generating items occurrences table grouped by segment and item ID
        items = items.groupby(['idSegmento', 'idPlanilhaItens']).count()
        items = items.rename(columns={'PRONAC': 'itemOccurrences'})
        items = items.sort_values('itemOccurrences', ascending=False)
        items = items.reset_index(['idSegmento', 'idPlanilhaItens'])

        # Selecting only the 'percentage' most common items of each segment
        def items_filter(x):
            return x[None: max(2, int(len(x) * percentage))]
        top_items = items.groupby('idSegmento').apply(items_filter)
        top_items = top_items.reset_index(['idSegmento'], drop=True)
        top_items = top_items.set_index(['idSegmento'])

        return top_items

    def _top_items_metrics(self, items):
        top_items = self.cache['top_items']
        segments = top_items.index.unique()
        metrics = {}
        for segment in segments:
            top_items_seg = self._top_items_segment(segment)
            segment_projects = items[items['idSegmento'] == segment]
            segment_projects = segment_projects.drop_duplicates(['PRONAC'])
            segment_projects = segment_projects['PRONAC'].values

            # project metric value
            pmv = []
            for project in segment_projects:
                pmv += [self._perc_items_in_top(items, project, top_items_seg)]
            metrics[segment] = {
                'mean': np.mean(pmv),
                'std': np.std(pmv)
            }
        return metrics

    def _top_items_segment(self, segment):
        top_items_seg = self.cache['top_items'].loc[segment]
        top_items_seg = top_items_seg.reset_index(drop=1)
        top_items_seg = top_items_seg.drop(columns=['itemOccurrences'])
        return top_items_seg

    def _perc_items_in_top(self, items, pronac, top_items_segment):
        # Handle segments with no common items
        if len(top_items_segment) == 0:
            return 0

        # Generating the list of the project items
        project_items = items[items['PRONAC'] == pronac]
        project_items = project_items.drop(columns=['PRONAC', 'idSegmento'])
        project_items = project_items.values[:, 0]
        if len(project_items) == 0:
            return 1

        # Generating the number of items found in the list of the most
        # common segment items
        found_in_top = top_items_segment.isin(project_items)
        found_in_top = sum(found_in_top['idPlanilhaItens'])

        # Returning the percentage of project items in the list of the most
        # common segment items
        return found_in_top / len(project_items)


    def _item_has_receipt(self, item_info):
        item_identifier = str(item_info['idPronac']) + '/' + str(item_info['idPlanilhaItens'])
        return item_identifier in self.dt_comprovacao.index


    def _process_receipt_data(self, dt_comprovacao):
        dt_comprovacao = dt_comprovacao[['IdPRONAC', 'idPlanilhaItem']].astype(str)
        dt_comprovacao['pronac_planilha_itens'] = dt_comprovacao['IdPRONAC'] + '/' + dt_comprovacao['idPlanilhaItem']
        dt_comprovacao.set_index(['pronac_planilha_itens'], inplace=True)
        return dt_comprovacao

    def _get_pronac_data(self, pronac):
        __FILE__FOLDER = os.path.dirname(os.path.realpath(__file__))
        sql_folder = os.path.join(__FILE__FOLDER, os.pardir, os.pardir, os.pardir)
        sql_folder = os.path.join(sql_folder, 'data', 'scripts')

        datasource = DataSource()
        path = os.path.join(sql_folder, 'planilha_orcamentaria.sql')

        pronac_dataframe = datasource.get_dataset(path, pronac=pronac)
        pronac_dataframe = pronac_dataframe[['PRONAC', 'idSegmento', 'idPlanilhaItens', 'idPronac',
            'UfItem', 'idProduto', 'cdCidade', 'cdEtapa']]

        return pronac_dataframe