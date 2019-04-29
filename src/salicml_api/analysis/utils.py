metrics_name_map = {
    'itens_orcamentarios': 'itens_orcamentarios',
    'valor_a_ser_comprovado': 'valor_a_ser_comprovado',
    'comprovantes_acima_50': 'comprovantes_acima_de_50',
    'comprovante_pagamento': 'comprovantes_pagamento',
    'novos_fornecedores': 'novos_fornecedores',
    'projetos_mesmo_proponente': 'projetos_mesmo_proponente',
    'comprovante_cheque': 'comprovantes_de_cheque',
    'comprovante_saque': 'comprovantes_de_saque',
    'comprovante_transferencia': 'comprovantes_de_transferencia',
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
        "link_da_planilha": "#",
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
