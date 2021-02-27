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
        if self.getToken() == 'begin':
            self.parteDaDeclaracao()
            self.proximoElemento()
            if self.getToken() != '.':
                raise error('era esperado um .')
            return True
        self.proximoElemento()
        if self.parteDaDeclaracao():  #falta fazer que reconhece o escopo principal
            return True
        raise error('Deu errado aqui')
        
        return True


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
            if self.tipo(): # fazer função tipo
                return True
            raise error('tipo da variavel não foi especificada')

    def processaConstantes(self):
            self.proximoElemento()
            if self.getToken() != 'identificador':
                raise error('era esperado um identificador')
            self.proximoElemento()
            if self.getToken() != '=':
                raise error('era esperado um =')
            self.proximoElemento()
            if self.getToken() != ';':
               raise error('era esperado um ;')
            while True:
                if self.getToken() == ';':
                    self.proximoElemento()
                    if self.getToken() == 'identificador':
                        self.proximoElemento()
                        if self.getToken() != '=':
                            raise error('era esperado um =')
                        self.proximoElemento()
                        if self.expressao() == False:
                            raise error('algo deu errado') 
                        self.proximoElemento()
                else:
                    break
        self.voltar()
        if self.getToken() != ';':
            raise error('era esperado um ;')
        self.proximoElemento()
        return True
    
    def tipo(self):
        if self.tipoArray():
            return True
        if self.tiposPrimitivos():
            return True
        return False

    def expressao(self):
        '''
        analisa a expressão matematica
        '''
        if self.expressaoSimples():
            self.proximoElemento()
            if self.operadoresRelacionais():
                self.proximoElemento()
                if self.expressaoSimples():
                    return True
            else:
                self.voltar()
                return True 
        return False
    
    def expressaoSimples(self):
        # verificar aqui o 
        flag = self.sinais()
        if flag or flag == None:
            self.proximoElemento()
            if self.termo():
                aux = self.indice
                self.proximoElemento()
                if not self.operadorDeSoma():
                    self.indice = aux
                    return True
                else:
                    self.proximoElemento()
                    while True:
                        if self.termo():
                            aux = self.indice
                            self.proximoElemento()
                            if not self.operadorDeSoma():
                                self.indice = aux
                                return True
                            else:
                                self.proximoElemento()
                        else:
                            return False
                return True
    def sinais(self):
        if self.getToken() in ["+","-"]:
            return True
        self.voltar()
    
    def operadoresRelacionais(self):
        return self.getToken() in  ["=","<>","<","<=",">=",">","or","and"]

    def operadorDeMultiplicacao(self):
        if self.getToken() == '*' or self.getToken() == '/':
            return True
        return False

    def operadorDeSoma(self):
        if self.getToken() in ["+","-"]:
            return True
        return False
    
    def variavel(self):
        if self.variavelNormal():
            return True
        if self.variavelComIndice():
            return True
        return False
    
    def variavelNormal(self):
        if self.variavelComIdentificador():
            return True
        return False
    
    def variavelComIdentificador(self):
        if self.getToken() == 'numero':
            return True
        if self.getToken() == 'string':
            return True
        if self.getToken() == 'identificador':
            self.eVariavel()
            return True

    def variavelComIndice(self):
        if self.variavelArray():
            self.proximoElemento()
            if self.getToken() != '[':
                raise error('era esperado um ]')
            self.proximoElemento()
            if self.expressao():
                self.proximoElemento()
                if self.getToken() != ']':
                    raise error('era esperado um ]')
                self.proximoElemento()
                return True
    
    def variavelArray(self):
        return self.variavelNormal()

    def termo(self):
        if self.fator():
            aux = self.indice
            self.proximoElemento()
            if not self.operadorDeMultiplicacao():
                self.indice = aux
                return True
            else:
                self.proximoElemento()
                while True:
                    if self.fator():
                        aux = self.indice
                        self.proximoElemento()
                        if not self.operadorDeMultiplicacao():
                            self.indice = aux
                            return True
                        else:
                            self.proximoElemento()
                    else:
                        return False
    def fator(self):
        if self.variavel() or self.getToken() == 'numero':
            return True
        elif self.getToken() == '(':
            self.proximoElemento()
            if self.expressao():
                self.proximoElemento()
                if self.getToken() != ')':
                    raise error('era esperado um )')
                return True
        elif self.getToken() == 'not':
            self.proximoElemento()
            if self.fator():
                return True

    def tipoArray(self):
        if self.getToken() != 'array': 
            return False

        self.proximoElemento()
        if self.getToken() != '[':
            raise error('esta faltando o [')

        self.proximoElemento()

        if self.tamanhoArray():
            self.proximoElemento()
            if self.getToken() != ']':
                raise error('esta faltando o ]')
            self.proximoElemento()
            if self.getToken() != 'of':
                raise error('palavra of faltando')
            self.proximoElemento()
            
            if self.tiposPrimitivos():
                return True
            raise error('tipo da variavel não foi especificada')
        else:
            raise error('tamanho do array nao foi definido')

    def tamanhoArray(self):

        if self.getToken() != 'numero':
            raise error('era esperado um numero')
        self.proximoElemento()

        if self.getToken() != '..':
            raise error('era esperado ..')

        self.proximoElemento()
        if self.getToken() != 'numero':
           raise error('era esperado um numero')
        return True
        
    def tiposPrimitivos(self):
        if self.getToken() in ["char", "integer", "boolean","real"]:
            return True
        return False
    
    def parteDaDeclaracao(self):
        return self.declaracaoComposta()
    
    def declaracaoComposta(self):
        if self.getToken() != 'begin':
            return False

        self.proximoElemento()
        if self.getToken() == 'end':
            self.proximoElemento()
            if self.getToken() != ';':
                raise error('era esperado ;')
            self.proximoElemento()
            return True
        if self.Declaracao() != True:
            raise error('deu errado aqui 1')
    
    def Declaracao(self):
        '''
        declaração simples pode ser uma invocação
        uma atribuição, leitura e escrita de dados 
        '''
        if self.declaracaoSimples():
            return True
        if self.declaracaoEstruturada():
            return True
        return False
    
    def declaracaoSimples(self):
        if self.invocacao():
        '''
        ainda pra fazer
        '''
            return True
        elif self.atribuicao():
        '''
        ainda pra fazer
        '''
            return True
        elif self.leituraDeDados():
        '''
        ainda pra fazer
        '''
            return True
        elif self.escritaDeDados():
        '''
        ainda pra fazer
        '''
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