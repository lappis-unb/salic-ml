SELECT a.idPronac,a.AnoProjeto+a.Sequencial as PRONAC,a.NomeProjeto,k.idProduto,k.idPlanilhaAprovacao, k.idPlanilhaAprovacaoPai,
       case 
         when k.idProduto = 0
           then 'Administração do Projeto'
           else c.Descricao 
         end as Produto,
       convert(varchar(8),d.idPlanilhaEtapa) + ' - ' + d.Descricao as Etapa,i.Descricao as Item,
       (z.Quantidade * z.Ocorrencia * z.ValorUnitario) as VlSolicitado,z.dsJustificativa as JustProponente,
       (b.Quantidade * b.Ocorrencia * b.ValorUnitario) as VlSugerido,b.Justificativa as JustParecerista,
       e.Descricao as Unidade,k.QtItem,k.nrOcorrencia,k.VlUnitario,k.QtDias,
       k.TpDespesa,k.TpPessoa,k.nrContrapartida,k.nrFonteRecurso as idFonte,x.Descricao as FonteRecurso,f.UF,
       f.Municipio,
       ROUND((k.QtItem * k.nrOcorrencia * k.VlUnitario),2) as Aprovado,
       k.dsJustificativa as JustComponente
       FROM SAC.dbo.Projetos a
       INNER JOIN SAC.dbo.tbPlanilhaProjeto b on (a.idPronac = b.idPronac)
       INNER JOIN SAC.dbo.tbPlanilhaProposta z on (b.idPlanilhaProposta=z.idPlanilhaProposta)
       INNER JOIN SAC.dbo.tbPlanilhaAprovacao k on (b.idPlanilhaProposta=k.idPlanilhaProposta)
       LEFT JOIN SAC.dbo.Produto c on (b.idProduto = c.Codigo)
       INNER JOIN SAC.dbo.tbPlanilhaEtapa d on (k.idEtapa = d.idPlanilhaEtapa)
       INNER JOIN SAC.dbo.tbPlanilhaUnidade e on (b.idUnidade = e.idUnidade)
       INNER JOIN SAC.dbo.tbPlanilhaItens i on (b.idPlanilhaItem=i.idPlanilhaItens)
       INNER JOIN SAC.dbo.Verificacao x on (b.FonteRecurso = x.idVerificacao)
       INNER JOIN agentes.dbo.vUfMunicipio f on (b.UfDespesa = f.idUF and b.MunicipioDespesa = f.idMunicipio);

