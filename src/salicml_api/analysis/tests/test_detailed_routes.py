import json
from .utils import load_json

PROJECT_DETAIL_URL_132955 = '/v1/projects/132955/details/'
PROJECT_NAME_132955 = 'Brasil contemporâneo: economia e cultura - Milagre econômico e recessão nos anos 70/80: décadas de chumbo, contestação e rock brazuca'

def test_detail_url(db, api_client):
    response = api_client.get(PROJECT_DETAIL_URL_132955)
    json_data = load_json(response)

    assert(response.status_code == 200)
   
    assert(json_data['pronac'] == '132955')
    assert(json_data['nome'] == PROJECT_NAME_132955)
    
    assert('AdmissibilityIndicator' in json_data['indicadores'])
    assert('FinancialIndicator' in json_data['indicadores'])

def test_financial_indicator_content(db, api_client):
    response = api_client.get(PROJECT_DETAIL_URL_132955)
    json_data = load_json(response)
    indicators = json_data['indicadores']
    financial_data = indicators['FinancialIndicator']

    assert(financial_data['valor'] == 3.2)
    assert('comprovante_saque' in financial_data['metricas'])
    assert('comprovante_cheque' in financial_data['metricas'])
    assert('comprovante_transferencia' in financial_data['metricas'])
    assert('comprovante_pagamento' in financial_data['metricas'])
    assert('itens_orcamentarios' in financial_data['metricas'])
    assert('novos_fornecedores' in financial_data['metricas'])
    assert('comprovantes_acima_50' in financial_data['metricas'])
    assert('projetos_mesmo_proponente' in financial_data['metricas'])
    assert('valor_a_ser_comprovado' in financial_data['metricas'])

def test_admissibility_indicator_content(db, api_client):
    response = api_client.get(PROJECT_DETAIL_URL_132955)
    json_data = load_json(response)
    indicators = json_data['indicadores']
    admissibility_data = indicators['AdmissibilityIndicator']

    assert(admissibility_data['valor'] == 0.0)
    assert('itens_comuns_e_incomuns_por_segmento' in admissibility_data['metricas'])

def test_itens_comuns_e_incomuns_por_segmento(db, api_client):
    response = api_client.get(PROJECT_DETAIL_URL_132955)
    json_data = load_json(response)
    indicators = json_data['indicadores']
    admissibility_data = indicators['AdmissibilityIndicator']
    itens_comuns_e_incomuns_por_segmento = admissibility_data['metricas']['itens_comuns_e_incomuns_por_segmento']
    data = itens_comuns_e_incomuns_por_segmento['data']

    assert(itens_comuns_e_incomuns_por_segmento['valor'] == "0.17391304347826086")
    assert(itens_comuns_e_incomuns_por_segmento['valor_valido'] == True)
    assert(itens_comuns_e_incomuns_por_segmento['is_outlier'] == False)
    assert(itens_comuns_e_incomuns_por_segmento['minimo_esperado'] == 0)
    assert(itens_comuns_e_incomuns_por_segmento['maximo_esperado'] == 0.28728639746373064)

    assert('items_incomuns' in data)
    assert('items_comuns_que_o_projeto_nao_possui' in data)
    
    assert(isinstance(data['items_incomuns'], list))
    assert(isinstance(data['items_comuns_que_o_projeto_nao_possui'], list))
    
    assert(isinstance(data['items_incomuns'][0], list))
    assert(isinstance(data['items_comuns_que_o_projeto_nao_possui'][0], list))
    
    assert(len(data['items_incomuns']) == 34)
    assert(len(data['items_comuns_que_o_projeto_nao_possui']) == 2)
    
    assert(isinstance(data['items_incomuns'][0][0], int))
    assert(isinstance(data['items_incomuns'][0][1], dict))
    
    assert('name' in data['items_incomuns'][0][1])
    assert('salic_url' in data['items_incomuns'][0][1])
    assert('has_recepit' in data['items_incomuns'][0][1])

    assert(isinstance(data['items_comuns_que_o_projeto_nao_possui'][0][0], int))
    assert(isinstance(data['items_comuns_que_o_projeto_nao_possui'][0][1], str))


def test_comprovante_saque(db, api_client):
    response = api_client.get(PROJECT_DETAIL_URL_132955)
    json_data = load_json(response)
    comprovante_saque = json_data['indicadores']['FinancialIndicator']['metricas']['comprovante_saque']

    assert(comprovante_saque['valor'] == "0")
    assert(comprovante_saque['data'] == {'comprovantes': []})
    assert(comprovante_saque['valor_valido'] == True)
    assert(comprovante_saque['is_outlier'] == False)
    assert(comprovante_saque['minimo_esperado'] == 0)
    assert(comprovante_saque['maximo_esperado'] == 0)

