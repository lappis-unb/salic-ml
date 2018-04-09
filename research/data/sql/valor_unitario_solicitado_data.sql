-- Colunas: Item, Valor Unitário Solicitado, Data de solicitação, idPRONAC do projeto

SELECT i.Descricao AS 'Item',
   	b.ValorUnitario AS 'ValorUnitarioSolicitado',
   	a.DtInicioExecucao AS 'Data',
   	a.IdPRONAC
FROM SAC.dbo.Projetos AS a
INNER JOIN SAC.dbo.tbPlanilhaProposta AS b ON a.idProjeto = b.idProjeto
INNER JOIN SAC.dbo.tbPlanilhaEtapa AS d ON b.idEtapa = d.idPlanilhaEtapa
INNER JOIN SAC.dbo.tbPlanilhaItens AS i ON b.idPlanilhaItem = i.idPlanilhaItens;
