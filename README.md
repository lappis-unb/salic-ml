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

O salic-ml desenvolve uma API para fornecer dados relevantes a respeito de projetos culturais a partir de seus dados abertos. O projeto conta com dois repositórios disponíveis na plataforma [GitHub](https://github.com/lappis-unb/) e um [servidor FTP](ftp://138.68.73.247/). Este é o repositório principal, onde são mantidas as pesquisas, tarefas e planejamento do time. O repositório [salic-ml-web](https://github.com/lappis-unb/salic-ml-web) é o repositório utilizado para desenvolver a API para a disponibilização dos dados encontrados através das pesquisas. Por fim, o servidor FTP fornece os dados brutos do Salic, utilizados para realizar todas as pesquisas do grupo.


Contribuição
------------

Antes de mais nada, sinta-se à vontade para nos contactar sempre que precisar. Nosso grupo de comunicação no [RocketChat](https://chat.lappis.rocks/channel/salic-ml) está sempre aberto para discussões. Para acompanhar nosso _roadmap_, instale o plugin [ZenHub](https://www.zenhub.com/) para o GitHub.

#### Requisitos

- Python 3.6
- Virtualenv ou virtualenvwrapper

#### Instalação

As pesquisas deste repositório são realizadas em notebooks do [Jupyter Notebook](http://jupyter.org/). Para reproduzir nossas pesquisas e estudos, é preciso baixar os dados do servidor FTP e instalar o Jupyter Notebook.

Para baixar os dados do servidor FTP, basta acessar o seu endpoint: _ftp://138.68.73.247/_. Lembrando que a estrutura de arquivos do servidor FTP é a mesma da pasta `data` deste repositório, então tenha cuidado para não armazenar os dados baixados em pastas erradas. Uma forma de baixar os dados é com o comando [wget](https://www.gnu.org/software/wget/), por um terminal de comandos, entre na pasta raiz deste repositório e execute o seguinte comando:

    $ wget -r -nH -nc -P data ftp://138.68.73.247

Este comando baixará todos os arquivos de dados do servidor e pode demorar alguns minutos ou mesmo horas. Cada notebook precisa de um conjunto específico de arquivos de dados e raramente ou único notebook utilizará todos os arquivos do servidor e para baixar arquivos específicos do servidor, execute o comando:

    $ wget -nc -P data/FILE ftp://138.68.73.247/FILE

Onde _FILE_ deve ser substituído pelo caminho e nome do arquivo desejado.

Para instalar o Jupyter Notebook, é possível utilizar a plataforma [Anaconda](https://www.anaconda.com/) ou o [pip](http://jupyter.org/install).
Para instalar todas as dependências deste projeto, esteja em um ambiente virtual do python e rode o seguinte comando:

    $ pip install -r requirements.txt

#### Reprodução de pesquisas

Após a instalação, execute o seguinte comando a partir da raiz do diretório:

    $ jupyter-notebook

Este comando abrirá uma página o navegador. A partir deste navegador, entre no diretório _notebooks_ e abra o notebook desejado. Estrutura de pastas para armazenar os notebooks de estudo e pesquisa:

* **Doing:** notebooks que estão sendo desenvolvidos.

* **Exploratory:** notebooks usados para exploração. Pode conter "rascunhos",
notebooks não finalizados ou finalizados mas com pouca relevância.
Seguem o formato <Descrição do Notebook>-<Versão>.

* **Report:** Notebooks com os resultados das pesquisas. Esta pasta contém as
versões de notebooks estáveis e atualizados das pesquisas realizadas.


#### API

Para rodar a api, execute o comando a partir da raiz do diretório:

    $ inv run

#### Passo a passo de contribuições

1. Crie um _Fork_ deste repositório: na página do repositório [salic-ml no GitHub](https://github.com/lappis-unb/salic-ml) tem um botão para realizar o _fork_;

2. Clone o seu _fork_ do repositório:

```
$ git clone http://github.com/<USERNAME>/salic-ml.git
```

3. Crie uma _branch_ de pesquisa:

```
$ git checkout -b <USERNAME>-new-research
```

4. Faça suas mudanças e realize os seus _commits_:

```
$ git commit -am 'My contribution'
```

5. Atualize suas modificações no seu _fork_ remoto:

```
$ git push origin <USERNAME>-new-research
```

6. Crie o seu _pull request_: na plataforma GitHub, a partir do seu _fork_, terá um botão para abrir um _pull request_.

#### Outros comandos

Alguns comandos foram criados para facilitar o desenvolvimento, para rodar a API, popular dados entre outros.
- Para que tenha acesso a lista de comandos digite em seu terminal:

     $ invoke --list

 - Para ler a descrição de um comando específico (exemplo comando run):

     $ invoke --help run

 - Para executá-lo (exemplo comando run):

     $ inv run

Licença
-------

O salic-ml é desenvolvido sob a [Licença GPLv3](LICENSE.md).
