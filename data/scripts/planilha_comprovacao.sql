SELECT projetos.IdPRONAC,
	   (projetos.AnoProjeto + projetos.Sequencial) AS PRONAC,
	   projetos.DtProtocolo AS DataProjeto,
	   a.idplanilhaaprovacao AS idPlanilhaAprovacao,
	   a.idPlanilhaItem,
	   itens.Descricao AS Item,
	   projetos.Segmento AS idSegmento,
	   comprovacao.vlComprovado AS vlComprovacao,
	   comprovacao.idComprovantePagamento,
	   e.CNPJCPF AS nrCNPJCPF,
	   f.Descricao AS nmFornecedor,
	   uf.CodUfIbge as UF,
	   a.idProduto AS cdProduto,
	   a.idMunicipioDespesa AS cdCidade,
	   a.idEtapa AS cdEtapa,
	   projetos.CgcCpf AS proponenteCgcCpf,
		  tb_comprovacao.tpFormaDePagamento
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
