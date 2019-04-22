/*

  Esse script retorna os projetos que não estão em situação finalizada
   - Pronac (AnoProjeto + Sequencial)
   - Nome do Projeto
   - Analista
   - Situação
   - Descrição da verificação
   - Data de inicio de execucação
   - Data de Fim de execução

   Obs: É usado o GROUP BY para remoção de projetos duplicados

*/

SELECT CONCAT(projetos.AnoProjeto, projetos.Sequencial) as pronac, MAX(NomeProjeto) as nome, MAX(Analista) as responsavel,
       MAX(Situacao) as situation, MAX(verificacao.Descricao) as description,
       MAX(DtInicioExecucao) as start_execution, MAX(DtFimExecucao) as end_execution
       FROM SAC.dbo.Projetos
       INNER JOIN SAC.dbo.tbProjetoFase fase ON (fase.idPronac = projetos.IdPRONAC)
       INNER JOIN SAC.dbo.Verificacao verificacao ON (fase.idFase = verificacao.idVerificacao)
       FULL JOIN SAC.dbo.tbPlanilhaAprovacao aprovacao ON (aprovacao.IdPRONAC = projetos.IdPRONAC)
       WHERE DtFimExecucao < GETDATE()
       AND Situacao NOT IN ('A09', 'A13', 'A14', 'A16', 'A17', 'A18', 'A20',
                              'A23', 'A24', 'A26', 'A40', 'A41', 'A42', 'C09',
                              'D18', 'E04', 'E09', 'E36', 'E47', 'E49', 'E63',
                              'E64', 'E65', 'G16', 'G25', 'G26', 'G29', 'G30',
                              'G56', 'K00', 'K01', 'K02', 'L01', 'L02', 'L03',
                              'L04', 'L05', 'L06', 'L08', 'L09', 'L10', 'L11')
        GROUP BY CONCAT(projetos.AnoProjeto, projetos.Sequencial)
