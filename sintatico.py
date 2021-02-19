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
    
    def eVariavel(self):
        self.tabela[self.indice][3] = 'var'
    
    def declaracao(self):
        """
            Criada a funcao que seta como true se a variavel está declarada
        """
        self.tabela[self.indice][2] = True

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
        if self.getToken() == 'var':
            self.declaracoesVariaveis1()
            if self.getToken() != ';':
                raise error('era esperado um ;')
            self.proximoElemento()
            if self.getToken() == 'const':
                self.processaConstantes()
        elif self.getToken() == 'const':
            self.processaConstantes()
            self.declaracoesVariaveis1()
            if self.getToken() != ';':
                raise error('era esperado um ;')
            self.proximoElemento()

    def declaracoesVariaveis1(self):
        if self.getToken() == 'var':
            self.proximoElemento()
            if self.declaracoesVariaveis2(): # fazer função reclarações variaveis 2 como discutimos na reunião.
                self.proximoElemento()
                if self.getToken() == ';':
                    aux = self.indice
                    self.proximoElemento()
                    if not self.declaracoesVariaveis2():
                        self.indice = aux
                        return True
                    else:
                        self.proximoElemento()
                        while True:
                            if self.getToken() == ';':
                                aux = self.indice
                                self.proximoElemento()

                                if not self.declaracoesVariaveis2():
                                    self.indice = aux
                                    return True
                                else:
                                    self.proximoElemento()
                            else:
                                raise error('precisa de ;')
                else:
                    raise error('era esperado um ;')
        else:
            return True
    
    def declaracoesVariaveis2(self):
        if self.getToken() == 'identificador':
            self.declaracao() #funcao feita
            self.eVariavel()

            self.proximoElemento()

            if self.getToken() == ':':
                self.proximoElemento()
            else:
                while True:
                    if self.getToken() == ',':
                        self.proximoElemento()
                        if self.getToken() == 'identificador':
                            self.declaracao() #funcao feita
                            self.eVariavel()

                            self.proximoElemento()

                            if self.getToken() == ':':
                                self.proximoElemento()
                                break
                    else:
                        raise error('algo falou aqui, tipo um :')
                        return False
            if self.tipo(): # fazer função tipo
                return True
            raise error('tipo da variavel não foi especificada')

    def processaConstantes(self):
        pass
    
    def tipo(self):
        if self.tipoArray():
            return True
        return False


    def valida(self):
        '''
        Ira Chama a função que inicia a validação
        '''
        flag = self.program()
        if flag:
            return flag
        else:
            return flag
    
