SELECT a.idPronac,a.AnoProjeto+a.Sequencial as PRONAC,k.idPlanilhaAprovacao, k.idPlanilhaAprovacaoPai,i.Descricao as Item,
       (z.Quantidade * z.Ocorrencia * z.ValorUnitario) as VlSolicitado,
       (b.Quantidade * b.Ocorrencia * b.ValorUnitario) as VlSugerido,
       e.Descricao as Unidade,k.QtItem,k.nrOcorrencia,k.VlUnitario,k.QtDias,f.UF,
       f.Municipio,
       ROUND((k.QtItem * k.nrOcorrencia * k.VlUnitario),2) as Aprovado,
       k.dtPlanilha,
       k.stAtivo,
       projetos.Area,
       projetos.Segmento,
       projetos.DtProtocolo AS DataProjeto
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
       INNER JOIN SAC.dbo.Projetos projetos on (a.idPronac = projetos.IdPRONAC);
