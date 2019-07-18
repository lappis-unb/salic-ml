SELECT
	   LTRIM(RTRIM(CONCAT(projetos.AnoProjeto, projetos.Sequencial))) AS pronac,
	   SUM(comprovacao.vlComprovado) AS valor_comprovado
FROM SAC.dbo.tbPlanilhaAprovacao a
INNER JOIN SAC.dbo.Projetos projetos ON (a.IdPRONAC = projetos.IdPRONAC)
INNER JOIN BDCorporativo.scSAC.tbComprovantePagamentoxPlanilhaAprovacao comprovacao ON (a.idPlanilhaAprovacao = comprovacao.idPlanilhaAprovacao)
WHERE  a.nrFonteRecurso = 109
       AND (sac.dbo.fnVlComprovado_Fonte_Produto_Etapa_Local_Item
                  (a.idPronac,a.nrFonteRecurso,a.idProduto,a.idEtapa,a.idUFDespesa,a.idMunicipioDespesa, a.idPlanilhaItem)) > 0
GROUP BY CONCAT(projetos.AnoProjeto, projetos.Sequencial)