def test_comprovante_cheque(db, api_client):

    response = api_client.get(PROJECT_DETAIL_URL_132955)
    json_data = load_json(response)
    comprovante_cheque = json_data['indicadores']['FinancialIndicator']['metricas']['comprovante_cheque']

    assert(comprovante_cheque['valor'] == "0")
    assert(comprovante_cheque['data'] == {'comprovantes': []})
    assert(comprovante_cheque['valor_valido'] == True)
    assert(comprovante_cheque['is_outlier'] == False)
    assert(comprovante_cheque['minimo_esperado'] == 0)
    assert(comprovante_cheque['maximo_esperado'] == 0)


def test_comprovante_transferencia(db, api_client):
    response = api_client.get(PROJECT_DETAIL_URL_132955)
    json_data = load_json(response)
    comprovante_transferencia = json_data['indicadores']['FinancialIndicator']['metricas']['comprovante_transferencia']

    assert(comprovante_transferencia['valor'] == "0")
    assert(comprovante_transferencia['data'] == {'comprovantes': []})
    assert(comprovante_transferencia['valor_valido'] == True)
    assert(comprovante_transferencia['is_outlier'] == False)
    assert(comprovante_transferencia['minimo_esperado'] == 0)
    assert(comprovante_transferencia['maximo_esperado'] == 0)

def test_comprovante_pagamento(db, api_client):
    response = api_client.get(PROJECT_DETAIL_URL_132955)
    json_data = load_json(response)
    comprovante_pagamento = json_data['indicadores']['FinancialIndicator']['metricas']['comprovante_pagamento']

    assert(comprovante_pagamento['valor'] == "10")
    assert(comprovante_pagamento['data']['maximo_esperado'] == 35.925945419092514)
    assert(comprovante_pagamento['data']['minimo_esperado'] == 0)
    assert(comprovante_pagamento['valor_valido'] == True)
    assert(comprovante_pagamento['is_outlier'] == False)
    assert(comprovante_pagamento['minimo_esperado'] == 0)
    assert(comprovante_pagamento['maximo_esperado'] == 35.925945419092514)

def test_itens_orcamentarios(db, api_client):
    pass

def test_novos_fornecedores(db, api_client):
    pass

def test_comprovantes_acima_50(db, api_client):
    response = api_client.get(PROJECT_DETAIL_URL_132955)
    json_data = load_json(response)
    comprovantes_acima_50 = json_data['indicadores']['FinancialIndicator']['metricas']['comprovantes_acima_50']
    data = comprovantes_acima_50['data']

    assert(comprovantes_acima_50['valor'] == '0')
    assert(comprovantes_acima_50['valor_valido'] == True)
    assert(comprovantes_acima_50['is_outlier'] == False)
    assert(comprovantes_acima_50['minimo_esperado'] == 0)
    assert(comprovantes_acima_50['maximo_esperado'] == 0)

    assert(data['maximo_esperado'] == 0)
    assert(data['minimo_esperado'] == 0)
    assert(data['link_da_planilha'] == "http://salic.cultura.gov.br/projeto/#/132955/relacao-de-pagamento")
    assert(isinstance(data['lista_de_comprovantes'], list))
    

def test_projetos_mesmo_proponente(db, api_client):
    response = api_client.get(PROJECT_DETAIL_URL_132955)
    json_data = load_json(response)
    projetos_mesmo_proponente = json_data['indicadores']['FinancialIndicator']['metricas']['projetos_mesmo_proponente']
    data = projetos_mesmo_proponente['data']
    projetos_analisados = data['projetos_analizados']


    assert(projetos_mesmo_proponente['valor'] == "0")
    assert(projetos_mesmo_proponente['valor_valido'] == True)
    assert(projetos_mesmo_proponente['is_outlier'] == False)
    assert(projetos_mesmo_proponente['minimo_esperado'] == 0)
    assert(projetos_mesmo_proponente['maximo_esperado'] >= 0)

    assert(isinstance(data['cpf_cnpj'], str))
    assert(isinstance(data['projetos_submetidos'], list))
    assert(isinstance(projetos_analisados, dict))
    assert(projetos_analisados['number_of_projects'] == 1)
    assert(projetos_analisados['pronacs_of_this_proponent'] == ["132955"])


def test_valor_a_ser_comprovado(db, api_client):
    response = api_client.get(PROJECT_DETAIL_URL_132955)
    json_data = load_json(response)
    valor_a_ser_comprovado = json_data['indicadores']['FinancialIndicator']['metricas']['valor_a_ser_comprovado']
    data = valor_a_ser_comprovado['data']

    assert(valor_a_ser_comprovado['valor'] == "25100.0")
    assert(valor_a_ser_comprovado['valor_valido'] == True)
    assert(valor_a_ser_comprovado['is_outlier'] == True)
    assert(valor_a_ser_comprovado['minimo_esperado'] == 0)
    assert(valor_a_ser_comprovado['maximo_esperado'] == 0)
    assert(data['valor_captado'] == 100000.0)
    assert(data['valor_comprovado'] == 74900.0)
    assert(data['minimo_esperado'] == 0)
    
