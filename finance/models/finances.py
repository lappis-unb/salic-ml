class Receipts:
    def __init__(self, raw_receipts):
        self.all_receipts = raw_receipts     
        
        
    def get_number_of_receipts(self):
        return len(self.all_receipts)

    def get_total_verified_cost(self):
        return sum(self.all_receipts['vlComprovacao'].values)
    
    def get_fornecedores(self):
        suppliers = self.all_receipts.nrCNPJCPF.unique()
        return suppliers

class Captacoes:
    def __init__(self, raw_captacao):
        self.all_captacoes = raw_captacao     
        
    def get_total_real_raised_funds(self):
        return sum(self.all_captacoes['CaptacaoReal'].values) # "CaptacaoReal","CaptacaoUfir"

class Items:
    def __init__(self, raw_items):
        self.all_items = raw_items
        
    
    def get_number_of_items(self):
        return self.all_items.shape[0]

    def get_quantity_of_items(self):
        quantity_of_items =  sum(self.all_items.QtItem * self.all_items.nrOcorrencia)
        return quantity_of_items
    
    def get_total_approved_cost(self):
        total_cost = sum(self.all_items.VlTotalAprovado)
        return total_cost
    
    def planilha_aprovacao_list(self):
        id_planilha_aprovacao = self.all_items['idPlanilhaAprovacao']
        return id_planilha_aprovacao.values
