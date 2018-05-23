Salic - Machine Learning
========================

Time atual:
* Prof. Felipe Duerno
* Luciano Prestes
* Marlon Mendes
* Alexandre Torres

Instalação
----------
Instale o Git Large File Storage (git-lfs) pelo link a baixo ou pela linha de
comando

https://git-lfs.github.com/

    $ apt install git-lfs

Após instalar o pacote é necessário executar o comando de instalação do git-lfs

    $ git lfs install

Clone o repositório

    $ GIT_LFS_SKIP_SMUDGE=1 git clone https://github.com/lappis-unb/salic-ml.git

É necessário definir o valor do GIT\_LFS\_SKIP\_SMUDGE como 1, para que ao
clonar o repositório o git não baixe automaticamente todos os arquivos grandes

Atualizar uma branch, quando for usar o comando "git pull" e não quiser baixar
todos os arquivos grandes, também é necessário definir o valor do
GIT\_LFS\_SKIP\_SMUDGE como 1

    $ GIT_LFS_SKIP_SMUDGE=1 git pull

Instale o python e o pip

    $ sudo apt install python3 python3-dev python3-pip

Instale o virtualenvwrapper e crie um virtualenv para o projeto

    $ pip install virtualenvwrapper
    $ mkvirtualenv -p /usr/bin/python3 salic-ml

Execute o seguinte comando para usar o virtualenv 'salic-ml'

    $ workon salic-ml

Quando quiser sair do virtualenv 'salic-ml' execute o seguinte comando

    $ deactivate

Instale as dependencias do projeto, certifique-se de estar no virtualenv
'salic-ml'

    $ pip3 install -e .


Baixar os dados
---------------

Para versionar os dados utilizados em nossas pesquisas, estamos utilizando o
[Git Large Files Storage](https://git-lfs.github.com/).

Para baixar os dados que utilizamos, instale o pacote `git-lfs` e então execute
o comando

    $ git-lfs pull

A partir do diretório raiz do repositório.


Executar um Notebook
--------------------

Execute o jupyter-notebook:

    $ jupyter-notebook

No jupter-notebook que foi aberto no navegador entre no diretório 'notebooks'
e abra o notebook desejado


Estrutura da pasta Notebook
---------------------------

A pasta notebook foi dividido em 3 subpastas:

* **Doing:** notebooks que estão sendo desenvolvidos.

* **Exploratory:** notebooks usados para exploração. Pode conter "rascunhos",
notebooks não finalizados ou finalizados mas com pouca relevância.
Seguem o formato <Descrição do Notebook>-<Versão>.

* **Report:** Notebooks com os resultados das pesquisas. Esta pasta contém as
versões de notebooks estáveis e atualizados das pesquisas realizadas.


Objetivos
---------

Automatizar o processo de admissão de propostas do Salic.

* **Verificação da planilha orçamentária:** para cada item da planilha
orçamentária, verificar se o valor solicitado para o mesmo é compatível com a
com a estrutura do projeto e com o histórico de aprovação daquele item.
Exemplo: solicitação de R$ 3,5 milhões de reais para pagamento de INSS.
* **Categorização de projetos:** verificar se o conjunto de produtos e serviços
solicitados fazem juz a categoria do projeto.

Arquitetura
-----------

A cada nova proposta cadastrada, o Salic envia os dados da proposta ao Salic-ML
via API, então o sistema realiza o processamento necessário e envia os
resultados de volta para o Salic. Ainda existe a possibilidade de um
administrador externo sincronizar os dados entre o Salic-ML e o Salic e
retreinar o algoritmo utilizado.

![Arquitetura Salic-ML](arquitetura.jpg)

Solução
-------

O corrente desenvolvimento tem como foco a criação de uma solução para
automatizar a verificação da planilha orçamentária, ou seja, verificar se cada
item da planilha contém um valor solicitado aceitável ou se deve ser reduzido.

**Ferramentas:** descrição das ferramentas utilizadas para viabilizar o
Salic-ML.

* DBeaver: acesso de leitura do banco de dados do Salic via VPN;
* Python e módulos científicos: numpy, scipy, matplotlib, pandas, sklearn;
* Jupyter notebook: interface de programação interativa para acelerar a
pesquisa;
* Django: criação da API.

**Abordagem:** o corrente problema é multivariável, desta forma, foram
levantadas todas as variáveis que podem influenciar aumento ou diminuição do
valor aceitável.

Todos os dados referentes às planilhas orçamentárias foram baixados do Salic
para manipulação e pesquisa local.

A primeira variável investigada foi o valor solicitado de cada item.
Comparou-se o valor aprovado e recusado para cada item de cada projeto. O
gráfico abaixo é um exemplo da análise realizada.

![Itens aprovados e recusados no tempo](itens.jpg)

**Resultados:** apenas a comparação entre o valor solicitado e o valor
aprovado não são suficientes para garantir quando um valor solicitado deve ser
aceito.

Próximos passos
---------------

* Investigar por análise de hipóteses quais outras variáveis podem ou não estar
relacionadas com a aprovação do item com o valor solicitado;
* Realizar análises de desempenho para cada método de verificação dos valores
dos itens da planilha orçamentária;
* Implementação de métodos estatísticos utilizando ou não aprendizado de
máquina para verificação dos valores dos itens da planilha orçamentária.

Novas demandas
--------------

Expandir o escopo do Salic-ML para englobar não só a análise de propostas
submetidas ao Salic, como também a análise de resultados de projetos já
executados e a investigação de insights para servirem de insumo ao Ver-Salic.
