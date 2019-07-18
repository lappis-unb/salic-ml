--- Project example: http://salic.cultura.gov.br/verprojetos?idPronac=501eac548e7d4fa987034573abc6e179MjEwMzEwZUA3NWVmUiEzNDUwb3RT
SELECT LTRIM(RTRIM(a.idPronac)) as idPronac, LTRIM(RTRIM(a.PRONAC)) as PRONAC, Item, LTRIM(RTRIM(i.idPlanilhaItens)) as idPlanilhaItens, Unidade, QtDias, QtItem, nrOcorrencia,
	(VlSolicitado / NULLIF(QtItem * nrOcorrencia, 0)) AS VlUnitarioSolicitado,
	VlSolicitado AS VlTotalSolicitado,
	VlUnitario AS VlUnitarioAprovado,
	Aprovado AS VlTotalAprovado,
	UF AS UfItem,
	Municipio AS MunicipioItem,
	LTRIM(RTRIM(Etapa)) as Etapa,
	LTRIM(RTRIM(p.Area)) as Area,
	LTRIM(RTRIM(p.Segmento)) as Segmento,
	p.DtProtocolo as DataProjeto
FROM SAC.dbo.vwPlanilhaAprovada a
LEFT JOIN SAC.dbo.Projetos p
	ON a.idPronac = p.IdPRONAC
INNER JOIN SAC.dbo.tbPlanilhaItens i
	ON Item = i.Descricao;
