# Diferença entre arquivos Docker-Compose

Atualmente no projeto, existem quatro diferentes docker-compose. Aqui será documentada a função de cada um.

## docker-compose.yml

É o docker-compose padrão da aplicação. Utilizado para rodar localmente o projeto, tem três serviços: O banco local **postgres**, a conexão com a VPN **salic-db**, e a aplicação em si **django**.

## docker-compose.continuous-deploy.yml

Compose utilizado para o deploy contínuo da aplicação. Nele são utilizados os serviços adicionais do **certbot**, configurando o certificado da api, e o **watchtower**, necessário para o deploy continuo.

## docker-compose.offline.yml

Compose utilizado quando não é necessária a conexão com o banco de homologação por VPN. Contém somente os serviços **postgres** e **django**

## Comparação

| Compose/Serviços                     | postgres | django | salic_db | certbot | watchtower |
|--------------------------------------|----------|--------|----------|---------|------------|
| docker-compose.yml                   |     x    |    x   |     x    |         |            |
| docker-compose.continuous-deploy.yml |     x    |    x   |     x    |    x    |      x     |
| docker-compose.offline.yml           |     x    |    x   |          |         |            |