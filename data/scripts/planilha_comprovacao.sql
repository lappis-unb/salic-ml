SELECT projetos.IdPRONAC,
	   LTRIM(RTRIM((projetos.AnoProjeto + projetos.Sequencial))) AS PRONAC,
	   projetos.DtProtocolo AS DataProjeto,
	   a.idplanilhaaprovacao AS idPlanilhaAprovacao,
	   LTRIM(RTRIM(a.idPlanilhaItem)) as idPlanilhaItem,
	   itens.Descricao AS Item,
	   LTRIM(RTRIM(projetos.Segmento)) AS idSegmento,
	   comprovacao.vlComprovado AS vlComprovacao,
	   comprovacao.idComprovantePagamento,
	   LTRIM(RTRIM(e.CNPJCPF)) AS nrCNPJCPF,
	   f.Descricao AS nmFornecedor,
	   uf.CodUfIbge as UF,
	   LTRIM(RTRIM(a.idProduto)) AS cdProduto,
	   a.idMunicipioDespesa AS cdCidade,
	   LTRIM(RTRIM(a.idEtapa)) AS cdEtapa,
	   LTRIM(RTRIM(projetos.CgcCpf)) AS proponenteCgcCpf,
	   LTRIM(RTRIM(tb_comprovacao.tpFormaDePagamento)) as tpFormaDePagamento
FROM SAC.dbo.tbPlanilhaAprovacao a
INNER JOIN SAC.dbo.Projetos projetos ON (a.IdPRONAC = projetos.IdPRONAC)
INNER JOIN BDCorporativo.scSAC.tbComprovantePagamentoxPlanilhaAprovacao comprovacao ON (a.idPlanilhaAprovacao = comprovacao.idPlanilhaAprovacao)
INNER JOIN BDCorporativo.scSAC.tbComprovantePagamento tb_comprovacao ON (comprovacao.idComprovantePagamento = tb_comprovacao.idComprovantePagamento)
INNER JOIN Agentes.dbo.Agentes e ON (tb_comprovacao.idFornecedor = e.idAgente)
INNER JOIN Agentes.dbo.Nomes f ON (tb_comprovacao.idFornecedor = f.idAgente)
INNER JOIN SAC.dbo.tbPlanilhaItens itens ON (a.idPlanilhaItem = itens.idPlanilhaItens)
INNER JOIN SAC.dbo.Uf uf ON (a.idUFDespesa = uf.CodUfIbge)
WHERE  a.nrFonteRecurso = 109
       AND (sac.dbo.fnVlComprovado_Fonte_Produto_Etapa_Local_Item
                  (a.idPronac,a.nrFonteRecurso,a.idProduto,a.idEtapa,a.idUFDespesa,a.idMunicipioDespesa, a.idPlanilhaItem)) > 0
