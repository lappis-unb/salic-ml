# Testes 

Os testes no SALIC-ML foram feitos utilizando o [pytest](https://docs.pytest.org/en/latest/contents.html).
A documentação aqui presente mostra como são executados os testes e como funciona a arquitetura dos mesmos.

## Arquitetura

Para a configuração correta do pytest e a execução dos testes foram necessários os seguintes arquivos e diretórios:

* tox.ini
* tests/
    * conftest.py
    * utils.py
    * test_x.py
    * ...

### tox.ini

No tox.ini, foram inseridas algumas configurações básicas para o pytest funcionar da maneira como desejamos.

Ele funciona como um ferramenta de automatização de testes que trabalha em conjunto com o pytest.

Nele, foi possível definir as seguintes configurações(no momento da escrita do documento):

```python
[pytest]
DJANGO_SETTINGS_MODULE=salicml_api.config.settings
django_find_project=true
python_paths = src/
testpaths= src/
```

É possível observar outras formas de se usar o tox juntamento com o pytest em: https://tox.readthedocs.io/en/latest/example/pytest.html

### tests/

Para que seja possível que o pytest encontre os testes, é necessário que todos eles estejam em um diretório com o nome tests. No nosso caso, o diretório se encontra dentro de src/salicml_api/analysis/tests/ .

### conftest.py

Este arquivo é onde se encontram as fixtures definidas no projeto, sendo possível definir várias delas no mesmo, o que faz com que o pytest automaticamente reconheça a existência das mesmas e utilize-as quando necessário.

### utils.py

Arquivo com funções compartilhadas pelos arquivos de teste.

### test_x.py

Arquivo de exemplo, representando todos os arquivos de teste que podem ser criados.

É importante lembrar que todos os arquivos de teste, e suas funções, devem ter seus nomes iniciados com "test_".

Exemplo de arquivo de teste e método:

![](figures/test.png?raw=true "Test Output")


## Primeiros Passos

Com a aplicação já rodando (subir_aplicação.md), os passos pra rodar os testes são os seguintes:

 1. Entrar no bash dentro do container  
     ```shell
    $ sudo docker-compose -f docker/docker-compose.yml exec django bash
    ```
 2. Agora dentro do container, é possivel ter acesso aos comandos inv (https://github.com/lappis-unb/salic-ml#tasks-comuns), com isso o comando para rodar os testes é os seguinte :
    ```shell
     $ inv test
     ```

    Esse comando irá percorrer toda a raiz do projeto procurando por diretórios com o nome *tests*, nele o pytest procurará por arquivos que contenham "test_" no nome e nesses arquivos, serão executadas as funções que contenham "test_" no nome.

    Exemplo de output dos testes:

    
    ![](figures/output.png?raw=true "Test Output")





