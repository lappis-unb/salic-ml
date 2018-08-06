from finance.models.finances import Items, Captacoes, Receipts



class Project:
    def __init__(self, raw_project, raw_receipts, raw_captacoes):
        self.raw_project      = raw_project
        self.raw_receipts = raw_receipts
        self.raw_captacoes    = raw_captacoes
        
        self.pronac = self.setPronac()
        
        self.items = Items(self.setItemsList())
        self.receipts = Receipts(self.raw_receipts)
        self.captacoes = Captacoes(self.raw_captacoes)
        
        self.segment = self.setSegment()
        self.area = self.setArea()
        self.project_data = self.setProjetoData()
        
    def setItemsList(self):
        return self.raw_project.drop(['idPronac', 'PRONAC', 'Area', 'idArea','Segmento', 'idSegmento', 'DataProjeto'], axis=1)
    
    def setSegment(self):
        return [self.raw_project['Segmento'].iloc[0],self.raw_project['idSegmento'].iloc[0]]

    def setArea(self):
        return [self.raw_project['Area'].iloc[0],self.raw_project['idArea'].iloc[0]]
      
    def setPronac(self):
        return [self.raw_project['PRONAC'].iloc[0], self.raw_project['idPronac'].iloc[0]]

    def setProjetoData(self):
        return self.raw_project['DataProjeto'].iloc[0]


class ProjectsList:
    
    def __init__(self, planilhaOrcamentaria, planilhaComprovacao, planilhaCaptacao):
        self.planilhaOrcamentaria = planilhaOrcamentaria
        self.planilhaComprovacao = planilhaComprovacao
        self.planilhaCaptacao = planilhaCaptacao
        
        self.pronac_list = []
        # self.loaded_projects_list = []
        self.loaded_projects = {}
        

    # CREATE LIST OF ALL PRONAC's
    def createPronacList(self):
        return self.planilhaOrcamentaria.PRONAC.unique()
    
    # Array of tuples: [(filter1,value1),(filter2,value2)]
    def createPronacListForFilteredProjects(self, filters_and_values):
        filtered_pronacs = []
        for (filtered_column, filter_value) in filters_and_values:
            filtered_projects = self.planilhaOrcamentaria[self.planilhaOrcamentaria[filtered_column] == filter_value]
            if (len(filtered_projects) > 0):
                filtered_pronacs = filtered_projects.PRONAC.unique()
        return filtered_pronacs
    
    # GET SINGLE PROJECT BY PRONAC
    def getUnloadedProject(self, pronac):
        raw_project = self.planilhaOrcamentaria.loc[self.planilhaOrcamentaria['PRONAC'] == pronac]
        raw_receipts = self.planilhaComprovacao.loc[self.planilhaComprovacao['IdPRONAC'] == raw_project['idPronac'].iloc[0]]
        raw_captacoes = self.planilhaCaptacao.loc[self.planilhaCaptacao['Pronac'] == pronac]
        project = Project(raw_project, raw_receipts, raw_captacoes)
        return project

    
    # LOAD ALL PROJECTS
    def loadAllProjects(self):
        pronac_list = self.createPronacList()
        self.pronac_list = []
        
        for [i,pronac] in enumerate(pronac_list):
            # print('loading: ', i, ' / ', len(self.pronac_list))
            #self.loaded_projects_list.append(pronac)
            self.loaded_projects[pronac] = self.getUnloadedProject(pronac);
            self.pronac_list.append(pronac)
            
            # AVOID LOADING ALL PROJECTS.
            if i == 1000:
                break;

    # LOAD ALL PROJECTS
    def loadFilteredProjects(self, filters_and_values):
        pronac_list = self.createPronacListForFilteredProjects(filters_and_values)
        self.pronac_list = []
        
        for [i,pronac] in enumerate(pronac_list):
            # print('loading: ', i, ' / ', len(self.pronac_list))
            #self.loaded_projects_list.append(pronac)

            self.loaded_projects[pronac] = self.getUnloadedProject(pronac)
            self.pronac_list.append(pronac)
            
            # AVOID LOADING ALL PROJECTS.
            if i == 1000:
                break;

    # GET SINGLE PROJECT BY PRONAC
    def loadSingleProject(self, pronac):
        self.pronac_list = [pronac]
        #self.loaded_projects_list = [self.loaded_projects[pronac]]
        self.loaded_projects[pronac] = self.getUnloadedProject(pronac)
        return self.loaded_projects[pronac]

