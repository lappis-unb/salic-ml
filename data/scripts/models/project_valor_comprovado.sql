SELECT
	   CONCAT(projetos.AnoProjeto, projetos.Sequencial) AS PRONAC,
	   SUM(comprovacao.vlComprovado) AS vlComprovacao
FROM SAC.dbo.tbPlanilhaAprovacao a
INNER JOIN SAC.dbo.Projetos projetos ON (a.IdPRONAC = projetos.IdPRONAC)
INNER JOIN BDCorporativo.scSAC.tbComprovantePagamentoxPlanilhaAprovacao comprovacao ON (a.idPlanilhaAprovacao = comprovacao.idPlanilhaAprovacao)
INNER JOIN BDCorporativo.scSAC.tbComprovantePagamento tb_comprovacao ON (comprovacao.idComprovantePagamento = tb_comprovacao.idComprovantePagamento)
WHERE  a.nrFonteRecurso = 109
       AND (sac.dbo.fnVlComprovado_Fonte_Produto_Etapa_Local_Item
                  (a.idPronac,a.nrFonteRecurso,a.idProduto,a.idEtapa,a.idUFDespesa,a.idMunicipioDespesa, a.idPlanilhaItem)) > 0
GROUP BY CONCAT(projetos.AnoProjeto, projetos.Sequencial)
