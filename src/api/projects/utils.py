### FORMAT FOR METRICS
metrics_name_map = {
    'number_of_items': 'itens_orcamentarios',
    'raised_funds': 'valor_captado', # DEPRECATED
    'approved_funds': 'valor_aprovado', # DEPRECATED
    'common_items_ratio': 'itens_orcamentarios_fora_do_comum',
    'total_receipts': 'comprovantes_pagamento',
    'new_providers': 'novos_fornecedores',
    'proponent_projects': 'projetos_mesmo_proponente',
    'item_prices': 'precos_acima_media',
    'verified_approved': 'comprovantes_acima_de_50',
    'to_verify_funds': 'valor_a_ser_comprovado',
}


{
  "itens_orcamentarios":{
      "valor": 0,
      "valor_valido": False,
      "is_outlier": False,
      "minimo_esperado": 0,
      "maximo_esperado": 0,
  },
  "valor_a_ser_comprovado":{
      "valor": 0,
      "valor_valido": False,
      "is_outlier": False,
      "minimo_esperado": 0,
      "maximo_esperado": 0,
  },
  "comprovantes_acima_de_50":{
      "valor": 0,
      "valor_valido": False,
      "is_outlier": False,
      "minimo_esperado": 0,
      "maximo_esperado": 0,
      "data": {
        "lista_de_comprovantes": None,
      }
  },
  "comprovantes_pagamento":{
      "valor": 0,
      "valor_valido": False,
      "is_outlier": False,
      "minimo_esperado": 0,
      "maximo_esperado": 0,
  },
}
