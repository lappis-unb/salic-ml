# Diferença entre arquivos Docker-Compose

Atualmente no projeto, existem quatro diferentes docker-compose. Aqui será documentada a função de cada um.

## docker-compose.yml

É o docker-compose padrão da aplicação. Utilizado para rodar localmente o projeto, tem três serviços: O banco local **postgres**, a conexão com a VPN **salic-db**, e a aplicação em si **django**.

## docker-compose.continuous-deploy.yml

Compose utilizado para o deploy contínuo da aplicação. Nele são utilizados os serviços adicionais do **certbot**, configurando o certificado SSL da aplicação, e o [**watchtower**](https://github.com/containrrr/watchtower), utilizado para o deploy continuo.

## docker-compose.offline.yml

Compose utilizado quando não há a possibilidade/necessidade de conexão com o banco de homologação via VPN. Contém somente os serviços **postgres** e **django**. Neste caso, não estão definidas as variáveis de conexão com um banco externo. Portanto, os dados utilizados são os contidos nos dataframes de desenvolvimento, commitados na pasta ```data```. A criação deste compose teve como principal motivação a necessidade de se subir um ambiente agnóstico, do ponto de vista de conexão externa, no GitLabCI para a execução dos testes.

## Comparação

| Compose/Serviços                     | postgres | django | salic_db | certbot | watchtower |
|--------------------------------------|----------|--------|----------|---------|------------|
| docker-compose.yml                   |     x    |    x   |     x    |         |            |
| docker-compose.continuous-deploy.yml |     x    |    x   |     x    |    x    |      x     |
| docker-compose.offline.yml           |     x    |    x   |          |         |            |
