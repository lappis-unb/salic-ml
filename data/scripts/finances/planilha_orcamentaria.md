```SQL
-- Project example: http://salic.cultura.gov.br/verprojetos?idPronac=501eac548e7d4fa987034573abc6e179MjEwMzEwZUA3NWVmUiEzNDUwb3RT
-- ID_PRONAC: '210310', PRONAC = '172085'

SELECT a.idPronac, a.PRONAC, a.idPlanilhaAprovacao, Item, i.idPlanilhaItens, Unidade, QtDias, QtItem, nrOcorrencia,
	(VlSolicitado / NULLIF(QtItem * nrOcorrencia, 0)) AS VlUnitarioSolicitado,
	VlSolicitado AS VlTotalSolicitado,
	VlUnitario AS VlUnitarioAprovado,
	Aprovado AS VlTotalAprovado,
	UF AS UfItem,
	Municipio AS MunicipioItem,
	Etapa,
	p.Area as idArea,
	area.Descricao as Area,
	p.Segmento AS idSegmento,
	s.Descricao AS Segmento,
	idProduto,
	Produto,
	p.DtProtocolo as DataProjeto
FROM SAC.dbo.vwPlanilhaAprovada a
LEFT JOIN SAC.dbo.Projetos p
	ON a.idPronac = p.IdPRONAC
INNER JOIN SAC.dbo.tbPlanilhaItens i
	ON Item = i.Descricao
INNER JOIN SAC.dbo.Segmento s
	ON P.Segmento = s.Codigo
INNER JOIN SAC.dbo.Area area
	ON p.Area = area.Codigo;
```
