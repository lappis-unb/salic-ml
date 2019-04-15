metrics_name_map = {
    'number_of_items': 'itens_orcamentarios',
    'to_verify_funds': 'valor_a_ser_comprovado',
    'verified_approved': 'comprovantes_acima_de_50',
    'total_receipts': 'comprovantes_pagamento',
    'new_providers': 'novos_fornecedores',
    'proponent_projects': 'projetos_mesmo_proponente',
    'check_receipts': 'comprovantes_de_cheque',
    'money_receipts': 'comprovantes_de_saque',
    'transfer_receipts': 'comprovantes_de_transferencia',
}

default_metrics = {
  "itens_orcamentarios": {
      "valor": 0,
      "valor_valido": False,
      "is_outlier": False,
      "minimo_esperado": 0,
      "maximo_esperado": 0,
  },
  "valor_a_ser_comprovado": {
      "valor": 0,
      "valor_valido": False,
      "is_outlier": False,
      "minimo_esperado": 0,
      "maximo_esperado": 0,
  },
  "comprovantes_acima_de_50": {
      "valor": 0,
      "valor_valido": False,
      "is_outlier": False,
      "minimo_esperado": 0,
      "maximo_esperado": 0,
      "data": {
        "lista_de_comprovantes": None,
      }
  },
  "comprovantes_pagamento": {
      "valor": 0,
      "valor_valido": False,
      "is_outlier": False,
      "minimo_esperado": 0,
      "maximo_esperado": 0,
  },
  "projetos_mesmo_proponente": {
      "valor": 0,
      "valor_valido": False,
      "is_outlier": False,
      "minimo_esperado": 0,
      "maximo_esperado": 0,
      "data": {
        "projetos_submetidos": None,
      }
  },
  "novos_fornecedores": {
      "valor": 0,
      "valor_valido": False,
      "is_outlier": False,
      "minimo_esperado": 0,
      "maximo_esperado": 0,
      "data": {
        "lista_de_novos_fornecedores": None,
      }
  },
  "comprovantes_de_cheque": {
      "valor": 0,
      "valor_valido": False,
      "is_outlier": False,
      "minimo_esperado": 0,
      "maximo_esperado": 0,
      "data": {
        "comprovantes": None,
      }
  },
  "comprovantes_de_saque": {
       "valor": 0,
       "valor_valido": False,
       "is_outlier": False,
       "minimo_esperado": 0,
       "maximo_esperado": 0,
       "data": {
         "comprovantes": None,
       }
   },
  "comprovantes_de_transferencia": {
       "valor": 0,
       "valor_valido": False,
       "is_outlier": False,
       "minimo_esperado": 0,
       "maximo_esperado": 0,
       "data": {
         "comprovantes": None,
       }
   },
}
