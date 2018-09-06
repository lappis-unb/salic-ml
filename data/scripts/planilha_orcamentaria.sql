-- Project example: http://salic.cultura.gov.br/verprojetos?idPronac=501eac548e7d4fa987034573abc6e179MjEwMzEwZUA3NWVmUiEzNDUwb3RT
-- ID_PRONAC: '210310', PRONAC = '172085'
SELECT
	a.idPronac,
	a.AnoProjeto+a.Sequencial as PRONAC,
	k.idPlanilhaAprovacao,
	i.Descricao as Item,
	i.idPlanilhaItens,
	e.Descricao as Unidade,
	k.QtDias,
	k.QtItem,
	k.nrOcorrencia,
	z.ValorUnitario AS VlUnitarioSolicitado,
	(z.Quantidade * z.Ocorrencia * z.ValorUnitario) AS VlTotalSolicitado,
	k.VlUnitario AS VlUnitarioAprovado,
	ROUND((k.QtItem * k.nrOcorrencia * k.VlUnitario),2) as VlTotalAprovado,
	f.UF AS UfItem,
	f.Municipio AS MunicipioItem,
	convert(varchar(8), d.idPlanilhaEtapa) + ' - ' + d.Descricao as Etapa,
	a.Area AS idArea,
	area.Descricao as Area,
	a.Segmento AS idSegmento,
	s.Descricao AS Segmento,
	k.idProduto,
	case 
	 when k.idProduto = 0
	   then 'Administração do Projeto'
	   else c.Descricao 
	end as Produto,
	a.DtProtocolo as DataProjeto,
	f.idMunicipio AS cdCidade,
	k.idEtapa AS cdEtapa
	FROM SAC.dbo.Projetos a
	INNER JOIN SAC.dbo.tbPlanilhaProjeto b on (a.idPronac = b.idPronac)
	INNER JOIN SAC.dbo.tbPlanilhaProposta z on (b.idPlanilhaProposta=z.idPlanilhaProposta)
	INNER JOIN SAC.dbo.tbPlanilhaAprovacao k on (b.idPlanilhaProposta=k.idPlanilhaProposta)
	LEFT JOIN SAC.dbo.Produto c on (b.idProduto = c.Codigo)
	INNER JOIN SAC.dbo.tbPlanilhaEtapa d on (k.idEtapa = d.idPlanilhaEtapa)
	INNER JOIN SAC.dbo.tbPlanilhaUnidade e on (b.idUnidade = e.idUnidade)
	INNER JOIN SAC.dbo.tbPlanilhaItens i on (b.idPlanilhaItem=i.idPlanilhaItens)
	INNER JOIN SAC.dbo.Verificacao x on (b.FonteRecurso = x.idVerificacao)
	INNER JOIN agentes.dbo.vUfMunicipio f on (b.UfDespesa = f.idUF and b.MunicipioDespesa = f.idMunicipio)
	INNER JOIN SAC.dbo.Area area ON (a.Area = area.Codigo)
	INNER JOIN SAC.dbo.Segmento s ON (a.Segmento = s.Codigo)
	WHERE k.stAtivo = 'S';

