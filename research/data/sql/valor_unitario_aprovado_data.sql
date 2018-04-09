-- Colunas: Item, Valor Unitário Aprovado, Data de solicitação, idPRONAC do projeto

SELECT itens.Descricao AS 'Item',
   	p.ValorUnitario AS 'ValorUnitarioAprovado',
   	projeto.DtInicioExecucao AS 'Data',
   	p.idPRONAC
FROM SAC.dbo.tbPlanilhaProjeto AS p
INNER JOIN SAC.dbo.Projetos AS projeto ON p.idPRONAC = projeto.IdPRONAC
INNER JOIN SAC.dbo.tbPlanilhaItens AS itens ON itens.idPlanilhaItens = p.idPlanilhaItem;
