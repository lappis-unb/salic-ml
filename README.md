Salic - Machine Learning
========================

Time atual:
* Prof. Felipe Duerno
* Luciano Prestes
* Marlon Mendes
* Alexandre Torres

Objetivos
---------

Automatizar o processo de admissão de propostas do Salic.

* **Verificação da planilha orçamentária:** para cada item da planilha orçamentária, verificar se o valor solicitado para o mesmo é compatível com a com a estrutura do projeto e com o histórico de aprovação daquele item. Exemplo: solicitação de R$ 3,5 milhões de reais para pagamento de INSS.
* **Categorização de projetos:** verificar se o conjunto de produtos e serviços solicitados fazem juz a categoria do projeto.

Arquitetura
-----------

A cada nova proposta cadastrada, o Salic envia os dados da proposta ao Salic-ML via API, então o sistema realiza o processamento necessário e envia os resultados de volta para o Salic. Ainda existe a possibilidade de um administrador externo sincronizar os dados entre o Salic-ML e o Salic e retreinar o algoritmo utilizado.

![Arquitetura Salic-ML](arquitetura.jpg)

Solução
-------

O corrente desenvolvimento tem como foco a criação de uma solução para automatizar a verificação da planilha orçamentária, ou seja, verificar se cada item da planilha contém um valor solicitado aceitável ou se deve ser reduzido.

**Ferramentas:** descrição das ferramentas utilizadas para viabilizar o Salic-ML.

* DBeaver: acesso de leitura do banco de dados do Salic via VPN;
* Python e módulos científicos: numpy, scipy, matplotlib, pandas, sklearn;
* Jupyter notebook: interface de programação interativa para acelerar a pesquisa;
* Django: criação da API.

**Abordagem:** o corrente problema é multivariável, desta forma, foram levantadas todas as variáveis que podem influenciar aumento ou diminuição do valor aceitável.

Todos os dados referentes às planilhas orçamentárias foram baixados do Salic para manipulação e pesquisa local.

A primeira variável investigada foi o valor solicitado de cada item. Comparou-se o valor aprovado e recusado para cada item de cada projeto. O gráfico abaixo é um exemplo da análise realizada.

![Itens aprovados e recusados no tempo](itens.jpg)

**Resultados:** apenas a comparação entre o valor solicitado e o valor aprovado não são suficientes para garantir quando um valor solicitado deve ser aceito.

Próximos passos
---------------

* Investigar por análise de hipóteses quais outras variáveis podem ou não estar relacionadas com a aprovação do item com o valor solicitado;
* Realizar análises de desempenho para cada método de verificação dos valores dos itens da planilha orçamentária;
* Implementação de métodos estatísticos utilizando ou não aprendizado de máquina para verificação dos valores dos itens da planilha orçamentária.

Novas demandas
--------------

Expandir o escopo do Salic-ML para englobar não só a análise de propostas submetidas ao Salic, como também a análise de resultados de projetos já executados e a investigação de insights para servirem de insumo ao Ver-Salic.
