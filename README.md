Salic - Machine Learning
========================

O salic-ml é um projeto aberto que utiliza inteligência artificial para otimizar e automatizar o ciclo de vida de projetos culturais viabilizados pela [Lei Rouanet](http://rouanet.cultura.gov.br/) e acompanhados pelo sistema [Salic](http://salic.cultura.gov.br/).

O projeto se iniciou em março de 2018, em uma parceria entre o [LAPPIS](https://fga.unb.br/lappis) e o Ministério da Cultura (MinC). A primeira fase do projeto teve foco no levantamento do ciclo de vida de projetos culturais e em seus principais pontos de melhoria. Em julho de 2018 foi iniciada a [Fase 2](https://github.com/lappis-unb/salic-ml/wiki/2018.07.17-Revisão-e-Planejamento) do projeto e foram definidas as primeiras metas e entregas de curto e médio prazo. Detalhes de pesquisa e planejamento estão disponíveis da seção [Wiki](https://github.com/lappis-unb/salic-ml/wiki) e discussões e principais ideias podem ser encontradas na seção [Issues](https://github.com/lappis-unb/salic-ml/issues).

A parceria contou com a contribuição de diversos funcionários do MinC e do LAPPIS e entre os idealizadores e principais contribuidores, é possível citar: [Carla Rocha](https://github.com/RochaCarla) e
[Fábio Mendes](https://github.com/fabiommendes) (coordenadores do LAPPIS) e
[Joênio Costa](https://github.com/joenio),
[Luciano Prestes](https://github.com/LucianoPC),
[Victor Moura](https://github.com/victorcmoura),
[Eduardo Nunes](https://github.com/eduardonunes2525),
[Fabíola Malta](https://github.com/fabiolamfleury),
[Rodrigo Oliveira](https://github.com/rodrigocam),
[Pablo Diego](https://github.com/pablodiegoss),
[João Guilherme](https://github.com/joaaogui),
[Daniel Guerreiro](https://github.com/danielgs83),
[Felipe Duerno](https://github.com/Duerno),
[Alexandre Torres](https://github.com/AlexandreTK),
[Lucas Mattioli](https://github.com/Mattioli),
[Marlon Mendes](https://github.com/marlonbymendes),
[Ricardo Poppi](https://github.com/ricardopoppi) e
[Rodrigo Maia](https://github.com/rodmaia2099).


O projeto salic-ml é dividido em uma API REST para disponibilização de indicadores a respeito dos projetos submetidos para a lei rouanet e um pacote de algoritmos utilizados para o cálculo de métricas.


Contribuição
------------

Para acompanhar nosso planejamento por sprint e a longo prazo, instale o plugin [ZenHub](https://www.zenhub.com/) para o GitHub e acesse a aba que fica ao lado da aba de Pull requests neste repositório.

#### Requisitos

Existem duas maneiras de executar este projeto, sendo uma com ambiente local e outra utilizando [Docker](https://www.docker.com/).

Para um ambiente de desenvolvimento local, você irá precisar da versão 3.6, ou superior, do [Python](https://www.python.org/downloads/release/python-360/). Além disso, é recomendado que você possua instalado o [virtualenv](https://virtualenv.pypa.io/en/latest/), um ótimo isolador de ambientes Python e junto com ele o [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/).


#### Instalação

Para ambientes locais, você pode seguir os seguintes passos:

 1. Criar ambiente isolado com virtualenv
    ```shell
    $ mkvirtualenv salicml -p /usr/bin/python3.6
    ```

 2. Instalar as dependências dentro do ambiente virtual
    ```shell
    $ python setup.py develop
    ```

Para ambientes docker, basta executar o docker-compose:

```shell
    $ sudo docker-compose -f docker/docker-compose.yml up
```

#### Como lidamos com os dados

Nosso algoritmos utilizam a biblioteca [pandas](https://pandas.pydata.org/), uma excelente biblioteca para lidar com dados em formato de tabela. Nosso flow de trabalho é:
    
 1. Gerar pandas dataframes a partir de um banco de dados.
 
 2. Gerar arquivos `pickle` comprimidos destes dataframes.

 3. Acessar estes arquivos `pickle` com nossa api de dados:
    ```python
    from salicml.data import data
    
    data.planilha_orcamentaria
    ```

Todos os dataframes em forma de arquivos `pickle`, são armazenados neste repositório da pasta `data/raw`, e ficam disponíveis para acesso via Python pela nossa api de dados.

#### Reprodução de pesquisas

Após a instalação, execute o seguinte comando a partir da raiz do diretório:

    $ jupyter-notebook

Este comando abrirá uma página o navegador. A partir deste navegador, entre no diretório `research/notebooks` e abra o notebook desejado. Estrutura de pastas para armazenar os notebooks de estudo e pesquisa:

* **Doing:** notebooks que estão sendo desenvolvidos.

* **Exploratory:** notebooks usados para exploração. Pode conter "rascunhos",
notebooks não finalizados ou finalizados mas com pouca relevância.
Seguem o formato <Descrição do Notebook>-<Versão>.

* **Report:** Notebooks com os resultados das pesquisas. Esta pasta contém as
versões de notebooks estáveis e atualizados das pesquisas realizadas.


#### Tasks comuns

Este projeto utiliza `tasks` do [invoke](http://www.pyinvoke.org/) para automatizar tarefas.

 - Subir o servidor de desenvolvimento da API:

    ```shell
    $ inv run
    ```

 - Popular o banco de dados local com os projetos do banco de dados remoto:

    ```shell
    $ inv update-models
    ```

 - Baixar os arquivos `pickles`:

    ```shell
    $ inv get-pickles
    ```

 - Gerar dataframes de teste

    ```shell
    $ inv gen-test-df
    ```

 - Transformar arquivos `csv` em `pickles`:

    ```shell
    $ inv pickle
    ```

- Treinar os algoritmos de cálculo de métricas:

    ```shell
    $ inv train-metrics
    ```

- Gerar um arquivo `pickle` a partir de uma consulta de banco:

    ```shell
    $ inv run-sql
    ```

- Criar migrações:

    ```shell
    $ inv make
    ```

- Executar migrações:

    ```shell
    $ inv migrate
    ```

- Alias para python `manage.py`:

    ```shell
    $ inv manager
    ```

#### Outros comandos

- Para que tenha acesso a lista de comandos digite em seu terminal:
    
    ```
     $ invoke --list
    ```
 - Para ler a descrição de um comando específico (exemplo comando run):

    ```
     $ invoke --help run
    ```

#### Primeiros passos

Aqui são descritos os passos necessários para quem acabou de instalar o ambiente:

 1. Baixar os arquivos `pickle`
     ```shell
    $ inv get-pickles
    ```
 2. Popular o banco com projetos
    ```shell
     $ inv update-models
    ```
 3. Treinar as métricas
    ```shell
    $ inv train-metrics
    ```
 4. Subir o servidor 
    ```shell
    $ inv run
    ```

Licença
-------

O salic-ml é desenvolvido sob a [Licença GPLv3](LICENSE.md).
