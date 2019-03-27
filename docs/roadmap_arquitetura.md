# Roadmap de Arquitetura
-- --
## Tópicos principais
### Curto/Médio prazo
- Realizar ajustes na aplicação web monolítica para iniciar-se a homologação
  - Links para o SALIC
  - Loading na página inicial
  - ...
- Análise dos dados de feedback
  - Automatização do processo de data capturing para ser disponibilizado numa planilha
- Modularizar a aplicação web monolítica em:
  - Backend Django REST
  - Frontend VueJS
- Ajustar fonte de dados para o Machine Learning
  - Transferir os CSVs do pacote Python para a aplicação web
  - Utilizar o banco de homologação do SALIC como fonte de dados.
  - Utilizar o SALIC-API como fonte de dados
  - Definir saídas do módulo de ML
- DevOPS
  - Finalizar ajustes do deploy na VM do MinC
  - Escrever testes
  - Configurar pipelines na infra do LAPPIS (backup plan)

### Longo prazo
- Arquitetura de Microservices
  - Um serviço para cada indicador
  - Cache de dados?
  - Paralelizar processamento interno
  - ...
- Exibição dos dados
  - Plugin?
  - Integração no SALIC?
  - Página externa?
  - ...
-- --
## Issues

### Curto/Médio prazo

1. BugFix
  - __Adicionar, na aplicação web, links para o SALIC.__
  - __Inserir loading na index page.__
2. Modularização da Arquitetura
  - Backend Django REST
    - __Replicar rotas da aplicação monolítica no formato de API__
    - __Modularizar funcionalidades em mais arquivos__
    - __Redefinir padrões de formato dos objetos enviados para o frontend__
    - __Criar testes unitários__
  2. Frontend VueJS
    - A defnir
3. Padronização de dados fornecidos pelo salic-ml-web
  - __Defnir formatos de objetos para o salic-ml-web__
  - __Definir formatos para as métricas já implementadas__
  - __Reorganizar o data handling dentro do backend__
4. Data handling para o ML
  - __Definir dados a serem passados como parâmetro para o módulo salic-ml-dev__
  - __Definir modelos de objetos a serem utilizados pelo salic-ml-dev__
  - __Modificar pasta de armazenamento do CSV para ser consumido pelo backend apenas__
  - __Puxar dados de treinamento do banco de homologação__
  - __Puxar dados de treinamento do SALIC-API__
5. DevOPS
  - __Revisar processo de deploy na VM do MinC__
  - __Corrigir problemas com o Pickle__
  - __Subir instância na infra do LAPPIS__

### Longo prazo

1. Microservices
  - __Remodelar arquitetura aplicando abordagem de microservices__
  - __Pesquisar implementações já existentes no contexto de machine learning__
2. Exibição dos dados
  - A definir
