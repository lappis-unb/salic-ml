<!-- a, c, i, k, segmento, -->

SELECT a.idPronac,
a.AnoProjeto+a.Sequencial as PRONAC,
k.idPlanilhaAprovacao,
i.Descricao as Item,
i.idPlanilhaItens,
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
a.DtProtocolo as DataProjeto
FROM SAC.dbo.Projetos a
INNER JOIN SAC.dbo.tbPlanilhaProjeto b on (a.idPronac = b.idPronac)
INNER JOIN SAC.dbo.tbPlanilhaAprovacao k on (b.idPlanilhaProposta=k.idPlanilhaProposta)
LEFT JOIN SAC.dbo.Produto c on (b.idProduto = c.Codigo)
INNER JOIN SAC.dbo.tbPlanilhaItens i on (b.idPlanilhaItem=i.idPlanilhaItens)
INNER JOIN SAC.dbo.Area area ON (a.Area = area.Codigo)
INNER JOIN SAC.dbo.Segmento segmento ON (a.segmento = segmento.Codigo)
WHERE k.stAtivo = 'S';
