**Links rápidos**
> [Questões de pesquisa](#sobre-a-pesquisa)
>
> [Pacotes do python para pesquisa](#dependências-do-python)


# Sobre a pesquisa

As questões de pesquisa estão sempre relacionadas aos nossos objetivos maiores dentro do Salic:
  - Automatizar subprocessos da fase de admissão de propostas
  - Automatizar subprocessos da fase de prestação de contas
  - Categorização de projetos

O processo para investigar as questões de pesquisa geralmente envolve: identificar um conjunto significativo de dados, coletá-los, visualização dos dados (por meio de gráficos, por exemplo), cálculo de estatísticas (média, mediana, desvio padrão por ex.), elicitar e investigar hipóteses e enfim propor alguma solução/aplicação e calcular sua eficácia.

**Fase de admissibilidade dos projetos**

Questões de pesquisa na fase de admissão:
- O que faz o preço unitário de um item ser aprovado?
- Qual o conjunto de dados que influenciam a decisão de aprovar ou não um dado item?
- Qual a relação de outros itens em aprovar ou não um item em específico?
- Como calcular a eficácia de uma solução que prevê a aprovação ou não de um item?

**Fase de prestação de contas**

**Categorização de projetos**

# Dependências do python

**Versão do python e bibliotcas utilizadas**

Recomendamos utilizar o `python3` (python 3.3 ou superior).
As bibliotecas do python utilizadas para fazer estão disponíves no arquivo [requirements.txt](https://github.com/lappis-unb/salic-ml/blob/master/research/requirements.txt).

**Instalando biblitecas**

Recomendamos utilizar o `pip3` como gerenciador de pacotes python.

1. `$ git clone https://github.com/lappis-unb/salic-ml` (caso ainda não tenha clonado o repositório)
2. `$ cd research/` (diretório de pesquisa)
3. `$ pip3 install -f requirements.txt`
