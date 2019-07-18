SELECT projetos.IdPRONAC,
	   LTRIM(RTRIM((projetos.AnoProjeto + projetos.Sequencial))) AS PRONAC,
	   projetos.DtProtocolo AS DataProjeto,
	   LTRIM(RTRIM(a.idplanilhaaprovacao)) AS idPlanilhaAprovacao,
	   LTRIM(RTRIM(a.idPlanilhaItem)) AS idPlanilhaItem,
	   LTRIM(RTRIM(itens.Descricao)) AS Item,
	   LTRIM(RTRIM(projetos.Segmento)) AS idSegmento,
	   comprovacao.vlComprovado AS vlComprovacao,
	   ROUND((a.QtItem * a.nrOcorrencia * a.VlUnitario),2) as vlAprovado,
	   LTRIM(RTRIM(comprovacao.idComprovantePagamento)),
	   LTRIM(RTRIM(e.CNPJCPF)) AS nrCNPJCPF,
	   f.Descricao AS nmFornecedor,
	   uf.CodUfIbge as UF,
	   LTRIM(RTRIM(a.idProduto)) AS cdProduto,
	   a.idMunicipioDespesa AS cdCidade,
	   a.idEtapa AS cdEtapa,
	   LTRIM(RTRIM(projetos.CgcCpf)) AS proponenteCgcCpf
FROM SAC.dbo.tbPlanilhaAprovacao a
INNER JOIN SAC.dbo.Projetos projetos ON (a.IdPRONAC = projetos.IdPRONAC)
INNER JOIN BDCorporativo.scSAC.tbComprovantePagamentoxPlanilhaAprovacao comprovacao ON (a.idPlanilhaAprovacao = comprovacao.idPlanilhaAprovacao)
INNER JOIN BDCorporativo.scSAC.tbComprovantePagamento tb_comprovacao ON (comprovacao.idComprovantePagamento = tb_comprovacao.idComprovantePagamento)
INNER JOIN Agentes.dbo.Agentes e ON (tb_comprovacao.idFornecedor = e.idAgente)
INNER JOIN Agentes.dbo.Nomes f ON (tb_comprovacao.idFornecedor = f.idAgente)
INNER JOIN SAC.dbo.tbPlanilhaItens itens ON (a.idPlanilhaItem = itens.idPlanilhaItens)
INNER JOIN SAC.dbo.Uf uf ON (a.idUFDespesa = uf.CodUfIbge)
WHERE a.stAtivo = 'S';
