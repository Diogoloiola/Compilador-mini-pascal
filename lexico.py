import source.palavrasLinguagem

class analisadorLexicoErro(Exception): pass

class analisadorLexico():

    def __init__(self, arquivo):
        self.cabeca = 0
        self.arquivo = arquivo
        self.indiceAnterior = 0
        self.tabelaToknes = []

        self.tipos = source.palavrasLinguagem.tipos
        self.operadores = source.palavrasLinguagem.operadores
        self.palavrasReservdas = source.palavrasLinguagem.palavrasReservadas

        try:
            arquivoBuffer = open(arquivo,'r')
            self.arquivo = arquivoBuffer.read()
        except:
            print('Erro ao abrir o arquivo')

        self.sintatico = 0

    def voltarCabeca(self):
        self.cabeca -= 1

    def getCaractere(self):
	    return '\0' if self.cabeca >= len(self.arquivo) else self.arquivo[self.cabeca]

    def proximoCaractere(self):
	    if self.cabeca >= len(self.arquivo):
		    return '\0'
	    else:
		    self.cabeca += 1
		    return self.arquivo[self.cabeca - 1]
    
    def avancaEspacos(self):
	    while self.getCaractere() in ' \t\r\n':
		    self.proximoCaractere()

    def proximoToken(self): 
        Token, Value = self.lerToken()
        while Token == 'Comentario':
           Token, Value = self.lerToken()
            
        self.indiceAnterior += 1
        dados = [Token, Value,None, None]
        self.tabelaToknes.append(dados)
        return Token, Value

    def lerToken(self):
        self.avancaEspacos()
        caractere = self.proximoCaractere()
        if caractere == '\0':
            return None, None
        elif caractere.lower() in source.palavrasLinguagem.IDENTIFICADOR_CONSTANTE:
            return self.processaIdentificador(caractere)
        elif caractere.lower() in source.palavrasLinguagem.CONSTANTE_NUMEROS or caractere == '$':
            return self.processaNumeros(caractere)

    def processaNumeros(self, char):
        proximo = self.proximoCaractere()
        if proximo.lower() in source.palavrasLinguagem.IDENTIFICADOR_CONSTANTE:
            raise analisadorLexicoErro('identificador nao pode comecar com numero')
        self.voltarCabeca()
        numero = ''
        if char == '$':
            char = self.proximoCaractere().lower()
            if char not in source.palavrasLinguagem.CONSTANTE_NUMEROS_HEXADECIMAL:
                self.voltarCabeca()
                raise analisadorLexicoErro('Erro caractere $ nao e permitido')
            
            while char in source.palavrasLinguagem.CONSTANTE_NUMEROS_HEXADECIMAL:
                numero += char
                char = self.proximoCaractere().lower()
            
            self.voltarCabeca()
            return 'Inteiro', int(numero, 16)
        # Thiago finaliza a função como foi combinado na reunião

    def processaIdentificador(self, caractere):
        identificador = ''
        while caractere.lower() in source.palavrasLinguagem.IDENTIFICADOR_CONSTANTE or caractere.lower() in source.palavrasLinguagem.CONSTANTE_NUMEROS:
            identificador += caractere
            caractere = self.proximoCaractere()
        
        self.voltarCabeca()
        identificador = identificador.lower()
        if identificador == 'false' or identificador == 'true':
            return identificador.lower(),'Boolean'
        elif identificador in self.tipos.keys():
            return self.tipos[identificador].lower(), self.tipos[identificador].lower()
        elif identificador in self.operadores.keys():
            return self.operadores[identificador].lower(), self.operadores[identificador].lower()
        elif identificador in self.palavrasReservdas.keys():
            return self.palavrasReservdas[identificador].lower(), self.palavrasReservdas[identificador].lower()
        else:
            return identificador,'identificador'


    def criaTabela(self):
        while (self.cabeca < len(self.arquivo)):
            self.proximoToken()
    
