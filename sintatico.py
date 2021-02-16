from os import error, truncate

class AnalisadorSintatico(object):
    def __init__(self, tabelaToknes):
        self.indice = 0
        self.tabela = []
        self.tabela = tabelaToknes
        '''
        self.inicio = 0
        self.fim = 0
        self.cont = 0
        self.eAtribuicao = False
        self.eAtribuicaoTipoVariavel = False
        self.variaveisDaFuncoes = {}
        self.nomeFuncaoProcedimento = '' 
        self.declaracaoFuncoesProcedimento = []
        '''

    def proximoElemento(self):
        '''
        Avança na tabela de tokens
        '''
        self.indice += 1
    
    def voltar(self):
        '''
        Volta na tabela de tokens
        '''
        self.indice -= 1
    
    def getToken(self):
        '''
        Tras o token no indice corrente  
        '''
        if not self.fimArquivo():
            return self.tabela[self.indice][1]
     
    def fimArquivo(self):
        '''
        Chegou ao final da tabela  
        '''
        return self.indice == len(self.tabela)
    
    def program(self):
        '''
        Função ira validar o inicio do programa
        '''
        if self.getToken() != 'program':
            return False, 'Era esperado um program'

        self.proximoElemento()

        if self.getToken() != "identificador":
           return False, 'Era esperado um identificador'

        self.proximoElemento()

        if self.getToken() != ';':
           return False, 'Era esperado um ;'
        
        self.proximoElemento()
        flag = self.bloco()
        return flag
    
    def bloco(self):
        '''
        Falta implementar a função bloco
        '''
        return True
    
    def valida(self):
        '''
        Ira Chama a função que inicia a validação
        '''
        flag = self.program()
        if flag:
            return flag
        else:
            return flag
    
