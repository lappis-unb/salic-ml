## Sistema de cache
O salicml utiliza um sistema de `cache` para facilitar a utilização dos dataframes necessários para os cálculos de métricas.
A implementação deste sistema está localizada no diretório `salic-ml/src/salicml/data` nos arquivos `loader.py` e `query.py`.
O sistema de cache carrega em memória os dataframes localizados no diretório `salicml/data` a medida em que são chamados no código, esta chamada é feita via o objeto **data**. Todos os dataframes localizados na pasta `salicml/data` podem ser carregados e utilizados da seguinte maneira:
```py
1 from salicml.data import data
2 data.nome_do_dataframe
3
4 #para utilizar o dataframe planilha_projetos por exemplo
5 data.planilha_projetos
``` 
O dataframe é carregado como um objeto dataframe pandas e portanto possui todos os métodos. Após ser carregado em memória, o dataframe é armazenado em um `cache` e se em algum outro lugar for chamado `data.nome_do_dataframe` o objeto em cache será utilizado, não necessitando um novo carregamento. 
Além dos dataframes salvos como `.pickle.gz`, o cache permite o registro de `sub dataframes` salvando em memória. Ex:
```py
1 from salicml.data import data
2 @data.lazy('planilha_comprovacao')
3 def verified_repeated_receipts(df):
4	receipts = df[COLUMNS]
5	duplicated = receipts[receipts.duplicated(
6		subset=['idComprovantePagamento'], keep=False)]
7	return duplicated
```

Portanto o processo de descobrimento dos dataframes ocorre da seguinte forma:

	1 - procura o dataframe na pasta `salic-ml/data/raw`
	2 - procura o dataframe na pasta `salic-ml/data/dev`
	3 - procura o dataframe na pasta `salic-ml/data/test`
	4 - procura o dataframe no `registry cache`

