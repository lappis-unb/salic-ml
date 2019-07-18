SELECT LTRIM(RTRIM(aprovado.idPronac)) as idPronac, Produto, Etapa, Item, VlSolicitado, JustProponente, VlSugerido,
	   JustParecerista, Unidade, QtItem, nrOcorrencia, VlUnitario, QtDias, FonteRecurso,
	   UF, Municipio, Aprovado, JustComponente, UfProjeto, Area, LTRIM(RTRIM(Segmento)) as Segmento, Mecanismo, projetos.NomeProjeto,
	   LTRIM(RTRIM(CgcCpf)) as CgcCpf, Situacao, projetos.DtProtocolo, OrgaoOrigem, Orgao, DtInicioExecucao, DtFimExecucao, SolicitadoReal
FROM SAC.dbo.vwPlanilhaAprovada as aprovado
LEFT JOIN SAC.dbo.Projetos as projetos
ON aprovado.idPronac = projetos.IdPRONAC;
