import os
import pandas as pd
import numpy as np

from core.data_handler.data_source import DataSource

class NewProviders():
    """ TODO
    """
    usecols = ['PRONAC', 'IdPRONAC', 'nrCNPJCPF', 'DataProjeto', 'idPlanilhaAprovacao',
               'Item', 'nmFornecedor', 'idSegmento', 'UF', 'cdProduto', 'cdCidade',
               'idPlanilhaItem', 'cdEtapa']

    def __init__(self, dt_comprovacao):
        """ TODO
        """
        print('*** NewProviders ***')
        assert isinstance(dt_comprovacao, pd.DataFrame)

        self.dt_comprovacao = dt_comprovacao[NewProviders.usecols].copy()
        self._train()

    def item_salic_url(self, item_info):
        url_keys = [
            ('pronac', 'idPronac'),
            ('uf', 'uf'),
            ('product', 'produto'),
            ('county', 'idmunicipio'),
            ('item_id', 'idPlanilhaItem'),
            ('stage', 'etapa')
        ]

        url_values = {
            'pronac': item_info['IdPRONAC'],
            'uf': item_info['UF'],
            'product': item_info['cdProduto'],
            'county': item_info['cdCidade'],
            'item_id': item_info['idPlanilhaItem'],
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

    def get_metrics(self, pronac):
        """ TODO
        """
        if not isinstance(pronac, str):
            raise ValueError('PRONAC type must be str')

        items = self._get_pronac_data(pronac)

        response = {}
        new_providers = {}
        pronac_segment = None

        for index, row in items.iterrows():
            cnpj = row['nrCNPJCPF']
            cnpj_count = self.providers_count.get(cnpj, 0)
            pronac_segment = row['idSegmento']

            if cnpj_count <= 1:
                item_id = row['idPlanilhaAprovacao']
                item_name = row['Item']
                provider_name = row['nmFornecedor']

                new_providers.setdefault(cnpj, {})
                new_providers[cnpj].setdefault('items', {})
                new_providers[cnpj].setdefault('name', provider_name)

                new_providers[cnpj]['items'].setdefault(item_id, {})
                new_providers[cnpj]['items'][item_id]['name'] = item_name

                item_info = row
                new_providers[cnpj]['items'][item_id]['salic_url'] = self.item_salic_url(item_info)
                new_providers[cnpj]['items'][item_id]['has_receipt'] = True

        new_providers_percentage = len(new_providers) / len(
            items['nrCNPJCPF'].unique())

        response['new_providers'] = new_providers
        response['new_providers_percentage'] = new_providers_percentage
        response['segment_average_percentage'] = \
            self.segments_average[pronac_segment]
        response['is_outlier'] = \
            new_providers_percentage > self.segments_average[pronac_segment]
        response['all_projects_average_percentage'] = self.all_projects_average

        return response

    def _train(self):
        """ TODO
        """
        self._set_projects_groupby()
        self._set_providers_count()
        self._train_average_percentage()

    def _set_projects_groupby(self):
        self.projects = self.dt_comprovacao.groupby('PRONAC')

    def _set_providers_count(self):
        self.providers_count = {}

        for pronac, items in self.projects:
            cnpjs = items['nrCNPJCPF'].unique()

            for cnpj in cnpjs:
                count = self.providers_count.setdefault(cnpj, 0)
                self.providers_count[cnpj] = count + 1

    def _train_average_percentage(self):
        segment_percentages = {}
        all_projects_percentages = []

        for pronac, items in self.projects:
            cnpjs = items.nrCNPJCPF.unique()
            new_providers = 0
            for cnpj in cnpjs:
                cnpj_count = self.providers_count.get(cnpj, 0)
                if cnpj_count <= 1:  # if cnpj_count == 1
                    # then the current pronac is the only one with the given provider
                    new_providers += 1

            id_segmento = items.iloc[0]['idSegmento']
            segment_percentages.setdefault(id_segmento, [])
            providers_percent = new_providers / cnpjs.size
            segment_percentages[id_segmento].append(providers_percent)
            all_projects_percentages.append(providers_percent)

        self.segments_average = {}
        for segment_id, percentages in segment_percentages.items():
            mean = np.mean(percentages)
            self.segments_average[segment_id] = mean

        self.all_projects_average = np.mean(all_projects_percentages)

    def get_averages(self):
        averages = {
            'segments_average': self.segments_average,
            'all_projects_average': self.all_projects_average,
        }
        return averages

    def _get_pronac_data(self, pronac):
        __FILE__FOLDER = os.path.dirname(os.path.realpath(__file__))
        sql_folder = os.path.join(__FILE__FOLDER, os.pardir, os.pardir, os.pardir)
        sql_folder = os.path.join(sql_folder, 'data', 'scripts')

        datasource = DataSource()
        path = os.path.join(sql_folder, 'planilha_comprovacao.sql')

        pronac_dataframe = datasource.get_dataset(path, pronac=pronac)
        pronac_dataframe = pronac_dataframe[NewProviders.usecols]

        dataframe_grouped_by = pronac_dataframe.groupby('PRONAC')

        return dataframe_grouped_by.get_group(pronac)