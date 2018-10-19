SELECT p.IdPRONAC,
	   (p.AnoProjeto + p.Sequencial) AS PRONAC,
	   p.DtProtocolo AS DataProjeto,
	   a.idplanilhaaprovacao AS idPlanilhaAprovacao,
	   a.idPlanilhaItem,
	   itens.Descricao AS Item,
	   p.Segmento AS idSegmento,
	   comprovacao.vlComprovado AS vlComprovacao,
	   comprovacao.idComprovantePagamento,
	   e.CNPJCPF AS nrCNPJCPF,
	   f.Descricao AS nmFornecedor,
	   uf.CodUfIbge as UF,
	   a.idProduto AS cdProduto,
	   a.idMunicipioDespesa AS cdCidade,
	   a.idEtapa AS cdEtapa
FROM SAC.dbo.tbPlanilhaAprovacao a
INNER JOIN SAC.dbo.Projetos p ON (a.IdPRONAC = p.IdPRONAC)
INNER JOIN BDCorporativo.scSAC.tbComprovantePagamentoxPlanilhaAprovacao comprovacao ON (a.idPlanilhaAprovacao = comprovacao.idPlanilhaAprovacao)
INNER JOIN BDCorporativo.scSAC.tbComprovantePagamento tb_comprovacao ON (comprovacao.idComprovantePagamento = tb_comprovacao.idComprovantePagamento)
INNER JOIN Agentes.dbo.Agentes e ON (tb_comprovacao.idFornecedor = e.idAgente)
INNER JOIN Agentes.dbo.Nomes f ON (tb_comprovacao.idFornecedor = f.idAgente)
INNER JOIN SAC.dbo.tbPlanilhaItens itens ON (a.idPlanilhaItem = itens.idPlanilhaItens)
INNER JOIN SAC.dbo.Uf uf ON (a.idUFDespesa = uf.CodUfIbge)
WHERE (p.AnoProjeto + p.Sequencial)='164274';
