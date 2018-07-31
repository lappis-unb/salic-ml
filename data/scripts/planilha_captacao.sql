SELECT Idcaptacao, capt.AnoProjeto+capt.Sequencial AS Pronac, NumeroRecibo, CgcCpfMecena, TipoApoio, MedidaProvisoria, DtChegadaRecibo, DtRecibo, CaptacaoReal, CaptacaoUfir, logon,isBemServico
FROM SAC.dbo.Captacao capt
