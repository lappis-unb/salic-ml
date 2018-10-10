SELECT projetos.AnoProjeto + projetos.Sequencial as PRONAC,
idPRONAC,
UfProjeto,
Area,
Segmento,
NomeProjeto,
CgcCpf,
Situacao,
DtProtocolo,
DtSituacao,
DtInicioExecucao,
DtFimExecucao
FROM SAC.dbo.Projetos
;

