import json
from .utils import load_json

PROJECT_DETAIL_URL_132955 = '/v1/projects/132955/details/'
PROJECT_NAME_132955 = '''
    Brasil contemporâneo: economia e cultura - Milagre econômico e 
    recessão nos anos 70/80: décadas de chumbo, contestação e rock brazuca
    '''

def test_detail_url(db, api_client):
    response = api_client.get(PROJECT_DETAIL_URL_132955)
    json_data = load_json(response)

    assert(response.status_code == 200)
    assert(json_data['pronac'] == '132955')
    assert(json_data['nome'] == PROJECT_NAME_132955)
    assert('AdmissibilityIndicator' in json_data['indicadores'])
    assert('FinancialIndicator' in json_data['indicadores'])

def test_financial_indicator_content(db, api_client):
    pass

def test_admissibility_indicator_content(db, api_client):
    pass

def test_itens_comuns_e_incomuns_por_segmento(db, api_client):
    pass

def test_comprovante_saque(db, api_client):
    pass

def test_comprovante_cheque(db, api_client):
    pass

def test_comprovante_transferencia(db, api_client):
    pass

def test_comprovante_pagamento(db, api_client):
    pass

def test_itens_orcamentarios(db, api_client):
    pass

def test_novos_fornecedores(db, api_client):
    pass

def test_comprovantes_acima_50(db, api_client):
    pass

def test_projetos_mesmo_proponente(db, api_client):
    pass

def test_valor_a_ser_comprovado(db, api_client):
    pass