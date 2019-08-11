# Criando nova métrica
Para que a nova métrica seja criada, deve-se definir os seguintes aspectos:
- Algoritmo
- Planilhas a serem utilizadas no cálculo
- Categoria da métrica (Financeira, Admissibilidade, ...)

Após bem definidos, pode-se executar as seguintes etapas (definidas no restante do documento):
- Inserir o cálculo no módulo de algoritmos
- Alimentar o algoritmo com dados
- Adicionar a nova métrica no pipeline de treinamento

## Onde inserir o algoritmo
Os algoritmos já existentes podem ser encontrados em ```/src/salicml/metrics/finance```

Para adicionar um novo algoritmo, crie um arquivo com o nome da métrica na pasta ```finance``` e, dentro dele uma função decorada da seguinte maneira:

**src/salicml/metrics/finance/nova_metrica.py**:
```py
@metrics.register('categoria_da_metrica')
def nova_metrica(pronac, dt):
    """
    Explicação da métrica
    """
    
    # Algoritmo
    # ...

    result = {
        'valor': 10.0
    }

    return result
```

O decorador garante que a métrica será registrada no módulo que gerencia o treinamento. Os parâmetros ```pronac``` e ```dt``` são definidos por padrão e fazem parte do pipeline do cálculo.

O retorno da função deve ser um dicionário contendo os dados que estarão disponíveis na resposta em json na API.

## Como alimentar o algoritmo com dados

Todo o salic-ml funciona a partir de dados que são disponibilizados pelo módulo ```salicml.data```. O acesso aos dataframes é feito da seguinte maneira:

**src/salicml/metrics/finance/nova_metrica.py**:
```py
from salicml.data import data

@metrics.register('categoria_da_metrica')
def nova_metrica(pronac, dt):
    """
    Explicação da métrica
    """
    
    # Algoritmo
    # ...
    dataframe_customizado = data.planilha_aprovacao_comprovacao_customizada
    # ...

    result = {
        'valor': 10.0
    }

    return result

@data.lazy('planilha_aprovacao_comprovacao')
def planilha_aprovacao_comprovacao_customizada(df):
    COLUMNS = ["PRONAC", "Item", "vlAprovado", "vlComprovacao"]
    return df[COLUMNS]
```

Com o módulo importado, deve-se apresentar uma função com algumas características:
- Decorada com o ```@data.lazy('nome da planilha a ser carregada')```
- Nomeada com o mesmo nome da chamada da função para se carregar os dados
- Retornando um dataframe

Para acessar o dado customizado, basta chamar 
```py
data.nome_da_funcao_criada
```

## Como adicionar a nova métrica no pipeline de treinamento

Para incluir o arquivo ```nova_metrica.py``` no pipeline de treinamento, basta adicionar o texto 'nova_metrica' nos seguintes locais:

**src/salicml_api/analysis/models/financial.py**:

Há várias métricas para cada planilha. Coloque a nova_metrica no campo mais adequado. No exemplo abaixo, temos o caso no qual a métrica tem a planilha comprovação como base.
```py
METRICS = {
        "planilha_comprovacao": [
            "comprovante_cheque",
            "comprovante_transferencia",
            "comprovante_saque",
            "novos_fornecedores",
            "comprovante_pagamento",
            "comprovantes_acima_50",
            "nova_metrica", # Métrica adicionada
        ],
        "planilha_projetos": ["projetos_mesmo_proponente"],
        "planilha_captacao": ["valor_a_ser_comprovado"],
        "planilha_orcamentaria": ["itens_orcamentarios"],
    }
```

Para o cálculo do score global do projeto, usamos um algoritmo de pesos no qual cada métrica possui um peso específico no resultado final. Portanto, deve-se inserir o peso da nova métrica:

```py
@property
    def metrics_weights(self):
        return {
            "itens_orcamentarios": 1,
            "valor_a_ser_comprovado": 5,
            "projetos_mesmo_proponente": 2,
            "novos_fornecedores": 1,
            "comprovantes_acima_50": 2,
            "comprovante_transferencia": 5,
            "comprovante_saque": 5,
            "comprovante_cheque": 1,
            "valor_comprovado": 0,
            "itens_comuns_e_incomuns_por_segmento": 0,
            "comprovante_pagamento": 0,
            "items_prices": 0,
            "nova_metrica": 2, # Métrica adicionada
        }
```

**src/salicml_api/analysis/utils.py**:

Exite um arquivo ```utils.py``` no qual estão presentes os seguintes objetos:
- Lista de métricas a serem entregues para o usuário que consultar a API
- Conteúdo default de cada métrica para ser usado caso não for possível calculá-la para algum projeto

Deve-se inserir, também, a 'nova_metrica' nestes objetos:

```py
financial_metrics_names = [
    'itens_orcamentarios',
    'valor_a_ser_comprovado',
    'comprovantes_acima_50',
    'comprovante_pagamento',
    'novos_fornecedores',
    'projetos_mesmo_proponente',
    'comprovante_cheque',
    'comprovante_saque',
    'comprovante_transferencia',
    'itens_comuns_e_incomuns_por_segmento'
    'nova_metrica' # Métrica adicionada
]

default_financial_metrics = {
    # ...
    "nova_metrica": {
        "valor": 10, # Valor padrão
        "valor_valido": False, # Importante manter False para indicar que este não é um valor calculado
        "is_outlier": False,
        "minimo_esperado": 0,
        "maximo_esperado": 0,
        "data": {"valor": 10} # Data padrão (varia de acordo com a métrica)
    },
    # ...
}
```

**src/salicml/metrics/finance/__init__.py**:

Por fim, deve-se inserir a nova métrica na lista de exports do módulo finance para que ela fique disponível no pipeline de cálculo:
```py
# flake8: noqa
from .comprovante_por_operacao import comprovante_cheque, comprovante_transferencia, comprovante_saque
from .valor_aprovado import valor_aprovado
from .itens_comuns_e_incomuns_por_segmento import itens_comuns_e_incomuns_por_segmento
from .preco_itens import preco_itens
from .novos_fornecedores import novos_fornecedores
from .itens_orcamentarios import itens_orcamentarios
from .projetos_mesmo_proponente import projetos_mesmo_proponente
from .valor_captado import valor_captado
from .comprovantes_pagamento import comprovante_pagamento
from .valor_comprovado import valor_comprovado
from .comprovantes_acima_50 import comprovantes_acima_50
from .valor_a_ser_comprovado import valor_a_ser_comprovado
from .nova_metrica import nova_metrica # Métrica adicionada
```

Com estas alterações, deve ser possível observar os resultados da nova métrica logo após o treinamento.