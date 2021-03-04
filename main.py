from typing import Text
import sys
from lexico import analisadorLexico
from sintatico import AnalisadorSintatico 

if __name__ == "__main__":
   lexico = analisadorLexico('main.pas')
   lexico.criaTabela()
   sintatico = AnalisadorSintatico(lexico.tabelaToknes)

   flag = sintatico.valida()
   print(flag)