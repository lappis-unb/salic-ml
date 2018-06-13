# Planilha Aprovação

**Dataset:**

**SQL query**: [dataset link]()

```SQL
SELECT aprovado.idPronac, Produto, Etapa, Item, VlSolicitado, JustProponente, VlSugerido,
	   JustParecerista, Unidade, QtItem, nrOcorrencia, VlUnitario, QtDias, FonteRecurso,
	   UF, Municipio, Aprovado, JustComponente, UfProjeto, Area, Segmento, Mecanismo, projetos.NomeProjeto,
	   CgcCpf, Situacao, projetos.DtProtocolo, OrgaoOrigem, Orgao, DtInicioExecucao, DtFimExecucao, SolicitadoReal
FROM SAC.dbo.vwPlanilhaAprovada as aprovado
LEFT JOIN SAC.dbo.Projetos as projetos
ON aprovado.idPronac = projetos.IdPRONAC;
```
