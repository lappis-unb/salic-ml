SELECT
projetos.AnoProjeto + projetos.Sequencial AS PRONAC,
a.idPlanilhaAprovacao,
c.idComprovantePagamento,
a.IdPRONAC,
projetos.Segmento AS idSegmento,
a.idProduto AS cdProduto,
a.idEtapa AS cdEtapa,
a.idUFDespesa AS cdUF,
a.idMunicipioDespesa AS cdCidade,
a.idPlanilhaItem,
itens.Descricao AS Item,
projetos.DtProtocolo AS DataProjeto,
c.nrComprovante,
c.nrSerie,
e.CNPJCPF AS nrCNPJCPF,
f.Descricao AS nmFornecedor,
projetos.CgcCpf AS proponenteCgcCpf,
   CASE c.tpDocumento
	 WHEN 1 THEN ('Cupom Fiscal')
	 WHEN 2 THEN ('Guia de Recolhimento')
	 WHEN 3 THEN ('Nota Fiscal/Fatura')
	 WHEN 4 THEN ('Recibo de Pagamento')
	 WHEN 5 THEN ('RPA') ELSE ''
   END AS tpDocumento,
   c.dtPagamento,
   dtEmissao,
   CASE
	 WHEN c.tpFormaDePagamento = '1' THEN 'Cheque'
	 WHEN c.tpFormaDePagamento = '2' THEN 'Transferencia Bancaria'
	 WHEN c.tpFormaDePagamento = '3' THEN 'Saque/Dinheiro' ELSE ''
   END AS tpFormaDePagamento,
   c.nrDocumentoDePagamento,c.idArquivo,c.dsJustificativa AS dsJustificativaProponente,
   b.dsJustificativa AS dsOcorrenciaDoTecnico,b.stItemAvaliado,
   CASE
	 WHEN stItemAvaliado = 1 THEN 'Validado'
	 WHEN stItemAvaliado = 3 THEN 'Impugnado'
	 WHEN stItemAvaliado = 4 THEN 'Aguardando analise'
   END AS stAvaliacao,
   c.vlComprovacao
  FROM       SAC.dbo.tbplanilhaaprovacao                                  a 
  INNER JOIN BDCORPORATIVO.scSAC.tbComprovantePagamentoxPlanilhaAprovacao b ON (a.idPlanilhaAprovacao    = b.idPlanilhaAprovacao)
  INNER JOIN BDCORPORATIVO.scSAC.tbComprovantePagamento                   c ON (b.idComprovantePagamento = c.idComprovantePagamento)
  INNER JOIN Agentes.dbo.Agentes                                          e ON (c.idFornecedor           = e.idAgente)
  INNER JOIN Agentes.dbo.Nomes                                            f ON (c.idFornecedor           = f.idAgente)
  INNER JOIN SAC.dbo.Projetos                                      projetos ON (a.IdPRONAC               = projetos.IdPRONAC)
  INNER JOIN SAC.dbo.tbPlanilhaItens 								  itens ON (a.idPlanilhaItem 		 = itens.idPlanilhaItens)
  WHERE    a.nrFonteRecurso = 109 
	  AND (sac.dbo.fnVlComprovado_Fonte_Produto_Etapa_Local_Item
	  (a.idPronac,a.nrFonteRecurso,a.idProduto,a.idEtapa,a.idUFDespesa,a.idMunicipioDespesa, a.idPlanilhaItem)) > 0 
