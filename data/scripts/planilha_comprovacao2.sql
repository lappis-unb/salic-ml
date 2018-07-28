SELECT a.idPlanilhaAprovacao,c.idComprovantePagamento,a.IdPRONAC,
   a.idProduto as cdProduto,a.idEtapa as cdEtapa,a.idUFDespesa AS cdUF,a.idMunicipioDespesa as cdCidade,a.idPlanilhaItem,
   c.nrComprovante,c.nrSerie,e.CNPJCPF as nrCNPJCPF,f.Descricao as nmFornecedor,
   CASE c.tpDocumento
	 WHEN 1 THEN ('Cupom Fiscal')
	 WHEN 2 THEN ('Guia de Recolhimento')
	 WHEN 3 THEN ('Nota Fiscal/Fatura')
	 WHEN 4 THEN ('Recibo de Pagamento')
	 WHEN 5 THEN ('RPA') ELSE ''
   END as tpDocumento,
   c.dtPagamento,
   dtEmissao,
   CASE
	 WHEN c.tpFormaDePagamento = '1' THEN 'Cheque'
	 WHEN c.tpFormaDePagamento = '2' THEN 'Transferencia Bancaria'
	 WHEN c.tpFormaDePagamento = '3' THEN 'Saque/Dinheiro' ELSE ''
   END as tpFormaDePagamento,
   c.nrDocumentoDePagamento,c.idArquivo,c.dsJustificativa as dsJustificativaProponente,
   b.dsJustificativa as dsOcorrenciaDoTecnico,b.stItemAvaliado,
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
  WHERE    a.nrFonteRecurso = 109 
	  AND (sac.dbo.fnVlComprovado_Fonte_Produto_Etapa_Local_Item
	  (a.idPronac,a.nrFonteRecurso,a.idProduto,a.idEtapa,a.idUFDespesa,a.idMunicipioDespesa, a.idPlanilhaItem)) > 0 
;
