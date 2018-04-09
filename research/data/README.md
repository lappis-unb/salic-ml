## Fonte de dados

### Obtendo datasets

Todos os datasets (em `.csv`) usados neste projeto são obtidos a partir do banco de dados do Salic. Este documento explica brevemente o processo de obtenção dos datasets.

1. Conecte-se com o banco de dados do Salic via VPN: [Guia de acesso ao banco de dados via VPN](https://github.com/lappis-unb/EcossistemasSWLivre/wiki/Acessando-banco-de-dados-via-VPN)

2. Identifique os bancos de dados, tabelas e colunas relevantes ao seu objetivo.

3. Execute comandos/scripts SQL para exibir os dados de interesse:

    `SELECT * FROM Sac_db.tbPlanilha;`

4. No DBeaver os resultados dos comandos executados são exibidos na aba/view "Results"

5. Clicando com o botão direito em qualquer linha do resultado da aba "Results", selecione a opção "Export resultset"

6. Escolha a opção CSV

7. Configure a saída de acordo com seu interesse, em geral as opções padrão são suficiente.

8. O CSV será baixado será salvo no local escolhido.
