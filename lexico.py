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