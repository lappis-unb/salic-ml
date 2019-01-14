from api.salic_db.utils import make_query_from_db
from api.indicators.utils import string_formatter

def fetch_raised_funds(pronac_list):
    query = "SELECT capt.AnoProjeto+capt.Sequencial AS Pronac, SUM(CaptacaoReal) AS ValorCaptado \
            FROM SAC.dbo.Captacao capt \
            INNER JOIN SAC.dbo.Projetos	proj ON (capt.AnoProjeto = proj.AnoProjeto AND capt.Sequencial = proj.Sequencial) \
            WHERE (capt.AnoProjeto + capt.Sequencial) in {} \
            GROUP BY (capt.AnoProjeto + capt.Sequencial)".format(string_formatter.list_to_string_tuple(pronac_list))
    
    query_data = make_query_from_db(query)

    result = {}

    for line in query_data:
        result[line[0]] = {
            'pronac': line[0],
            'raised_funds': string_formatter.empty_or_valid_string(line[1])
        }

    return result  

def fetch_general_data(pronac_list):
    if len(pronac_list) == 0:
        return {}

    query = "SELECT projetos.AnoProjeto + projetos.Sequencial as PRONAC, \
            NomeProjeto, \
            situacao.Descricao as Situacao, \
            DtInicioExecucao, \
            DtFimExecucao, \
            verificacao.Descricao as Etapa, \
            situacao.Codigo as CodigoSituacao \
            FROM SAC.dbo.Projetos projetos \
            INNER JOIN SAC.dbo.Situacao situacao ON projetos.Situacao = situacao.Codigo \
            INNER JOIN SAC.dbo.tbProjetoFase fase ON (fase.idPronac = projetos.IdPRONAC) \
            INNER JOIN SAC.dbo.Verificacao verificacao ON (fase.idFase = verificacao.idVerificacao) \
            WHERE (projetos.AnoProjeto + projetos.Sequencial) in {}".format(string_formatter.list_to_string_tuple(pronac_list))

    query_data = make_query_from_db(query)

    result = {}

    for line in query_data:
        result[line[0]] = {
            'pronac': line[0],
            'name': line[1],
            'situation': string_formatter.empty_or_valid_string(line[6]) + ' - ' + string_formatter.empty_or_valid_string(line[2]),
            'start_date': string_formatter.empty_or_valid_string(line[3]),
            'end_date': string_formatter.empty_or_valid_string(line[4]),
            'stage': string_formatter.empty_or_valid_string(line[5])
        }

    return result  

    

def fetch_verified_funds(pronac_list):
    query = "SELECT (projetos.AnoProjeto + projetos.Sequencial) AS PRONAC, \
	        SUM(comprovacao.vlComprovado) AS vlComprovacao \
            FROM SAC.dbo.tbPlanilhaAprovacao aprovacao \
            INNER JOIN SAC.dbo.Projetos projetos ON (aprovacao.IdPRONAC = projetos.IdPRONAC) \
            INNER JOIN BDCorporativo.scSAC.tbComprovantePagamentoxPlanilhaAprovacao comprovacao ON (aprovacao.idPlanilhaAprovacao = comprovacao.idPlanilhaAprovacao) \
            WHERE  DtProtocolo>='2013-01-01 00:00:00' AND \
                aprovacao.nrFonteRecurso = 109 \
                AND (sac.dbo.fnVlComprovado_Fonte_Produto_Etapa_Local_Item \
                    (aprovacao.idPronac,aprovacao.nrFonteRecurso,aprovacao.idProduto,aprovacao.idEtapa,aprovacao.idUFDespesa,aprovacao.idMunicipioDespesa, aprovacao.idPlanilhaItem)) > 0 \
                AND (projetos.AnoProjeto + projetos.Sequencial) in {} \
            GROUP BY (projetos.AnoProjeto + projetos.Sequencial), projetos.DtProtocolo".format(string_formatter.list_to_string_tuple(pronac_list))
    
    query_data = make_query_from_db(query)

    result = {}

    for line in query_data:
        result[line[0]] = {
            'pronac': line[0],
            'verified_funds': string_formatter.empty_or_valid_string(line[1])
        }

    return result  
