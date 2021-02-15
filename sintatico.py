from os import error, truncate

class AnalisadorSintatico(object):
    def __init__(self, tabelaToknes):
        self.indice = 0
        self.tabela = []
        self.tabela = tabelaToknes

    def proximoElemento(self):
        self.indice += 1
    
    def voltar(self):
        self.indice -= 1