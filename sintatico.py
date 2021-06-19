from os import error, read, truncate

class AnalisadorSintatico(object):
    def __init__(self, tabelaToknes):
        self.indice = 0
        self.tabela = []
        self.declaracaoFuncoesProcedimento = []
        self.inicio = 0
        self.fim = 0
        self.cont = 0
        self.eAtribuicao = False
        self.eAtribuicaoTipoVariavel = False
        self.tabela = tabelaToknes
        self.variaveisDaFuncoes = {}
        self.nomeFuncaoProcedimento = ''
    
    def appendFuncaoProcedimento(self):
        self.declaracaoFuncoesProcedimento.append(self.tabela[self.indice])

    def proximoElemento(self):
        self.indice += 1
    
    def voltar(self):
        self.indice -= 1

    def getToken(self):
         if not self.fimArquivo():
            return self.tabela[self.indice][1]
    
    def getValor(self):
        return self.tabela[self.indice][0]

    def fimArquivo(self):
        return self.indice == len(self.tabela)
    
    def declaracao(self):
        self.tabela[self.indice][2] = True
    
    def eVariavel(self):
        self.tabela[self.indice][3] = 'var'

    def identificaFuncaoProcedimento(self, tipo):
        self.tabela[self.indice][2] = tipo
    
    def setQuantidadeParametros(self, indice):
        self.tabela[indice][3] = self.cont
        self.cont = 0

    def setVariavel(self, tipo, nomeFuncao):
        self.tabela[self.indice][4] = tipo
        if nomeFuncao != '':
            self.tabela[self.indice][5] = nomeFuncao

    def program(self):
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
        while True:
            if self.getToken() == 'procedure':
                self.procedimento()
            elif self.getToken() == 'function':
                self.funcao()
            else:
                break
        if self.getToken() == 'begin':
               self.parteDaDeclaracao()
               self.proximoElemento()
               if self.getToken() != '.':
                   raise error('era esperado um .')
               return True
        self.proximoElemento()
        if self.parteDaDeclaracao():
            return True
        raise error('Deu errado aqui')
        
    def procedimento(self):
        self.proximoElemento()
        if self.getToken() != 'identificador':
            raise error('era esperado um identificador')
        nomeFuncao = self.getValor()
        self.variaveisDaFuncoes[nomeFuncao] = []
        self.nomeFuncaoProcedimento = nomeFuncao
        self.identificaFuncaoProcedimento('procedure')
        self.appendFuncaoProcedimento()
        self.proximoElemento()
        if self.getToken() != ';':
            raise error('era esperado um ;')
        self.proximoElemento()

        if self.getToken() == 'var':
            self.declaracoesVariaveis1(None, nomeFuncao)
            if self.getToken() != ';':
                raise error('era esperado um ;')
            self.proximoElemento()
            if self.getToken() == 'const':
                self.processaConstantes()
        elif self.getToken() == 'const':
            self.processaConstantes()
            self.declaracoesVariaveis1(None, nomeFuncao)
            if self.getToken() != ';':
                raise error('era esperado um ;')
            self.proximoElemento()

        self.parteDaDeclaracao()
        self.proximoElemento()
        self.proximoElemento()
        self.nomeFuncaoProcedimento = ''

    def funcao(self):
        self.proximoElemento()
        if self.getToken() != 'identificador':
            raise error('era esperado um identificador')
        indiceFuncao = self.indice
        nomeFuncao = self.getValor()
        self.variaveisDaFuncoes[nomeFuncao] = []
        self.nomeFuncaoProcedimento = nomeFuncao
        self.identificaFuncaoProcedimento('function')
        self.appendFuncaoProcedimento()
        self.proximoElemento()
        if self.getToken() != '(':
            raise error('era esperado um (')
        self.proximoElemento()
        self.processaVariavelProcedimento(nomeFuncao)
        self.setQuantidadeParametros(indiceFuncao)
        if self.getToken() != ')':
                raise error('era esperado um )')
        self.proximoElemento()
        if self.getToken() != ':':
            raise error('era esperado um :')
        self.proximoElemento()
        if self.tipo()[0] != True:
            raise error('tipo da variavel não foi especificada')
        self.proximoElemento()
        if self.getToken() != ';':
            raise error('era esperado um ;')
        self.proximoElemento()

        if self.getToken() == 'var':
            self.declaracoesVariaveis1(None, nomeFuncao)
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

        self.parteDaDeclaracao()
        self.proximoElemento()
        self.proximoElemento()
        self.nomeFuncaoProcedimento = ''
        

    def processaConstantes(self):
        self.proximoElemento()
        if self.getToken() != 'identificador':
            raise error('era esperado um identificador')
        self.proximoElemento()
        if self.getToken() != '=':
            raise error('era esperado um =')
        self.proximoElemento()
        if self.expressao():
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

    def processaVariavelProcedimento(self,nomeFuncao):
         if self.getToken() == 'identificador':
            self.inicio = self.indice
            self.proximoElemento()
            self.proximoElemento()
            if self.declaracoesVariaveis2(True, nomeFuncao):
                self.proximoElemento()
                if self.getToken() == ';':
                    aux = self.indice
                    self.proximoElemento()
                    self.inicio = self.indice
                    if not self.declaracoesVariaveis2(True, nomeFuncao):
                        self.indice = aux
                        return True
                    else:
                        self.proximoElemento()
                        while True:
                            if self.getToken() == ';':
                                aux = self.indice
                                self.proximoElemento()
                                self.inicio = self.indice
                                if not self.declaracoesVariaveis2(True, nomeFuncao):
                                    self.indice = aux
                                    return True
                                else:
                                    self.proximoElemento()
                            else:
                                # self.proximoElemento()
                                break
                else:
                    return True
        

    def declaracoesVariaveis1(self, funcao = None, nomeFuncao = None):
        if self.getToken() == 'var':
            self.proximoElemento()
            self.inicio = self.indice
            if self.declaracoesVariaveis2(funcao, nomeFuncao):
                self.proximoElemento()
                if self.getToken() == ';':
                    aux = self.indice
                    self.proximoElemento()
                    self.inicio = self.indice
                    if not self.declaracoesVariaveis2(funcao, nomeFuncao):
                        self.indice = aux
                        return True
                    else:
                        self.proximoElemento()
                        while True:
                            if self.getToken() == ';':
                                aux = self.indice
                                self.proximoElemento()
                                self.inicio = self.indice
                                if not self.declaracoesVariaveis2(funcao, nomeFuncao):
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
        
    def declaracoesVariaveis2(self, funcao = None, nomeFuncao = None):
        if self.getToken() == 'identificador':
            self.declaracao()
            self.eVariavel()

            self.proximoElemento()

            if self.getToken() == ':':
                self.proximoElemento()
            else:
                while True:
                    if self.getToken() == ',':
                        self.proximoElemento()
                        if self.getToken() == 'identificador':
                            self.declaracao()
                            self.eVariavel()

                            self.proximoElemento()

                            if self.getToken() == ':':
                                self.proximoElemento()
                                break
                    else:
                        raise error('algo falou aqui, tipo um :')
                        return False
            flag, tipo = self.tipo()
            if flag:
                self.fim = self.indice - 2
                self.setTipoVariavel(tipo, funcao,nomeFuncao)
                return True
            raise error('tipo da variavel não foi especificada')
    
    def setTipoVariavel(self, tipo, funcao, nomeFuncao):
       estadoFinal = self.indice
       self.indice = self.inicio
       for i in range(self.indice, self.fim + 1):
            if self.getToken() != ',':
               self.setVariavel(tipo, nomeFuncao)
               if nomeFuncao != None:
                   if nomeFuncao != None and funcao == None:
                        self.tabela[self.indice][5] = 'campo' + nomeFuncao
                        self.variaveisDaFuncoes[nomeFuncao].append(self.tabela[self.indice])
                   else:
                        self.variaveisDaFuncoes[nomeFuncao].append(self.tabela[self.indice])
               self.proximoElemento()
               if funcao:
                   self.cont += 1
            else:
               self.proximoElemento()
       self.indice = estadoFinal        
    def tipo(self):
        if self.tipoArray():
            return True, ''
        flag, tipo = self.tiposPrimitivos()
        if flag:
            return True, tipo
        return False,''

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
        tipos =  ["char", "integer", "boolean","real"]
        indice = self.getToken() in tipos
        if indice:
            return True, self.tipoToken()
        return False,''

    def tipoToken(self):
      tipo = ''
      if self.getToken() == 'integer':
        tipo = 'inteiro'
      elif self.getToken() == 'char':
        tipo = 'string'
      elif self.getToken() == 'boolean':
        tipo = 'boolean'
      elif self.getToken() == 'real':
        tipo = 'real'  
      return tipo

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

        self.proximoElemento()
        if self.getToken() == 'end':
            return True
        else:
            while True:
                if self.getToken() == ';':
                    self.proximoElemento()
                    if self.Declaracao():
                        if self.getToken() != ';':
                            self.proximoElemento()
                elif self.getToken() == 'end':
                    return True
                else:
                    return False

    def Declaracao(self):
        if self.declaracaoSimples():
            return True
        if self.declaracaoEstruturada():
            return True
        return False

    def declaracaoEstruturada(self):
        if self.declaracaoComposta():
            return True
        elif self.declaracaoIf():
            return True
        elif self.declaracaoWhile():
            return True
    
    def declaracaoIf(self):
        if self.getToken() == 'if':
            self.proximoElemento()
            if self.expressao():
                self.proximoElemento()
                if self.getToken() != 'then':
                    raise error('era esperado um then')
                self.proximoElemento()
                if self.Declaracao():
                    self.proximoElemento()
                    if self.getToken() != ';':
                        return False
                    self.proximoElemento()
                    while True:
                        if self.Declaracao():
                            self.proximoElemento()
                            if self.getToken() != ';':
                                return False
                            self.proximoElemento()
                        else:
                            break
                    if self.getToken() == 'else':
                        self.proximoElemento()
                        if self.Declaracao():
                            # if self.getToken() != ')':
                            #     return False
                            self.proximoElemento()
                            if self.getToken() != ';':
                                return False
                            
                            if self.getToken() == ';':
                                self.voltar()
                                return True

                            self.proximoElemento()
                            return True
                    else:
                        self.voltar()
                        self.voltar()
                        return True
        return False

    def declaracaoWhile(self):
        if self.getToken() == 'while':
            self.proximoElemento()
            if self.expressao():
                self.proximoElemento()

                if self.getToken() != 'do':
                    raise error('era esperado um do')
                self.proximoElemento()
                if self.declaracaoComposta():
                    return True
                return False
        else:
            return False

    def declaracaoSimples(self):
        if self.invocacao():
            return True
        elif self.atribuicao():
            return True
        elif self.leituraDeDados():
            return True
        elif self.escritaDeDados():
            return True
        return False

    def leituraDeDados(self):
        if self.getToken() == 'read':
            self.proximoElemento()
            if self.getToken() != '(':
                raise error('era esperado um (')
            self.proximoElemento()
            if self.variavel():
                self.proximoElemento()
                if self.getToken() == ')':
                    return True
                else:
                    while True:
                        if self.getToken() == ',':
                            self.proximoElemento()
                            if self.variavel():
                                self.proximoElemento()
                        elif self.getToken() == ')':
                            return True
                        else:
                            raise error('algo de errado aconteuceu')

    def escritaDeDados(self):
        if self.getToken() == 'write':
            self.proximoElemento()
            if self.getToken() != '(':
                raise error('era esperado um (')
            self.proximoElemento()
            if self.variavel():
                self.proximoElemento()
                if self.getToken() == ')':
                    return True
                else:
                    while True:
                        if self.getToken() == ',':
                            self.proximoElemento()
                            if self.variavel():
                                self.proximoElemento()
                        elif self.getToken() == ')':
                            return True
                        else:
                            raise error('algo de errado aconteuceu')

    def invocacao(self):
        if self.getToken() != 'identificador':
           return False
        nomeFuncao = self.getValor()
        flag, tipo = self.buscaFuncaoProcedimento()
        
        self.proximoElemento()
        if self.getToken() != '(':
            self.voltar()
            return False
        if not flag:
            msg = 'funcao nao declarada' + nomeFuncao
            raise error(msg)
        self.proximoElemento()
        variaveis = self.getTiposVariaveisFuncoes(nomeFuncao) #ajeitar isso aqui
        indiceVariavel = 0
        while True:
            if tipo == 'procedure':
                break
            if self.variavel():
                if indiceVariavel >= len(variaveis):
                    msg = 'a quantidade de parametros esta errada, a quantidade fornecida foi ' + str(indiceVariavel + 1) + ' e quantidade esperada e ' + str(len(variaveis))
                    raise error(msg)
                if self.getToken() == 'numero':
                    tipoInteiro = type(self.getValor()) == int
                    tipofloat =  type(self.getValor()) == float

                    if tipoInteiro and variaveis[indiceVariavel] == 'inteiro':
                        indiceVariavel += 1
                    elif tipofloat and variaveis[indiceVariavel] == 'real':
                        indiceVariavel += 1
                    else:
                        raise error('tipos de incompatives na passagem de argumentos')
                elif self.getToken() == 'string':
                    tipoString =  type(self.getValor()) == str
                    if tipoString and variaveis[indiceVariavel] == 'string':
                        indiceVariavel += 1
                    else:
                        raise error('tipos de incompatives na passagem de argumentos') 
                else:
                    tipo = self.pesquisaVariavel()
                    if tipo == variaveis[indiceVariavel]:
                        indiceVariavel += 1
                    else:
                        raise error('tipos de incompatives na passagem de argumentos')
                self.proximoElemento()
                if self.getToken() == ',':
                    self.proximoElemento()
            else:
                break
        if indiceVariavel != len(variaveis):
            msg = 'a quantidade de parametros esta errada, a quantidade fornecida foi ' + str(indiceVariavel) + ' e quantidade esperada e' + str(len(variaveis))
            raise error(msg)
        if self.getToken() != ')':
            return False
        return True

    def pesquisaVariavel(self):
        token = self.getValor()
        indiceInicial = 4
        indiceAtual = self.indice
        self.indice = indiceInicial

        while self.getToken() == 'identificador' or self.getToken() in [',',':','char', 'integer', 'boolean','real',';']:
            if self.getValor() == token:
                tipoVariavel = self.tabela[self.indice][4]
                self.indice = indiceAtual
                return tipoVariavel
            self.proximoElemento()
        msg = 'a variavel ' + token + ' nao foi declarada'
        raise error(msg)

    def getTiposVariaveisFuncoes(self, nomeFuncao, flag = None):
        tipos = []
        for linha in self.variaveisDaFuncoes[str(nomeFuncao)]:
            if (linha[5] == nomeFuncao or linha[5] == 'campo' + nomeFuncao) and flag == True:
                return linha[4]
            elif linha[5] == nomeFuncao:
                tipos.append(linha[4])
        if flag == True:
            if len(tipos) == 0:
                raise error('variavel nao encontrada')
        return tipos

    def buscaFuncaoProcedimento(self):
        for i in self.declaracaoFuncoesProcedimento:
            if i[0] == self.getValor():
                return True, i[2]
        return False,''

    def atribuicao(self):
        tipo = None
        if self.getToken() != 'identificador':
            return False
        if  self.nomeFuncaoProcedimento != '':
            tipo = self.getTiposVariaveisFuncoes(self.nomeFuncaoProcedimento, True)
        if tipo == None:
            tipo = self.pesquisaVariavel()
        self.proximoElemento()
        if self.getToken() != ':=':
            raise error('era esperado um :=')
        self.proximoElemento()
        self.eAtribuicao = True
        self.eAtribuicaoTipoVariavel = tipo
        if self.expressao():
            self.proximoElemento()
            if self.getToken() != ';':
                raise error('era esperado um ;')
            self.voltar()
            self.eAtribuicao = False
            self.eAtribuicaoTipoVariavel = False
            return True
        raise error('deu erro na hora da atribuicao')

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
        if self.eAtribuicao:
            if self.getToken() == 'numero':
                tipoInteiro = type(self.getValor()) == int
                tipofloat =  type(self.getValor()) == float
                if tipoInteiro and self.eAtribuicaoTipoVariavel == 'inteiro':
                    return True
                elif tipofloat and self.eAtribuicaoTipoVariavel == 'real':
                    return True
                raise error('tipos inconpativeis')
            elif self.getToken() == 'string':
                tipoString =  type(self.getValor()) == str
                if tipoString and self.eAtribuicaoTipoVariavel == 'string':
                    return True
                msg = 'tipos incompativeis ' + self.getToken() + ' mas a variavel e do tipo ' + self.eAtribuicaoTipoVariavel
                raise error(msg)
            else:
                tipo = None
                if  self.nomeFuncaoProcedimento != '':
                    tipo = self.getTiposVariaveisFuncoes(self.nomeFuncaoProcedimento, True)
                if tipo == None:
                    tipo = self.pesquisaVariavel()
                if tipo == self.eAtribuicaoTipoVariavel:
                    return True
                raise error('tipos incompativeis')
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

    def expressao(self):
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

    def valida(self):
        flag = self.program()
        if flag:
            return flag
        else:
            return flag