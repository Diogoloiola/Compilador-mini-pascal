from typing import Text
from sintatico import AnalisadorSintatico 
import sys
from lexico import analisadorLexico


if __name__ == "__main__":
   if len(sys.argv) == 0:
      print('informe o caminho do arquivo')
   else:
      lexico = analisadorLexico(sys.argv[1])
      lexico.criaTabela()

      sintatico = AnalisadorSintatico(lexico.tabelaToknes)

      flag = sintatico.valida()
      if flag:
         print('analise lexica, sintatica, semantica ok')