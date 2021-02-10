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