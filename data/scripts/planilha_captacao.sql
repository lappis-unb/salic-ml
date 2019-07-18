SELECT Idcaptacao, LTRIM(RTRIM(capt.AnoProjeto+capt.Sequencial)) AS Pronac, proj.Segmento AS Segmento, NumeroRecibo, CgcCpfMecena, TipoApoio, MedidaProvisoria, DtChegadaRecibo, DtRecibo, CaptacaoReal, CaptacaoUfir, capt.logon,isBemServico
FROM SAC.dbo.Captacao capt
INNER JOIN SAC.dbo.Projetos	proj ON (capt.AnoProjeto = proj.AnoProjeto AND capt.Sequencial = proj.Sequencial)
