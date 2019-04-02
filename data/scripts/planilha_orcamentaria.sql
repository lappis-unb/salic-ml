SELECT a.idPronac,
a.AnoProjeto+a.Sequencial as PRONAC,
k.idPlanilhaAprovacao,
i.Descricao as Item,
i.idPlanilhaItens,
e.Descricao as Unidade,
k.QtDias,
k.QtItem,
k.nrOcorrencia,
z.ValorUnitario as VlUnitarioSolicitado,
(z.Quantidade * z.Ocorrencia * z.ValorUnitario) as VlTotalSolicitado,
k.VlUnitario as VlUnitarioAprovado,
ROUND((k.QtItem * k.nrOcorrencia * k.VlUnitario), 2) as VlTotalAprovado,
f.UF as UfItem,
f.Municipio as MunicipioItem,
convert(varchar(8), d.idPlanilhaEtapa) + ' - ' + d.Descricao as Etapa,
a.Area as idArea,
area.Descricao as Area,
a.Segmento AS idSegmento,
segmento.Descricao AS Segmento,
k.idProduto,
case
    when k.idProduto = 0
       then 'Administracao do Projeto'
       else c.Descricao
end as Produto,
a.DtProtocolo as DataProjeto,
k.idEtapa AS cdEtapa,
k.idMunicipioDespesa AS cdCidade
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
INNER JOIN SAC.dbo.Segmento segmento ON (a.segmento = segmento.Codigo)
WHERE k.stAtivo = 'S'
