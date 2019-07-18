SELECT LTRIM(RTRIM(CONCAT(capt.AnoProjeto, capt.Sequencial))) AS pronac,
       SUM(CaptacaoReal) as valor_captado
FROM SAC.dbo.Captacao capt
INNER JOIN SAC.dbo.Projetos	proj ON (capt.AnoProjeto = proj.AnoProjeto AND capt.Sequencial = proj.Sequencial)
GROUP BY CONCAT(capt.AnoProjeto, capt.Sequencial)
