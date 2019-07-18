SELECT LTRIM(RTRIM(projetos.AnoProjeto + projetos.Sequencial)) as PRONAC,
LTRIM(RTRIM(idPRONAC)) as idPRONAC,
LTRIM(RTRIM(UfProjeto)) as UfProjeto,
LTRIM(RTRIM(Area)) as Area,
LTRIM(RTRIM(Segmento)) as Segmento,
LTRIM(RTRIM(NomeProjeto)) as NomeProjeto,
LTRIM(RTRIM(CgcCpf)) as CgcCpf,
LTRIM(RTRIM(Situacao)) as Situacao,
DtProtocolo,
DtSituacao,
DtInicioExecucao,
DtFimExecucao
FROM SAC.dbo.Projetos
