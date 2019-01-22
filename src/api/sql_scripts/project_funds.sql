/*
  Esse script retorna os fundos levantados de um projeto:
   - Pronac (AnoProjeto + Sequencial)
   - Fundos levantados
*/

SELECT capt.AnoProjeto+capt.Sequencial AS Pronac, SUM(CaptacaoReal) AS ValorCaptado
            FROM SAC.dbo.Captacao capt
            INNER JOIN SAC.dbo.Projetos	proj ON (capt.AnoProjeto = proj.AnoProjeto AND capt.Sequencial = proj.Sequencial)
      --      WHERE (capt.AnoProjeto + capt.Sequencial) in {} \
            GROUP BY (capt.AnoProjeto + capt.Sequencial) --.format(string_formatter.list_to_string_tuple(pronac_list))

/*
  Esse script retorna os fundos comprados de um projeto:
   - Pronac (AnoProjeto + Sequencial)
   - Fundos comprovados
*/

SELECT (projetos.AnoProjeto + projetos.Sequencial) AS PRONAC,
	        SUM(comprovacao.vlComprovado) AS vlComprovacao
            FROM SAC.dbo.tbPlanilhaAprovacao aprovacao
            INNER JOIN SAC.dbo.Projetos projetos ON (aprovacao.IdPRONAC = projetos.IdPRONAC)
            INNER JOIN BDCorporativo.scSAC.tbComprovantePagamentoxPlanilhaAprovacao comprovacao ON (aprovacao.idPlanilhaAprovacao = comprovacao.idPlanilhaAprovacao)
            WHERE  DtProtocolo>='2013-01-01 00:00:00' AND
                aprovacao.nrFonteRecurso = 109
                AND (sac.dbo.fnVlComprovado_Fonte_Produto_Etapa_Local_Item
                    (aprovacao.idPronac,aprovacao.nrFonteRecurso,aprovacao.idProduto,aprovacao.idEtapa,aprovacao.idUFDespesa,aprovacao.idMunicipioDespesa, aprovacao.idPlanilhaItem)) > 0
              --  AND (projetos.AnoProjeto + projetos.Sequencial) in {} \
            GROUP BY (projetos.AnoProjeto + projetos.Sequencial), projetos.DtProtocolo --.format(string_formatter.list_to_string_tuple(pronac_list))
